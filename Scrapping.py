from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
import time
from datetime import datetime, timedelta

def previous_business_day(date):
    if date.weekday() == 0:
        return date - timedelta(days=3)
    else:
        return date - timedelta(days=1)
    
def replace_newlines_in_description(match):
    content = match.group(1)
    content = content.replace("\n", "<br>")
    return f'<p class="description">{content}</p>'

def scrapping(secao,search,orgPrinc,orgSub,index,secaoExtra):
    service = Service(executable_path="chromedriver.exe") # Descomentar para uso no pc do Léo
    # service = Service(executable_path="E:\Backup_PC\Aplicativos\ChromeDrive\WebDriver\chromedriver.exe") # Caso o cromedriver esteja em um diretório diferente dos arquivos, inclua-o aqui e comente a linha de cima.
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    time.sleep(2)
    try:
        driver.get("https://www.in.gov.br/leiturajornal")
    except Exception as e:
        print('Erro ao abrir o DOI',e)
        time.sleep(5)
    time.sleep(2)
    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.ID, "toggle-search-advanced"))
    )
    advance_search = driver.find_element(By.ID, "toggle-search-advanced")
    advance_search.click()
    time.sleep (1)
    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.ID, secao))
    )
    secao_n = driver.find_element(By.ID, secao)
    secao_n.click()
    time.sleep(2)
    ontem = previous_business_day(datetime.today())
    data_formatada = ontem.strftime("%d/%m/%Y")


    # data_formatada = "DD/MM/AAAA" # Descomentar - tirar o # no inicio - e modificar manualmente quando houver feriados (inclua a data anterior ao feriado - lembre-se: o DO não publica na maioria dos feriados, mas a automação acontece para coletar do dia útil anterior, então esse ajuste te ajuda a coletar o dia anterior ao feriado
    
    
    dia = driver.find_element(By.ID, "personalizado")
    dia.click()
    data_inicio = driver.find_element(By.ID, "data-inicio")
    data_inicio.click()
    data_inicio.send_keys(Keys.CONTROL + "a")
    data_inicio.send_keys(data_formatada)
    data_inicio.send_keys(Keys.RETURN)
    data_fim = driver.find_element(By.ID, "data-fim")
    data_fim.click()
    data_fim.send_keys(Keys.CONTROL + "a")
    data_fim.send_keys(data_formatada)
    data_fim.send_keys(Keys.RETURN)
    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "form-control"))
    )
    search_area = driver.find_element(By.CLASS_NAME, "form-control")
    search_area.clear()
    if isinstance(search,str):
        search_area.send_keys(search + Keys.ENTER)
    elif all(element == search[0] for element in search):
        search_area.send_keys(search[0] + Keys.ENTER)
    else:
        print(f'Erro: Todas as palavras-chave na lista {secao} devem ser iguais.')
        time.sleep(300)
        return None
    time.sleep(5)
    if not secaoExtra:
        if orgPrinc != "":
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "orgPrinAction"))
            )
            org_prin = driver.find_element(By.ID, "orgPrinAction")
            org_prin.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dropdown-item"))
            )
            try:
                org_principal = driver.find_element(By.XPATH, f"//a[contains(text(), '{orgPrinc}')]")
                org_principal.click()
            except:
                print(f'Não há busca para {secao}-{orgPrinc}')
                driver.quit()
                return {},{},{},{},{},{},data_formatada
            time.sleep(2)
        if orgSub!='':
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "orgSubAction"))
            )
            org_Sub = driver.find_element(By.ID, "orgSubAction")
            org_Sub.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "dropdown-item"))
            )
            try:
                org_Subordinada = driver.find_element(By.XPATH, f"//a[contains(text(), '{orgSub}')]")
                org_Subordinada.click()
            except:
                print(f'Não há busca para {secao}-{orgPrinc}-{orgSub}')
                driver.quit()
                return {},{},{},{},{},{},data_formatada
        time.sleep(5)
    ## Obtendo as noticias ##
    noticia_url = {} # Dicionario para colocar a url da notícia
    titulo_dou = {} # Dicionario para colocar o titulo da notícia
    texto_dou = {} # Dicionario para texto da noticia
    secao_dou ={} # Dicionario para numero da seção
    data_dou = {}# Dicionario para data de publicação
    sub_dou = {}
    i = index
    iterations = 0
    while iterations < 5:
        try:
            noticias = driver.find_elements(By.CLASS_NAME, "resultados-wrapper") # Obtem as classes de noticias existentes na aba
            erroIdx = 0
            for noticia in noticias:
                while erroIdx<5:
                    try:
                        if secaoExtra:
                            breadcrumb = WebDriverWait(noticia, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "dou-hierarquia.breadcrumb")))
                            secaoAtual = breadcrumb.find_element(By.CLASS_NAME, "secao-marker").text
                            orgPrincAtual = breadcrumb.find_element(By.CLASS_NAME, "hierarchy-item-marker").text
                            orgSubAtual = breadcrumb.find_element(By.CLASS_NAME, "hierarchy-item-marker").text
                            if isinstance(secaoExtra,list):
                                for idxExtra in range(len(secaoExtra)):
                                    if secaoExtra[idxExtra] in secaoAtual and orgPrinc[idxExtra] in orgPrincAtual and orgSub[idxExtra] in orgSubAtual:
                                        link_element = noticia.find_element(By.TAG_NAME, "a") # Encontrar link
                                        break
                                    else:
                                        link_element = None
                                break
                            else:
                                if secaoExtra in secaoAtual and orgPrinc in orgPrincAtual and orgSub in orgSubAtual:
                                    link_element = noticia.find_element(By.TAG_NAME, "a") # Encontrar link
                                    break
                                else:
                                    link_element = None
                                    break
                        else:
                            link_element = noticia.find_element(By.TAG_NAME, "a") # Encontrar link
                            erroIdx = 0
                            break
                    except Exception as e:
                        erroIdx += 1
                        print(f"Erro ao coletar link da notícia. Tentando novamente.")
                        time.sleep(3)
                if erroIdx == 6:
                    print(f'Não foi possível corrigir o erro.\n{e}')
                    time.sleep(300)
                    return None
                if link_element:
                    if secao == 'do3' and search!='':
                        subject = f'{secao} ({search})'
                    elif secao == 'do3' and orgSub=='Comando da Aeronáutica':
                        subject = f' {secao} (FAB)'
                    else:
                        subject = f' {secao}'
                    while erroIdx<5:
                        try:
                            noticia_url[f'Noticia {i}{subject}'] = link_element.get_attribute("href") # Coletar o link
                            driver.execute_script("window.open(arguments[0]);", noticia_url[f'Noticia {i}{subject}']) # Abrir em nova aba
                            driver.switch_to.window(driver.window_handles[1]) # Ir para a nova aba
                            break
                        except:
                            erroIdx += 1
                            print(f"Erro ao abrir link da notícia em nova aba. Tentando novamente.")
                            time.sleep(3)
                    if erroIdx == 6:
                        print('Não foi possível corrigir o erro.')
                        time.sleep(300)
                        return None
                    try:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "dou-paragraph"))
                        ) # Esperar o texto da notícia carregar
                    except Exception as e:
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "identifica"))
                        ) # Esperar o texto da notícia carregar
                        print('A página não carregou corretamente', e)
                        time.sleep(30)
                    titulo_dou[f'Noticia {i}{subject}'] = driver.find_element(By.CLASS_NAME, "identifica").text # Coletar titulo
                    texto_dou[f'Noticia {i}{subject}'] = driver.find_element(By.CLASS_NAME, "texto-dou").get_attribute('outerHTML') # Coletar notícia
                    data_dou[f'Noticia {i}{subject}'] = driver.find_element(By.CLASS_NAME, "publicado-dou-data").text # Coletar data
                    secao_dou[f'Noticia {i}{subject}'] = driver.find_element(By.CLASS_NAME, "secao-dou").text # Coletar secao
                    sub_dou[f'Noticia {i}{subject}'] = driver.find_element(By.CLASS_NAME, "orgao-dou-data").text # Coletar orgao
                    texto_dou[f'Noticia {i}{subject}'] = texto_dou[f'Noticia {i}{subject}'].replace('Objeto:', '<br><b>Objeto:</b>')
                    texto_dou[f'Noticia {i}{subject}'] = texto_dou[f'Noticia {i}{subject}'].replace('Contratante:', '<br><b>Contratante:</b>')
                    texto_dou[f'Noticia {i}{subject}'] = texto_dou[f'Noticia {i}{subject}'].replace('Contratado:', '<br><b>Contratado:</b>')
                    texto_dou[f'Noticia {i}{subject}'] = texto_dou[f'Noticia {i}{subject}'].replace('\n', '<br>')

                    print(f'Coletou Noticia {i}, {secao}-{orgPrinc}-{orgSub}-{search}')

                    driver.close() # Fechar a aba adicional
                    driver.switch_to.window(driver.window_handles[0])  # Voltar à aba principal

                    noticias = driver.find_elements(By.CLASS_NAME, "resultados-wrapper") # Atualizar a lista das notícias na pagina
                    i += 1
            nextPage = driver.find_element(By.CLASS_NAME, "icon-caret-right") # Verifica se existe próxima tela
            nextPage.click()  # Vai para a próxima tela
            print("Foi para a práxima página")
            time.sleep(2)
            iterations += 1
        except:
            print(f'Não há mais páginas para carregar na pesquisa {secao}-{orgPrinc}-{orgSub}-{search}')
            break # Sai do loop se não existir próxima tela
    driver.quit() # Sai da pagina da web
    return noticia_url, titulo_dou, texto_dou, secao_dou, data_dou, sub_dou, data_formatada