# Como rodar o mapa sem instalar nada, e sem administrador

O mapa dos trechos críticos é um servidor local em Python que lê um só
arquivo, o `dados/consolidado.db`. Ele usa apenas a biblioteca padrão do Python,
então não precisa de `pip install`, nem de internet, nem de direito de
administrador. Só precisa de um Python que rode na máquina.

## O que levar

Duas pastas, num pen drive:

- `Tese_BR_TEES`, o repositório, com o `dados/consolidado.db` dentro.
- `PythonPortatil`, o Python embarcado, para o caso de a máquina não ter Python.

O `dados/consolidado.db`, de cerca de 9 MB, acompanha o repositório e é tudo o
que o mapa consome. Os 35 GB de dados de origem não são necessários para rodar.

## Preparar o Python embarcado, uma vez, numa máquina com internet

1. No site oficial python.org, na página de downloads do Windows, baixe o
   **Windows embeddable package (64-bit)**. É um arquivo `.zip`, e não um
   instalador, por isso não pede administrador.
2. Extraia o conteúdo numa pasta chamada `PythonPortatil`.
3. Copie a pasta `PythonPortatil` para o pen drive, ao lado da pasta
   `Tese_BR_TEES`.

Se a máquina do DNIT já tiver Python instalado, esse passo é dispensável: o
atalho abaixo usa o Python do sistema quando não encontra o portátil.

## Rodar

Na máquina do DNIT, entre na pasta `Tese_BR_TEES` e dê **dois cliques em
`abrir_mapa.bat`**. Ele abre o navegador em `http://127.0.0.1:8000/mapa` e sobe o
servidor. A janela preta que aparece é o servidor: enquanto ela estiver aberta, o
mapa funciona. Para parar, feche a janela.

O atalho procura o Python nesta ordem: primeiro o `..\PythonPortatil\python.exe`,
ao lado da pasta; depois o `python` do sistema. Se não achar nenhum, avisa na
tela.

## Estrutura esperada no pen drive

```
PenDrive\
  PythonPortatil\
    python.exe
    ...
  Tese_BR_TEES\
    abrir_mapa.bat
    dados\consolidado.db
    src\
    custo_social_core\
    ...
```

## O endereço é local

O `127.0.0.1` abre apenas na própria máquina que roda o servidor. Para mostrar
numa tela de reunião, abra o navegador nessa mesma máquina. Expor o mapa para
outros computadores da rede do DNIT dependeria de trocar o endereço e de
liberação da equipe de rede, e fica fora deste guia.

## Resolução de problemas

- **A janela preta abre e fecha na hora.** O Python não foi encontrado, ou o
  banco não está em `dados\consolidado.db`. Rode o `abrir_mapa.bat` a partir de um
  Prompt de Comando para ler a mensagem.
- **O navegador diz que não consegue conectar.** O servidor não está de pé.
  Confirme que a janela preta continua aberta e recarregue a página.
- **A porta 8000 está ocupada.** Feche a instância anterior do servidor, ou
  reinicie a máquina, e rode de novo.
