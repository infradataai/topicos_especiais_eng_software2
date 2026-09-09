"""Reconstroi o extrato deduplicado da PRF para uma UF (RF01 a RF04).

Uso:
    python -m scripts.reconstruir_prf \
        --origem "<pasta com acidentes<ano>_todas_causas_tipos.csv>" \
        --destino "<pasta de saida>" --uf RN --de 2019 --ate 2025

Gera, na pasta de destino, as quatro tabelas de grao unico em Parquet e CSV, o
vetor C por ocorrencia e o relatorio de ingestao por ano.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from custo_social_core import ingestao_prf


def main() -> None:
    p = argparse.ArgumentParser(description="Reconstroi o extrato deduplicado da PRF.")
    p.add_argument("--origem", required=True, type=Path)
    p.add_argument("--destino", required=True, type=Path)
    p.add_argument("--uf", default="RN")
    p.add_argument("--de", type=int, default=2019)
    p.add_argument("--ate", type=int, default=2025)
    args = p.parse_args()

    args.destino.mkdir(parents=True, exist_ok=True)
    tabelas, rel = ingestao_prf.ingerir(args.origem, args.uf, range(args.de, args.ate + 1))

    print(f"\n=== Ingestao PRF — UF={args.uf} ===")
    print(rel.para_dataframe().to_string(index=False))

    for nome, df in tabelas.items():
        df.to_parquet(args.destino / f"prf_{args.uf}_{nome}.parquet", index=False)
        df.to_csv(args.destino / f"prf_{args.uf}_{nome}.csv", index=False, encoding="utf-8")
        print(f"{nome:14s} {len(df):>8,} linhas")

    c = ingestao_prf.vetor_c(tabelas)
    c.to_parquet(args.destino / f"prf_{args.uf}_vetor_c.parquet", index=False)
    print(f"{'vetor_c':14s} {len(c):>8,} linhas")

    import pandas as pd
    achados = pd.DataFrame(ingestao_prf.validar(tabelas))
    print("\n=== Validacao (RF04) ===")
    print(achados.to_string(index=False))
    achados.to_csv(args.destino / f"prf_{args.uf}_validacao.csv", index=False, encoding="utf-8")

    rel.para_dataframe().to_csv(
        args.destino / f"prf_{args.uf}_relatorio_ingestao.csv", index=False, encoding="utf-8"
    )


if __name__ == "__main__":
    main()
