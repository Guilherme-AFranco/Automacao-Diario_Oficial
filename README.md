# Automação - Diário Oficial

### Instalação e configuração de softwares

**Python**
- Para instalação do pacote Python, entrar no site oficial do [Python](https://www.python.org/downloads/windows/) e realizar a instalação. Quando instalar, selecione "Add python.exe to PATH" no instalador.

**VSCode**
- Para instalação do software, entrar no site oficial do [Visual Studio](https://code.visualstudio.com/) e seguir o procedimento de instalação descrito.
- Inicie o VSCode. Na aba da esquerda, abra as configurações.
- (Opcional) Com as configurações abertas, no canto superior esquerdo aparecerá um item selecionavel "Open Settiongs (JSON)". Aba-o.
- (Opcional) Copie o código `JSON_config.txt` e cole no JSON que está aberto. Esta é apenas uma configuração de setup do VSCode.
- (Opcional) Na aba esquerda do VSCode, encontre o icone "Extensions" e selecione-o. Dentro da aba, instale as extensões abaxo:
  - Code Runner;
  - Material Icon Theme;
  - Om Theme;
  - Pylance;
  - Python;
  - Python Debugger.

**Git**
- Faça a instalação do Git a partir do site oficial [Git](https://git-scm.com/downloads) seguindo as recomendações descritas.

**Clonagem dos arquivos do Github para o VSCode**
- Dentro do VSCode, abra uma pasta onde deseja realizar a cópia dos arquivos do GitHub.
- Abra o terminal novamente e faça a clonagem dos arquivos do Github com o comando "git clone https://github.com/Guilherme-AFranco/Streamlit-Planar.git" (apenas para o primeiro uso).

**Criação e uso do ambiente virtual**
- Abra o VSCode e entre na pasta onde estão os arquivos do Dashboard;
- No canto superior direito da tela haverá uma opção "Toggle Panel (Ctrl + J)". Abra-o;
- Dentro do terminal que será aberto, digite "python -m venv venv" para criação do seu ambiente virtual na pasta em que estiver selecionada (faça isso apenas no primeiro acesso);
- Antes de acessar seu ambiente virtual no terminal, digite "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process" para habilitar o uso dele.
- Acesse-o utilizando o comando "\venv\Scripts\activate" e digite r para permitir (faça isso sempre que abrir o VSCode e quiser realizar uma compilação pelo terminal ou no primeiro uso para que seja possível instalar as bibliotecas necessárias);
- Instale o arquivo `requirements.txt` dentro do seu ambiente virtual a partir do comando "pip install -r .\requirements.txt" (faça isso apenas no primeiro acesso).

**Instalação do ChromeDriver**
- Verifique a versão do seu navegador Google Chrome em: ... - Ajuda - Sobre o Google Chrome;
- Acesse [Chromedriver](https://googlechromelabs.github.io/chrome-for-testing/);
- Encontre a mesma versão do seu navegado;
- Faça download do .zip;
- Extraia em um local conhecido (recomendável que seja dentro do disco local e que seja na mesma página que serão armazenados os arquivos da automação).
