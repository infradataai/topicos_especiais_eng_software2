"""Execucao nacional: roda o nucleo para todas as UFs, ou para uma lista.

E a mesma logica do piloto RN, com a UF variando. O piloto e este script diferem
apenas pelo conjunto de UFs processadas, o que confirma a escala por parametro.

Uso:
    python -m scripts.run_nacional                 # todas as UFs
    python -m scripts.run_nacional --ufs RN PB CE  # um subconjunto

O provedor de dados nacional (leitura de PRF, SNV, VMDa, LAI de todas as UFs) entra
com os dados reais neste repositorio privado. Aqui fica um provedor de demonstracao,
so para exercitar o fluxo.
"""
from __future__ import annotations

import argparse

from custo_social_core import config, custo, pipeline, referenciamento

UFS_BR = [
    "AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG",
    "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO",
]


class ProvedorDemo:
    """Provedor de demonstracao, um trecho por UF. Substituido pelos dados reais."""

    def safras_snv(self):
        return ["201811A", "202001A", "202101A"]

    def segmentos_snv(self, safra, uf):
        return [referenciamento.SegmentoSNV(safra, 101, uf, 0.0, 20.0, 20.0)]

    def sinistros(self, uf):
        return [
            {"br": 101, "km": 5.0, "ano": 2020, "n_leves": 1, "n_graves": 1,
             "n_mortos": 0, "houve_dano": False},
        ]

    def vmda_segmento(self, safra, br, km_inicial):
        return 12000.0

    def tabela_custo_vitima(self, uf):
        return custo.CustoVitima(44290.53, 25000.0, 150000.0, 1253056.76)


def main() -> None:
    parser = argparse.ArgumentParser(description="Custo social por segmento, nacional.")
    parser.add_argument("--ufs", nargs="+", default=UFS_BR, help="UFs a processar.")
    parser.add_argument("--cenario", default=config.CENARIO_SUBREGISTRO_PADRAO,
                        choices=list(config.FATOR_SUBREGISTRO))
    args = parser.parse_args()

    provedor = ProvedorDemo()
    for uf in args.ufs:
        res = pipeline.rodar(provedor, uf=uf, cenario_subregistro=args.cenario)
        total = sum(s.custo_social for s in res.segmentos)
        print(f"{uf}: {len(res.segmentos)} segmento(s), custo social R$ {total:,.2f}")


if __name__ == "__main__":
    main()
