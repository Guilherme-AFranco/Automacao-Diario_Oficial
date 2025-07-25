@echo off
echo Ativando o ambiente virtual...
call "C:\Seu\diretorio\de\arquivos\venv\Scripts\activate"
if %errorlevel% neq 0 (
    echo Falha ao ativar o ambiente virtual.
    exit /b %errorlevel%
)
echo Ambiente virtual ativado.
 
echo Navegando para o diretório...
cd "C:\Seu\diretorio\de\arquivos"
if %errorlevel% neq 0 (
    echo Falha ao navegar para o diretório.
    exit /b %errorlevel%
)
echo Diretório acessado.
 
echo Executando o script Python...
python .\automation_diario_ofc.py
if %errorlevel% neq 0 (
    echo Falha ao executar o script Python.
    exit /b %errorlevel%
)
echo Script Python executado com sucesso.