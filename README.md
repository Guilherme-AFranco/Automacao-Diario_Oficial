# Automação - Diário Oficial

### Instalação e configuração de softwares

**Python (apenas para o primeiro uso)**
- Para instalação do pacote Python, entrar no site oficial do [Python](https://www.python.org/downloads/windows/) e realizar a instalação. Quando instalar, selecione "Add python.exe to PATH" no instalador.

**VSCode (apenas para o primeiro uso)**
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

**Git (apenas para o primeiro uso)**
- Faça a instalação do Git a partir do site oficial [Git](https://git-scm.com/downloads) seguindo as recomendações descritas.

**Clonagem dos Arquivos do Github para o VSCode (apenas para o primeiro uso)**
- Dentro do VSCode, abra uma pasta onde deseja realizar a cópia dos arquivos do GitHub.
- Abra o terminal novamente e faça a clonagem dos arquivos do Github com o comando "git clone https://github.com/Guilherme-AFranco/Streamlit-Planar.git" (apenas para o primeiro uso).

**Criação e Uso do Ambiente Virtual (apenas para o primeiro uso)**
- Abra o VSCode e entre na pasta onde estão os arquivos do Dashboard;
- No canto superior direito da tela haverá uma opção "Toggle Panel (Ctrl + J)". Abra-o;
- Dentro do terminal que será aberto, digite "python -m venv venv" para criação do seu ambiente virtual na pasta em que estiver selecionada (faça isso apenas no primeiro acesso);
- Antes de acessar seu ambiente virtual no terminal, digite "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process" para habilitar o uso dele.
- Acesse-o utilizando o comando "\venv\Scripts\activate" e digite r para permitir (faça isso sempre que abrir o VSCode e quiser realizar uma compilação pelo terminal ou no primeiro uso para que seja possível instalar as bibliotecas necessárias);
- Instale o arquivo `requirements.txt` dentro do seu ambiente virtual a partir do comando "pip install -r .\requirements.txt" (faça isso apenas no primeiro acesso).

**Instalação do ChromeDriver (primeiro uso e quando houver atualização do navegador Chrome)**
- Verifique a versão do seu navegador Google Chrome em: ... - Ajuda - Sobre o Google Chrome;
- Acesse [Chromedriver](https://googlechromelabs.github.io/chrome-for-testing/);
- Encontre a mesma versão do seu navegado;
- Faça download do .zip;
- Extraia em um local conhecido (recomendável que seja dentro do disco local e que seja na mesma página que serão armazenados os arquivos da automação).

**Execução do programa**

- Execute o arquivo `automacao_DOD.bat`.

### Observações Importantes

Antes de executar a automação, é importante configurar alguns campos conforme o seu uso. Para isso, deixo destacado aqui quais campos serão necessários realizar ajustes:

**Configurações Finais**

Para o primeiro uso, será necessário incluir algumas informações pessoais nos seus arquivos.

- automation_diario_ofc.py:
  - Linha 154: `email.BCC = "example1@domain.com.br; example2@domain.com.br"`

    Ação: Inclua os e-mails dos destinatários seguindo o formato indicado.
  - Linha 176: `email.SendUsingAccount = outlook.Session.Accounts.Item("example@domain.com.br")`

    Ação: Inclua o seu e-mail do Outlook.
  - Linha 177: `email.SentOnBehalfOfName = "example@domain.com.br"`

    Ação: Inclua o endereço de email secundário (será o remetente que aparecerá para os destinatários).
- automacao_DOD.bat:
  - Linha 3: `call "C:\Seu\diretorio\de\arquivos\venv\Scripts\activate"`

    Ação: Inclua o diretório que estão alocados os seus arquivos seguindo o modelo acima. Não esqueça que o final do diretório deve ser `\venv\Scripts\activate`.
  - Linha 11: `cd "C:\Seu\diretorio\de\arquivos"`

    Ação: Inclua seu diretório onde estão alocados os arquivos. Note que aqui é apenas o diretório mesmo.
- html_draft_start.txt:
  - Linha 7: `<title>Diário Oficial / Company</title>`

    Ação: Incluir a área/empresa no início da mensagem.
- html_draft_end.txt:
  - Linha 7: `<p> Signature </p>`

    Ação: Influir a assinatura.
  - Linha 9: `<img src="https://IMAGEM.com" alt="" width="144" height="40"`

    Ação: Incluir o html de um logo da empresa que esteja disponível na web.

**Publicação de Dias Retroativos**

Caso não seja possível publicar a automação em algum dia específico (como os dias anteriores à feriados ou por instabilidade no site), é importante realizar algumas alteraçãos, **que devem ser desfeitas após o uso**. Isso pode ser feito utilizando o VSCode (mais intuitivo) ou abrindo os arquivos no bloco de notas.

- Alteração no arquivo Scrapping.py:
  - Linha 49: `# data_formatada = "DD/MM/AAAA"`

    Ação: Descomentar e incluir a data que deseja realizar a coleta, seguindo o formato DD/MM/AAAA. Após alterar, certifique-se de salvar as alterações ("Ctrl+S").
- Alteração no arquivo automation_diario_ofc.py:
  - Linhas 162, 165, 168, 171: `# email.Subject = f"Retroactive day {formatted_date}:.......`

    Ação: Descomentar e salvar as alterações no arquivo.

**Atualização do Chromedriver**

Geralmente erros que acontecem na automação é por conta do chromedriver desatualizado. Então quando houver erro, baixe a versão atualizada do chromedriver e substitua-o na pasta da automação.
