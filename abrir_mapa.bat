@echo off
REM Sobe o servidor local do mapa e abre o navegador. Nao instala nada.
REM O mapa usa so a biblioteca padrao do Python; basta um Python que rode.
REM
REM Prioridade do interpretador:
REM   1) PythonPortatil\python.exe ao lado desta pasta (pen drive, sem admin)
REM   2) o "python" do PATH, se a maquina ja tiver Python
REM
REM Requer apenas o arquivo dados\consolidado.db, que acompanha o repositorio.

cd /d "%~dp0"

set "PY="
if exist "..\PythonPortatil\python.exe" set "PY=..\PythonPortatil\python.exe"
if not defined PY (
  where python >nul 2>nul && set "PY=python"
)
if not defined PY (
  echo Nenhum Python encontrado.
  echo Coloque o Python embarcado em ..\PythonPortatil\ ou instale o Python no PATH.
  pause
  exit /b 1
)

if not exist "dados\consolidado.db" (
  echo Falta o banco dados\consolidado.db nesta pasta.
  pause
  exit /b 1
)

echo Subindo o servidor em http://127.0.0.1:8000/mapa
echo Feche esta janela para parar o servidor.
start "" http://127.0.0.1:8000/mapa
"%PY%" -c "import sqlite3; from src.consulta_web import executar_servidor; executar_servidor(sqlite3.connect('dados/consolidado.db')).serve_forever()"
