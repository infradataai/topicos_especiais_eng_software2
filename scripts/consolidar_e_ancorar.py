"""Consolida o banco de uma UF e ancora as ocorrencias nos segmentos do SNV.

Uso:
    python -m scripts.consolidar_e_ancorar --uf RN \
        --silver dados/prf/silver --snv "<pasta das planilhas SNV>"

Le as tabelas da ingestao, calcula o custo por ocorrencia, ancora cada uma na
safra vigente do SNV e grava tudo no banco consolidado, com proveniencia.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import pandas as pd

from custo_social_core import (custo, exposicao as expo, persistencia as pst,
                               saude, snv)

CLS = {"Sem Vítimas": "sem_vitimas", "Com Vítimas Feridas": "com_vitimas",
       "Com Vítimas Fatais": "com_fatalidade"}


def safras_disponiveis(pasta: Path) -> dict[str, Path]:
    """Mapeia o rotulo da safra para o arquivo, a partir do nome SNV_<safra>.xls."""
    out = {}
    for f in sorted(pasta.glob("SNV_*.xls*")):
        m = re.search(r"SNV_(\d{6}[A-Za-z]*)", f.name)
        if m:
            out[m.group(1)] = f
    return out


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--uf", default="RN")
    p.add_argument("--silver", type=Path, default=Path("dados/prf/silver"))
    p.add_argument("--snv", type=Path, required=True)
    p.add_argument("--vmda", type=Path, default=None, help="pasta do PNCT/VMDa")
    p.add_argument("--datasus", type=Path, default=None, help="pasta dos agregados")
    p.add_argument("--banco", type=Path, default=None)
    a = p.parse_args()

    banco = a.banco or pst.caminho_banco_padrao()
    eng = pst.criar_esquema(banco)
    print(f"banco: {banco}")

    # 1. tabelas da ingestao
    tabs = {}
    for nome in ("ocorrencias", "veiculos", "pessoas", "causas_tipos"):
        f = a.silver / f"prf_{a.uf}_{nome}.parquet"
        tabs[nome] = pd.read_parquet(f)
        n = pst.carregar(eng, nome, tabs[nome], orgao="PRF", arquivo=f.name,
                         referencia=f"{a.uf} 2019-2025")
        print(f"  {nome:<14} {n:>7,} inseridas  (tabela com {pst.contar(eng, nome):,})")

    oc, pe, ve = tabs["ocorrencias"], tabs["pessoas"], tabs["veiculos"]

    # 2. custo por ocorrencia
    cg = pe.groupby(["id", "gravidade"]).size().unstack(fill_value=0)
    cv = ve.groupby(["id", "tipo_veiculo"]).size().unstack(fill_value=0)
    linhas = []
    for _, r in oc.iterrows():
        i = r["id"]
        vc = {}
        if i in cg.index:
            vc.update({k: int(v) for k, v in cg.loc[i].items() if v})
        if i in cv.index:
            vc.update({k: int(v) for k, v in cv.loc[i].items() if v})
        rc = custo.custo_ocorrencia(vc, CLS[r["classificacao_acidente"]])
        linhas.append({"id": i, "total": rc.total, "subtotal_pessoas": rc.subtotal_pessoas,
                       "subtotal_veiculos": rc.subtotal_veiculos,
                       "subtotal_institucional": rc.subtotal_institucional,
                       "categoria": rc.categoria, "base_monetaria": rc.base_monetaria})
    custos = pd.DataFrame(linhas)
    pst.carregar(eng, "custo_ocorrencia", custos, orgao="interno",
                 arquivo="calculo C.M", referencia="jun/2026")
    print(f"  custo_ocorrencia {len(custos):>5,} | total R$ {custos['total'].sum():,.2f}")

    # 3. segmentos do SNV, por safra usada
    safras = safras_disponiveis(a.snv)
    anos = sorted(oc["ano"].dropna().astype(int).unique())
    usadas = {}
    for ano in anos:
        try:
            usadas[ano] = snv.selecionar_safra(ano, list(safras))
        except snv.SafraIndisponivel:
            usadas[ano] = None
    print(f"  safras por ano: { {k: v for k, v in usadas.items()} }")

    segs = {}
    for s in {v for v in usadas.values() if v}:
        d = snv.ler_safra(safras[s], uf=a.uf)
        d.insert(0, "safra", s)
        segs[s] = d
        pst.carregar(eng, "segmentos_snv", d, orgao="DNIT",
                     arquivo=safras[s].name, referencia=s)
    print(f"  segmentos_snv  {pst.contar(eng, 'segmentos_snv'):>7,} (de {len(segs)} safras)")

    # 4. ancoragem
    anc = []
    for _, r in oc.iterrows():
        ano = r["ano"]
        s = usadas.get(int(ano)) if pd.notna(ano) else None
        if s is None:
            anc.append({"id": r["id"], "safra": None, "codigo_segmento": None,
                        "houve_desempate": 0, "motivo": "sem safra vigente"})
            continue
        res = snv.ancorar(int(r["br"]) if pd.notna(r["br"]) else -1, a.uf,
                          float(r["km"]) if pd.notna(r["km"]) else -1.0, segs[s])
        anc.append({"id": r["id"], "safra": s, "codigo_segmento": res.codigo,
                    "houve_desempate": int(res.houve_desempate), "motivo": res.motivo})
    anc = pd.DataFrame(anc)
    pst.carregar(eng, "ancoragem", anc, orgao="interno", arquivo="ancoragem SNV",
                 referencia="safra casada por ano")

    ok = anc["codigo_segmento"].notna().sum()
    print(f"\n=== Ancoragem ({a.uf}) ===")
    print(f"  ancoradas:        {ok:,} de {len(anc):,}  ({100*ok/len(anc):.1f}%)")
    print(f"  com desempate:    {int(anc['houve_desempate'].sum()):,}")
    print(f"  nao ancoradas:    {len(anc)-ok:,}")

    # 5. exposicao de trafego (PNCT/VMDa)
    if a.vmda:
        for f in sorted(a.vmda.glob("VMDa_*.xlsx")):
            ano = int(re.search(r"VMDa_(\d{4})", f.name).group(1))
            try:
                d = expo.agregar_por_segmento(expo.ler_vmda(f))
            except expo.AbaDeDadosAusente as e:
                print(f"  VMDa {ano}: ignorado ({e})")
                continue
            d = d[d["uf"] == a.uf].copy()
            d["ano"] = ano
            d["sentidos_completos"] = d["sentidos_completos"].astype(int)
            pst.carregar(eng, "exposicao_segmento", d, orgao="DNIT/PNCT",
                         arquivo=f.name, referencia=str(ano))
        print(f"  exposicao_segmento {pst.contar(eng, 'exposicao_segmento'):>5,}")

    # 6. agregados do DATASUS
    if a.datasus:
        mapa = {"obitos_transporte_SIM_uf_ano.csv": ("obitos_sim", "SIM"),
                "sih_internacoes_V01_V99_uf_ano_mes.csv": ("internacoes_sih", "SIH")}
        for nome, (tabela, orgao) in mapa.items():
            f = a.datasus / nome
            if not f.exists():
                print(f"  {tabela}: arquivo ausente ({nome})")
                continue
            d = saude.ler_agregado(f)
            pst.carregar(eng, tabela, d, orgao=f"DATASUS/{orgao}",
                         arquivo=nome, referencia="2019-2025")
            print(f"  {tabela:<18} {pst.contar(eng, tabela):>5,}")

    # 7. trechos criticos
    r = pst.custo_por_segmento(eng, uf=a.uf)
    if not r.empty:
        print(f"\n=== Trechos criticos de {a.uf} (top 10 por custo por km) ===")
        top = r.sort_values("custo_por_km", ascending=False).head(10)
        print(f"{'codigo':<14}{'BR':>5}{'km':>8}{'regime':>8}{'ocorr.':>8}"
              f"{'custo social':>18}{'R$/km':>16}")
        for _, x in top.iterrows():
            print(f"{x['codigo']:<14}{int(x['br']):>5}{x['extensao']:>8.1f}"
                  f"{str(x['regime']):>8}{int(x['ocorrencias']):>8}"
                  f"{x['custo_social']:>18,.0f}{x['custo_por_km']:>16,.0f}")
        # as duas leituras lado a lado
        r["custo_por_km"] = r["custo_social"] / r["extensao"]
        r["criticidade"] = r.apply(
            lambda x: expo.criticidade(x["custo_social"], x.get("vmda"), x["extensao"]),
            axis=1)
        com_exp = r["criticidade"].notna()
        print(f"\n  segmentos com ocorrencia: {len(r):,}"
              f" | extensao ancorada: {r['extensao'].sum():,.1f} km")
        print(f"  com exposicao medida: {com_exp.sum():,} ({100*com_exp.mean():.0f}%)")

        if com_exp.any():
            print("\n=== As duas leituras: custo por km x custo por exposicao ===")
            k = r.sort_values("custo_por_km", ascending=False).head(8)["codigo"].tolist()
            c = r[com_exp].sort_values("criticidade", ascending=False).head(8)["codigo"].tolist()
            print(f"{'pos':>4}  {'por R$/km':<14}{'por R$/veic-km':<14}")
            for i in range(8):
                print(f"{i+1:>4}  {k[i] if i < len(k) else '':<14}"
                      f"{c[i] if i < len(c) else '':<14}")
            comuns = len(set(k) & set(c))
            print(f"\n  segmentos em comum no top 8: {comuns} de 8"
                  f"  -> {8-comuns} trechos so aparecem numa das leituras")
        print("\n=== Por regime ===")
        g = r.groupby("regime").agg(seg=("codigo", "size"), km=("extensao", "sum"),
                                    custo=("custo_social", "sum"))
        g["custo_por_km"] = g["custo"] / g["km"]
        for k, x in g.iterrows():
            print(f"  {k:<8}{int(x['seg']):>5} segmentos  {x['km']:>9,.1f} km"
                  f"  R$ {x['custo']:>16,.0f}  R$/km {x['custo_por_km']:>12,.0f}")


if __name__ == "__main__":
    main()
