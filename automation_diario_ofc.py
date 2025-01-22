import win32com.client as win32
from datetime import datetime
from Scrapping import *

## Coleta das informações da web ##
secao = ["do2", "do3"] # Seções a analisar
search = ["", "aeronave"] # # Pesquisas a analisar com base nas seções
orgPrinc = ["Ministério da Defesa", ""]
orgSub = ["Comando da Aeronáutica", ""]

news = {}
title = {}
text = {}
data = {}
section = {}
sub = {}

# Inclusao de atos de poder executivo da seção 2
news['do2 - atos'], title['do2 - atos'], text['do2 - atos'], section['do2 - atos'], data['do2 - atos'], sub['do2 - atos'] = scrapping_executivo()

# Verificação do indice para noticias do2
if 'do2 - atos' in news.keys():
    idx = len(news['do2 - atos'])
else:
    idx = 0

for i in range(len(secao)):
    if secao[i]=='do2':
        news[f'{secao[i]}'], title[f'{secao[i]}'], text[f'{secao[i]}'], section[f'{secao[i]}'], data[f'{secao[i]}'], sub[f'{secao[i]}']  = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],idx)
    else:
        news[f'{secao[i]}'], title[f'{secao[i]}'], text[f'{secao[i]}'], section[f'{secao[i]}'], data[f'{secao[i]}'], sub[f'{secao[i]}'] = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],0)


news['do2'] = {**news["do2 - atos"],**news["do2"]}
title['do2'] = {**title["do2 - atos"],**title["do2"]}
text['do2'] = {**text["do2 - atos"],**text["do2"]}
data['do2'] = {**data["do2 - atos"],**data["do2"]}
section['do2'] = {**section["do2 - atos"],**section["do2"]}
sub['do2'] = {**sub["do2 - atos"],**sub["do2"]}

if 'do2 - atos' in news.keys():
    news.pop('do2 - atos')
    title.pop('do2 - atos')
    text.pop('do2 - atos')
    data.pop('do2 - atos')
    section.pop('do2 - atos')
    sub.pop('do2 - atos')
    
## Coleta de noticias pela IA Gemini ##
# results = gemini_analysis(titulo_dou,texto_dou) # Faz a analise a partir de IA na função vista pelo código Gemini.py

# for key, value in results.items(): # Loop para pegar todas as notícias do dicionário
#     print(f"Título: {value['title']}") # Imprime o título
#     if "response" in value: # Pega apenas a resposta gerada pela IA para printar
#         print(f"Resposta: {value['response']}") # Imprime a resposta
#         with open("noticias.txt", "a") as arquivo:
#             arquivo.write(f"Título {value['title']}.{value['response']}\n\n\n")
#     else:
#         print(f"Erro: {value['error']}") # Se der erro, ficaremos tristes


## Inserção dos dados em arquivos .txt separados ##
# Abrir o arquivo "html_draft_start.txt" e ler o conteúdo
with open("html_draft_start.txt", "r") as draftStart_file:
    html_draft_start = draftStart_file.read()

# Abrir o arquivo "html_draft_end.txt" e ler o conteúdo
with open("html_draft_end.txt", "r") as draftEnd_file:
    html_draft_end = draftEnd_file.read()

for idx, value in enumerate(news):
    if news[value] != {}:
        # Escrever o conteúdo do "html_draft_start.txt" no início do "noticias_XX.txt"
        with open(f"noticias-{value}.txt", "w") as noticias_file:
            noticias_file.write(html_draft_start)

        titulo_part = []
        body_part = []
        url_part = []
        section_part = []
        pub_date_part = []
        sub_part = []
        current_date = datetime.now().date()
        formatted_date = current_date.strftime("%B %d, %Y")
        html_template = []

        # Criando cada noticia em uma string html_template
        for i in range(0, int(len(title[value]))):
            titulo_part.append(f"{title[value][f'Noticia {i}']}.")
            body_part.append(f"{text[value][f'Noticia {i}']}")
            url_part.append(f"{news[value][f'Noticia {i}']}")
            section_part.append(f"{section[value][f'Noticia {i}']}")
            pub_date_part.append(f"{data[value][f'Noticia {i}']}")
            sub_part.append(f"{sub[value][f'Noticia {i}']}")
            html_template.append(f"""
                    <tr>
                        <td style="width: auto; vertical-align: top;">
                            <h4 style="display: inline; margin-bottom: 0;">
                                <a href="{str(url_part[i])}">
                                    <span style="color: #ed7d31; font-family: 'Arial Black'; font-size: 11pt;">{str(section_part[i][:8])}|</span>
                                    <span style="color: #002060; font-family: 'Arial Black'; font-size: 11pt;">{str(titulo_part[i])}</span>
                                </a>
                            </h4>
                            <p class="date">{str(sub_part[i])}</p>
                        </td>
                    </tr>
                    <tr>
                        <td style="vertical-align: top;">
                            <p class="date">{str(pub_date_part[i])}</p>
                            <p class="description">{str(body_part[i])}</p>
                        </td>
                    </tr>
            """)
        
        # Escrever todas as notícia no arquivo "noticias_XX.txt"
        for i in range(0, int(len(html_template))):
            with open(f"noticias-{value}.txt","a", encoding="utf-8") as arquivo:
                arquivo.write(html_template[i])

        # Escrever o conteúdo do "html_draft_end.txt" no final do "noticias.txt"
        with open(f"noticias-{value}.txt", "a") as noticias_file:
            noticias_file.write(html_draft_end)

        try:
            ## Gerando o email ##
            outlook = win32.Dispatch('Outlook.Application') # cria integração com o outlook
            email = outlook.CreateItem(0) # Cria e-mail

            # Configurações do e-mail
            with open(f"noticias-{value}.txt","r", encoding="utf-8") as file:
                file_content = file.read()

            file_content.replace("\n", "<br>")

            email.BCC = "rafael.marques@embraer.com.br; stefano.martins@embraer.com.br; guilherme.franco@embraer.com.br; leonardo.fsantos@embraer.com.br"
            # email.BCC = "guilherme.franco@embraer.com.br;"
            email.Subject = f"{str(section_part[i][:8])} - Resumo Diário Oficial - {formatted_date}"
            # email.Subject = f"{str(section_part[i][:8])} - VERSÃO DE TESTE - {formatted_date}"

            email.HTMLBody = file_content

            # Especifica a conta de envio
            email.SendUsingAccount = outlook.Session.Accounts.Item("guilherme.franco@embraer.com.br")
            email.SentOnBehalfOfName = "defensemarketstrategy@embraer.com.br"
            email.Send()
        except:
            print("Erro ao gerar o email")
    else:
        print(f'Não há noticias para os termos procurados hoje em {value}')