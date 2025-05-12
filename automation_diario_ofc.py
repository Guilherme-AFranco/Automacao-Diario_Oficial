import win32com.client as win32
from datetime import datetime
from Scrapping import *
import re

# Coleta das informações da web ##
secao = ["do1", "do1", "do1", "do2", "do2", "do3", "do3", "doe"] # Seções a analisar
search = ["", "", "", "", "",  "aeronave", "", ""] # Pesquisas a analisar com base nas seções
orgPrinc = ["Atos do Poder Executivo", "Ministério da Defesa", "Ministério da Defesa", "Atos do Poder Executivo", "Ministério da Defesa", "", "Ministério da Defesa", ""]
orgSub = ["", "Comando da Aeronáutica", "Gabinete do Ministro", "", "Comando da Aeronáutica", "", "Comando da Aeronáutica", ""]

news = {}
title = {}
text = {}
data = {}
section = {}
sub = {}

for i, value in enumerate(secao):
    if secao[i] == 'do3' and orgSub[i]=='Comando da Aeronáutica':
        subject = f'{secao[i]} (FAB)'
    else:
        subject = secao[i]
    if subject.startswith(secao[i]) and not subject.endswith('FAB') and subject in news:
        idx = len(news[subject])
        try:
            n, t, tx, s, d, sb  = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],idx)
        except:
            print('Erro na coleta')
        news[subject] = {**n,**news[subject]}
        title[subject] = {**t,**title[subject]}
        text[subject] = {**tx,**text[subject]}
        data[subject] = {**d,**data[subject]}
        section[subject] = {**s,**section[subject]}
        sub[subject] = {**sb,**sub[subject]}
    else:
        idx = 0
        try:
            news[subject], title[subject], text[subject], section[subject], data[subject], sub[subject]  = scrapping(secao[i],search[i], orgPrinc[i], orgSub[i],idx)
        except:
            print('Erro na coleta')

## Inserção dos dados em arquivos .txt separados ##
# Abrir o arquivo "html_draft_start_local.txt" e ler o conteúdo
with open("html_draft_start_local.txt", "r") as draftStart_file:
    html_draft_start = draftStart_file.read()
# Abrir o arquivo "html_draft_end_local.txt" e ler o conteúdo
with open("html_draft_end_local.txt", "r") as draftEnd_file:
    html_draft_end = draftEnd_file.read()
confirm = input('Você deseja realizar o envio? (s/n)')
if confirm.lower() == 's':
    for idx, value in enumerate(news):
        if news[value] != {}:
            with open(f"noticias-{value}.txt", "w") as noticias_file:
                noticias_file.write(html_draft_start)
            titulo_part = []
            body_part = []
            url_part = []
            section_part = []
            pub_date_part = []
            sub_part = []
            current_date = previous_business_day(datetime.today())
            formatted_date = current_date.strftime("%B %d, %Y")
            html_template = []
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
            for i in range(0, int(len(html_template))):
                with open(f"noticias-{value}.txt","a", encoding="utf-8") as arquivo:
                    arquivo.write(html_template[i])
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



                email.BCC = "example1@domain.com.br; example2@domain.com.br"



                if value == 'do3':
                    email.Subject = f"{str(section_part[i][:8])} (Aeronave) - Resumo Diário Oficial - {formatted_date}"
                elif value == 'do3 (FAB)':
                    email.Subject = f"{str(section_part[i][:8])} (FAB) - Resumo Diário Oficial - {formatted_date}"
                elif value == 'doe':
                    email.Subject = f"{str(section_part[7][:7])+str(section_part[7][11:16])} - Resumo Diário Oficial - {formatted_date}"
                else:
                    email.Subject = f"{str(section_part[i][:8])} - Resumo Diário Oficial - {formatted_date}"
                email.HTMLBody = file_content
                # Especifica a conta de envio
                email.SendUsingAccount = outlook.Session.Accounts.Item("example@domain.com.br")
                email.SentOnBehalfOfName = "example@domain.com.br"
                email.Send()
            except:
                print("Erro ao gerar o email")
        else:
            print(f'Não há noticias para os termos procurados hoje em (({value})) {secao[idx]}-{orgPrinc[idx]}-{orgSub[idx]}-{search[idx]}')
else:
    print("Envio de e-mails cancelado pelo usuário.")