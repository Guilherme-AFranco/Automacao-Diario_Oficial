# Automação - Diário Oficial

### Instalação e configuração de softwares

**Python**
- Para instalação do pacote Python, entrar no site oficial do [Python](https://www.python.org/downloads/windows/) e realizar a instalação. Quando instalar, selecione "Add python.exe to PATH" no instalador.

**VSCode**
- Para instalação do software, entrar no site oficial do [Visual Studio](https://code.visualstudio.com/) e seguir o procedimento de instalação descrito.
- Após a instalação, abra o PowerShell no Windows (como administrador) e execute o comando "Set-ExecutionPolicy AllSigned -Force" para que possa ser usado o ambiente virtual dentro do VSCode.
- Inicie o VSCode, na aba esquerda, abra as configurações.
- Com as configurações abertas, no canto superior esquerdo aparecerá um item selecionavel "Open Settiongs (JSON)". Aba-o.
- (Opcional) Na aba esquerda do VSCode, encontre o icone "Extensions" e selecione-o. Dentro da aba, instale as extensões abaxo:
  - Code Runner;
  - Material Icon Theme;
  - Om Theme;
  - Pylance;
  - Python;
  - Python Debugger.
- (Opcional) Copie o código `JSON_config.txt` e cole no JSON que está aberto. Esta é apenas uma configuração de setup do VSCode.

**Git**
- Faça a instalação do Git a partir do site oficial [Git](https://git-scm.com/downloads) seguindo as recomendações descritas.

**Clonagem dos arquivos do Github para o VSCode**
- Dentro do VSCode, abra uma pasta onde deseja realizar a cópia dos arquivos do GitHub.
- Abra o terminal novamente e faça a clonagem dos arquivos do Github com o comando "git clone https://github.com/Guilherme-AFranco/Streamlit-Planar.git" (apenas para o primeiro uso)

**Criação e uso do ambiente virtual**
- Abra o VSCode e entre na pasta onde estão os arquivos do Dashboard;
- No canto superior direito da tela haverá uma opção "Toggle Panel (Ctrl + J)". Abra-o;
- Dentro do terminal que será aberto, digite "python -m venv venv" para criação do seu ambiente virtual na pasta em que estiver selecionada (faça isso apenas no primeiro acesso);
- Acesse-o utilizando o comando "\venv\Scripts\activate" e digite r para permitir (faça isso sempre que abrir o VSCode);
- Instale o arquivo `requirements.txt` dentro do seu ambiente virtual a partir do comando "pip install -r .\requirements.txt" (faça isso apenas no primeiro acesso).

**Instalação do ChromeDriver**
- Verifique a versão do seu navegador Google Chrome em: ... - Ajuda - Sobre o Google Chrome;
- Acesse [Chromedriver](https://googlechromelabs.github.io/chrome-for-testing/);
- Encontre a mesma versão do seu navegado;
- Faça download do .zip;
- Extraia em um local conhecido (recomendável que seja dentro do disco local e que seja na mesma página que serão armazenados os arquivos da automação).
