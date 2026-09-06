"""Nucleo de calculo do custo social de sinistros, parametrizado por UF.

O piloto roda com uf='RN'; a escala nacional roda o mesmo codigo com outra UF.
Modulos de dominio (referenciamento, custo, exposicao, subregistro) nao importam
uns aos outros; apenas leem constantes de config. O pipeline os compoe.
"""
