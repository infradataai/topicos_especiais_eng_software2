# Roteiro do GIF do mapa (para o post do LinkedIn)

Objetivo: um GIF de 6 a 8 segundos do mapa de trechos críticos, salvo em `docs/trechos-criticos-mapa.gif`.

## Como gravar (ScreenToGif — grátis, Windows)

1. Instale o ScreenToGif: https://www.screentogif.com/ (ou pela Microsoft Store).
2. Suba o servidor: duplo-clique em `abrir_mapa.bat`. O mapa abre em `http://127.0.0.1:8000/mapa`.
3. No ScreenToGif, escolha **Gravadora** e posicione o retângulo de captura sobre a área do mapa (sem a barra do navegador).
4. Clique em **Gravar** e execute o roteiro abaixo. Clique em **Parar** ao final.
5. Em **Editar**, corte para 6–8 s, e salve como GIF em `docs/trechos-criticos-mapa.gif`.

## Roteiro (8 segundos)

1. Estado inicial: RN, leitura "custo por quilometro" (1 s).
2. Trocar a leitura para "custo por veiculo-quilometro" e clicar em **Consultar** (2 s) — as cores dos trechos mudam.
3. Clicar duas vezes no botão **+** para dar zoom num corredor da malha do RN (2 s).
4. Passar o cursor sobre um trecho preto (com óbito) para o popup aparecer (2 s).
5. Segurar o quadro final por 1 s.

## Alternativa: captura estática

Se preferir imagem em vez de GIF, uma captura de tela do mapa (RN, com a caixa "Custo social por ano" visível, somando R$ 1.915.035.912) já comunica o resultado e atende o pedido do professor de conteúdo visual.

## Nota

A gravação automatizada pela extensão Claude no Chrome foi tentada, mas o service worker do Chrome dormia entre um comando e outro e derrubava a conexão. A gravação manual acima é o caminho estável.
