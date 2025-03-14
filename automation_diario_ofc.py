import win32com.client as win32
from datetime import datetime
from Scrapping import *
import re

# Coleta das informações da web ##
secao = ["do1","do1","do2", "do3", "do3"] # Seções a analisar
search = ["","","", "aeronave",""] # # Pesquisas a analisar com base nas seções
orgPrinc = ["Ministério da Defesa", "Ministério da Defesa", "Ministério da Defesa", "", "Ministério da Defesa"]
orgSub = ["Comando da Aeronáutica","Gabinete do Ministro","Comando da Aeronáutica", "", "Comando da Aeronáutica"]


# secao = ["do3"] # Seções a analisar
# search = ["aeronave"] # # Pesquisas a analisar com base nas seções
# orgPrinc = [""]
# orgSub = [""]


news = {}
title = {}
text = {}
data = {}
section = {}
sub = {}

    
# Inclusao de atos de poder executivo da seção 1
news['do1 - atos'], title['do1 - atos'], text['do1 - atos'], section['do1 - atos'], data['do1 - atos'], sub['do1 - atos'] = scrapping_executivo("do1")

# Verificação do indice para noticias do1
if 'do1 - atos' in news.keys():
    idx1 = len(news['do1 - atos'])
else:
    idx1 = 0


# Inclusao de atos de poder executivo da seção 2
news['do2 - atos'], title['do2 - atos'], text['do2 - atos'], section['do2 - atos'], data['do2 - atos'], sub['do2 - atos'] = scrapping_executivo("do2")

# Verificação do indice para noticias do2
if 'do2 - atos' in news.keys():
    idx2 = len(news['do2 - atos'])
else:
    idx2 = 0



for i in range(len(secao)):
    if secao[i]=='do1':
        news[f'{secao[i]}'], title[f'{secao[i]}'], text[f'{secao[i]}'], section[f'{secao[i]}'], data[f'{secao[i]}'], sub[f'{secao[i]}']  = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],idx1)
    elif secao[i]=='do2':
        news[f'{secao[i]}'], title[f'{secao[i]}'], text[f'{secao[i]}'], section[f'{secao[i]}'], data[f'{secao[i]}'], sub[f'{secao[i]}']  = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],idx2)
    elif f'{secao[i]}' in news:
        news[f'{secao[i]} (FAB)'], title[f'{secao[i]} (FAB)'], text[f'{secao[i]} (FAB)'], section[f'{secao[i]} (FAB)'], data[f'{secao[i]} (FAB)'], sub[f'{secao[i]} (FAB)'] = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],len(news[f'{secao[i]}']))
    else:
        print(secao)
        news[f'{secao[i]}'], title[f'{secao[i]}'], text[f'{secao[i]}'], section[f'{secao[i]}'], data[f'{secao[i]}'], sub[f'{secao[i]}'] = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],0)


news['do1'] = {**news["do1 - atos"],**news["do1"]}
title['do1'] = {**title["do1 - atos"],**title["do1"]}
text['do1'] = {**text["do1 - atos"],**text["do1"]}
data['do1'] = {**data["do1 - atos"],**data["do1"]}
section['do1'] = {**section["do1 - atos"],**section["do1"]}
sub['do1'] = {**sub["do1 - atos"],**sub["do1"]}

news['do2'] = {**news["do2 - atos"],**news["do2"]}
title['do2'] = {**title["do2 - atos"],**title["do2"]}
text['do2'] = {**text["do2 - atos"],**text["do2"]}
data['do2'] = {**data["do2 - atos"],**data["do2"]}
section['do2'] = {**section["do2 - atos"],**section["do2"]}
sub['do2'] = {**sub["do2 - atos"],**sub["do2"]}

if 'do1 - atos' in news.keys():
    news.pop('do1 - atos')
    title.pop('do1 - atos')
    text.pop('do1 - atos')
    data.pop('do1 - atos')
    section.pop('do1 - atos')
    sub.pop('do1 - atos')
    

if 'do2 - atos' in news.keys():
    news.pop('do2 - atos')
    title.pop('do2 - atos')
    text.pop('do2 - atos')
    data.pop('do2 - atos')
    section.pop('do2 - atos')
    sub.pop('do2 - atos')

## Inserção dos dados em arquivos .txt separados ##
# Abrir o arquivo "html_draft_start_local.txt" e ler o conteúdo
with open("html_draft_start_local.txt", "r") as draftStart_file:
    html_draft_start = draftStart_file.read()

# Abrir o arquivo "html_draft_end_local.txt" e ler o conteúdo
with open("html_draft_end_local.txt", "r") as draftEnd_file:
    html_draft_end = draftEnd_file.read()

for idx, value in enumerate(news):
    if news[value] != {}:
        # Escrever o conteúdo do "html_draft_start_local.txt" no início do "noticias_XX.txt"
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
        for i, val in enumerate(title[value].keys()):
            titulo_part.append(f"{title[value][val]}.")
            url_part.append(f"{news[value][val]}")
            section_part.append(f"{section[value][val]}")
            
            pub_date_part.append(f"{data[value][val]}")
            sub_part.append(f"{sub[value][val]}")
            
            text[value][val] = text[value][val].replace("<div class=\"texto-dou\"><br> <br> <br>  <p class=\"identifica\">","")
            text[value][val] = text[value][val].replace("  <p class=\"dou-paragraph\">","")
            text[value][val] = text[value][val].replace("<p class=\"dou-paragraph\">","")
            text[value][val] = text[value][val].replace("</p>","")
            text[value][val] = text[value][val].replace("  <p class=\"assina\">","")
            text[value][val] = text[value][val].replace("</div>","")
            text[value][val] = text[value][val].replace("<br>","\n")
            text[value][val] = text[value][val].replace("<table class=\"dou-table\">","<table class=\"description-table\">")

            # Verificar se há dois <p class="identifica"> consecutivos antes de fazer a substituição
            if "\n  <p class=\"identifica\">" not in text[value][val]:
                text[value][val] = text[value][val].replace("\n  <p class=\"identifica\">", f"""</p>
                    </td>
                </tr>
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
                        <p class="description">
                """)
            text[value][val] = text[value][val].replace("<p class=\"identifica\">","")
            text[value][val] = text[value][val].replace("<p class=\"cargo\">","")
            text[value][val] = text[value][val].replace("<div class=\"texto-dou\">","")
            text[value][val] = text[value][val].replace("<p class=\"titulo\">","")
            text[value][val] = text[value][val].replace("<p class=\"data\">","")
            text[value][val] = text[value][val].replace("<p class=\"assinaPr\">","")
            text[value][val] = text[value][val].replace("<p class=\"ementa\">","")
            text[value][val] = text[value][val].replace("<p class=\"anexo\">","")

            body_part.append(f"{text[value][val]}")
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

        # Escrever o conteúdo do "html_draft_end_local.txt" no final do "noticias.txt"
        with open(f"noticias-{value}.txt", "a") as noticias_file:
            noticias_file.write(html_draft_end)

        try:
            ## Gerando o email ##
            outlook = win32.Dispatch('Outlook.Application') # cria integração com o outlook
            email = outlook.CreateItem(0) # Cria e-mail

            # Configurações do e-mail
            with open(f"noticias-{value}.txt","r", encoding="utf-8") as file:
                file_content = file.read()

            # Usar regex para encontrar e substituir o conteúdo dentro de <p class="description"></p>
            file_content = re.sub(r'<p class="description">(.*?)</p>', replace_newlines_in_description, file_content, flags=re.DOTALL)

            email.BCC = "example@dominio.com.br; "
            # print(i)
            
            if idx == 2:
                email.Subject = f"{str(section_part[i][:8])} (Aeronave) - Resumo Diário Oficial - {formatted_date}"
            elif idx == 3:
                email.Subject = f"{str(section_part[i][:8])} (FAB) - Resumo Diário Oficial - {formatted_date}"
            else:
                email.Subject = f"{str(section_part[i][:8])} - Resumo Diário Oficial - {formatted_date}"

            # email.Subject = f"{str(section_part[i][:8])} - VERSÃO DE TESTE - {formatted_date}"

            email.HTMLBody = file_content

            # Especifica a conta de envio
            email.SendUsingAccount = outlook.Session.Accounts.Item("example_my_email@dominio.com.br")
            email.SentOnBehalfOfName = "example_to@dominio.com.br"
            email.Send()
        except:
            print("Erro ao gerar o email")

    else:
        print(f'Não há noticias para os termos procurados hoje em {value}')