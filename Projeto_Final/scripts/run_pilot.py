"""Ponto de entrada do piloto. Roda o nucleo com a UF de config (RN por padrao).

Uso:
    python -m Projeto_Final.scripts.run_pilot            # roda o RN
    python -m Projeto_Final.scripts.run_pilot --uf PB    # a mesma logica, outra UF

O provedor de dados real (leitura de PRF, SNV, VMDa, LAI) entra na fase 2. Este
script usa um provedor de demonstracao, so para exercitar o fluxo do esqueleto.
"""
from __future__ import annotations

import argparse

from Projeto_Final.custo_social_core import config, custo, pipeline, referenciamento


class ProvedorDemo:
    """Provedor de demonstracao: um trecho, dois sinistros. Substituido na fase 2."""

    def safras_snv(self):
        return ["201811A", "202001A", "202101A"]

    def segmentos_snv(self, safra, uf):
        return [referenciamento.SegmentoSNV(safra, 101, uf, 0.0, 20.0, 20.0)]

    def sinistros(self, uf):
        return [
            {"br": 101, "km": 5.0, "ano": 2020, "n_leves": 2, "n_graves": 1,
             "n_mortos": 0, "houve_dano": False},
            {"br": 101, "km": 8.0, "ano": 2021, "n_leves": 0, "n_graves": 0,
             "n_mortos": 1, "houve_dano": False},
        ]

    def vmda_segmento(self, safra, br, km_inicial):
        return 12000.0

    def tabela_custo_vitima(self, uf):
        return custo.CustoVitima(44290.53, 25000.0, 150000.0, 1253056.76)


def main() -> None:
    parser = argparse.ArgumentParser(description="Piloto de custo social por segmento.")
    parser.add_argument("--uf", default=config.UF, help="UF a processar (padrao: RN).")
    parser.add_argument("--cenario", default=config.CENARIO_SUBREGISTRO_PADRAO,
                        choices=list(config.FATOR_SUBREGISTRO))
    args = parser.parse_args()

    res = pipeline.rodar(ProvedorDemo(), uf=args.uf, cenario_subregistro=args.cenario)
    print(f"Piloto de custo social — UF={res.uf} — subregistro={res.cenario_subregistro}")
    print(f"{'BR':>4} {'km_ini':>7} {'km_fim':>7} {'custo_social':>16} "
          f"{'corrigido':>16} {'R$/km':>14} {'R$/veic-km':>12} {'corredor':>9}")
    for s in res.segmentos:
        exp = f"{s.custo_por_exposicao:.6f}" if s.custo_por_exposicao is not None else "imputada"
        print(f"{s.br:>4} {s.km_inicial:>7.1f} {s.km_final:>7.1f} {s.custo_social:>16.2f} "
              f"{s.custo_corrigido:>16.2f} {s.custo_por_km:>14.2f} {exp:>12} "
              f"{'sim' if s.corredor_destaque else 'nao':>9}")


if __name__ == "__main__":
    main()
