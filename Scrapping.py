from selenium import webdriver
from selenium.webdriver.chrome.service import Service 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC 
import time

# from Gemini import *

# Função para substituir \n por <br> dentro de <p class="description"></p>
def replace_newlines_in_description(match):
    content = match.group(1)
    content = content.replace("\n", "<br>")
    return f'<p class="description">{content}</p>'

def scrapping(secao,search,orgPrinc,orgSub,index):
    service = Service(executable_path="chromedriver.exe") # Descomentar para uso no pc do Léo
    # service = Service(executable_path="E:\Backup_PC\Aplicativos\ChromeDrive\WebDriver\chromedriver.exe") # Descomentar para uso no pc do Gui
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()

    time.sleep(2)

    driver.get("https://in.gov.br/leiturajornal")

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

    dia = driver.find_element(By.ID, "dia") # Voltar para "dia" dps (tinha poucas noticias com parametro "dia")
    dia.click()

    WebDriverWait(driver, 2).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "form-control"))
    )


    search_area = driver.find_element(By.CLASS_NAME, "form-control")
    search_area.clear()
    search_area.send_keys(search + Keys.ENTER)
    time.sleep(5)

    if orgPrinc != "":
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "orgPrinAction"))
        )

        org_prin = driver.find_element(By.ID, "orgPrinAction")
        org_prin.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "dropdown-item"))
        )

        org_principal = driver.find_element(By.XPATH, f"//a[contains(text(), '{orgPrinc}')]")
        org_principal.click()

        time.sleep(2)

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
            driver.quit()
            return {}, {}, {}, {}, {}, {}


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

            for _, noticia in enumerate(noticias):
                try:
                    link_element = noticia.find_element(By.TAG_NAME, "a") # Encontrar link
                    if secao == 'do3':
                        noticia_url[f'Noticia {i} (Aeronave)'] = link_element.get_attribute("href") # Coletar o link

                        driver.execute_script("window.open(arguments[0]);", noticia_url[f'Noticia {i} (Aeronave)']) # Abrir em nova aba
                        driver.switch_to.window(driver.window_handles[1]) # Ir para a nova aba

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "dou-paragraph"))
                        ) # Esperar o texto da notícia carregar

                        titulo_dou[f'Noticia {i} (Aeronave)'] = driver.find_element(By.CLASS_NAME, "identifica").text # Coletar titulo
                        texto_dou[f'Noticia {i} (Aeronave)'] = driver.find_element(By.CLASS_NAME, "texto-dou").get_attribute('outerHTML') # Coletar notícia
                        data_dou[f'Noticia {i} (Aeronave)'] = driver.find_element(By.CLASS_NAME, "publicado-dou-data").text # Coletar data
                        secao_dou[f'Noticia {i} (Aeronave)'] = driver.find_element(By.CLASS_NAME, "secao-dou").text # Coletar secao

                        sub_dou[f'Noticia {i} (Aeronave)'] = driver.find_element(By.CLASS_NAME, "orgao-dou-data").text # Coletar orgao

                        texto_dou[f'Noticia {i} (Aeronave)'] = texto_dou[f'Noticia {i} (Aeronave)'].replace('Objeto:', '<br><b>Objeto:</b>')
                        texto_dou[f'Noticia {i} (Aeronave)'] = texto_dou[f'Noticia {i} (Aeronave)'].replace('Contratante:', '<br><b>Contratante:</b>')
                        texto_dou[f'Noticia {i} (Aeronave)'] = texto_dou[f'Noticia {i} (Aeronave)'].replace('Contratado:', '<br><b>Contratado:</b>')
                        texto_dou[f'Noticia {i} (Aeronave)'] = texto_dou[f'Noticia {i} (Aeronave)'].replace('\n', '<br>')
                    elif secao == 'do3_fab':
                        noticia_url[f'Noticia {i} (FAB)'] = link_element.get_attribute("href") # Coletar o link

                        driver.execute_script("window.open(arguments[0]);", noticia_url[f'Noticia {i} (FAB)']) # Abrir em nova aba
                        driver.switch_to.window(driver.window_handles[1]) # Ir para a nova aba

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "dou-paragraph"))
                        ) # Esperar o texto da notícia carregar

                        titulo_dou[f'Noticia {i} (FAB)'] = driver.find_element(By.CLASS_NAME, "identifica").text # Coletar titulo
                        texto_dou[f'Noticia {i} (FAB)'] = driver.find_element(By.CLASS_NAME, "texto-dou").get_attribute('outerHTML') # Coletar notícia
                        data_dou[f'Noticia {i} (FAB)'] = driver.find_element(By.CLASS_NAME, "publicado-dou-data").text # Coletar data
                        secao_dou[f'Noticia {i} (FAB)'] = driver.find_element(By.CLASS_NAME, "secao-dou").text # Coletar secao

                        sub_dou[f'Noticia {i} (FAB)'] = driver.find_element(By.CLASS_NAME, "orgao-dou-data").text # Coletar orgao

                        texto_dou[f'Noticia {i} (FAB)'] = texto_dou[f'Noticia {i} (FAB)'].replace('Objeto:', '\n<b>Objeto:</b>')
                        texto_dou[f'Noticia {i} (FAB)'] = texto_dou[f'Noticia {i} (FAB)'].replace('Contratante:', '\n<b>Contratante:</b>')
                        texto_dou[f'Noticia {i} (FAB)'] = texto_dou[f'Noticia {i} (FAB)'].replace('Contratado:', '\n<b>Contratado:</b>')
                        texto_dou[f'Noticia {i} (FAB)'] = texto_dou[f'Noticia {i} (FAB)'].replace('\n', '<br>')
                    else:
                        noticia_url[f'Noticia {i}'] = link_element.get_attribute("href") # Coletar o link

                        driver.execute_script("window.open(arguments[0]);", noticia_url[f'Noticia {i}']) # Abrir em nova aba
                        driver.switch_to.window(driver.window_handles[1]) # Ir para a nova aba

                        WebDriverWait(driver, 10).until(
                            EC.presence_of_all_elements_located((By.CLASS_NAME, "dou-paragraph"))
                        ) # Esperar o texto da notícia carregar

                        titulo_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "identifica").text # Coletar titulo
                        texto_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "texto-dou").get_attribute('outerHTML') # Coletar notícia
                        data_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "publicado-dou-data").text # Coletar data
                        secao_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "secao-dou").text # Coletar secao

                        sub_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "orgao-dou-data").text # Coletar orgao

                        texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('Objeto:', '\n<b>Objeto:</b>')
                        texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('Contratante:', '\n<b>Contratante:</b>')
                        texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('Contratado:', '\n<b>Contratado:</b>')
                        texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('\n', '<br>')

                    print(f'Coletou Noticia {i}, seção {secao}')

                    driver.close() # Fechar a aba adicional
                    driver.switch_to.window(driver.window_handles[0])  # Voltar à aba principal

                    noticias = driver.find_elements(By.CLASS_NAME, "resultados-wrapper") # Atualizar a lista das notícias na pagina
                    i += 1
                except Exception as e:
                    print(f"Erro ao processar a notícia {i+1}: {e}") # Se der erro, ele avisa e ficamos tristes

            nextPage = driver.find_element(By.CLASS_NAME, "icon-caret-right") # Verifica se existe próxima tela
            nextPage.click()  # Vai para a próxima tela
            print("Foi pra proxima pagina")
            time.sleep(2)
            iterations += 1
        except:
            break # Sai do loop se não existir próxima tela

    driver.quit() # Sai da pagina da web


    # # Coleta de noticias pela IA Gemini ##
    # results = gemini_analysis(titulo_dou,texto_dou) # Faz a analise a partir de IA na função vista pelo código Gemini.py
    # texto_IA = {}

    # for i, value in results.items(): # Loop para pegar todas as notícias do dicionário
    #     if "response" in value: # Pega apenas a resposta gerada pela IA para printar
    #         print(f"Resposta: {value['response']}") # Imprime a resposta
    #         texto_IA[f'Noticia {i}'] = value['response']
    #     else:
    #         print(f"Erro: {value['error']}") # Se der erro, ficaremos tristes
    #         texto_IA[f'Noticia {i}'] = 'Erro: Contate o administrador do programa.'

    # for key, value in results.items(): # Loop para pegar todas as notícias do dicionário
    #     print(f"Título: {value['title']}") # Imprime o título
    #     if "response" in value: # Pega apenas a resposta gerada pela IA para printar
    #         print(f"Resposta: {value['response']}") # Imprime a resposta
    #         with open("noticias.txt", "a") as arquivo:
    #             arquivo.write(f"Título {value['title']}.{value['response']}\n\n\n")
    #     else:
    #         print(f"Erro: {value['error']}") # Se der erro, ficaremos tristes


    return noticia_url, titulo_dou, texto_dou, secao_dou, data_dou, sub_dou #, texto_IA

def scrapping_executivo(secao):
    service = Service(executable_path="chromedriver.exe") # Descomentar para uso no pc do Léo
    # service = Service(executable_path="E:\Backup_PC\Aplicativos\ChromeDrive\WebDriver\chromedriver.exe") # Descomentar para uso no pc do Gui
    driver = webdriver.Chrome(service=service)
    driver.maximize_window()
    time.sleep(2)

    driver.get("https://in.gov.br/leiturajornal")
    time.sleep(2)



    if secao == "do1":
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'button secao_1_hover')]")))
        secao_n = driver.find_element(By.XPATH, "//a[contains(@class, 'button secao_1_hover')]")
        
    elif secao == "do2":
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'button secao_2_hover')]")))
        secao_n = driver.find_element(By.XPATH, "//a[contains(@class, 'button secao_2_hover')]")
    else:
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@class, 'button secao_3_hover')]")))
        secao_n = driver.find_element(By.XPATH, "//a[contains(@class, 'button secao_3_hover')]")
    secao_n.click()
    time.sleep (1)

    WebDriverWait(driver, 12).until(
        EC.presence_of_element_located((By.ID, "slcOrgs"))
    )

    try:
        select_element = Select(driver.find_element(By.ID, "slcOrgs"))
        # select_element.select_by_visible_text("Presidência da República")  # Exemplo de seleção
        select_element.select_by_visible_text("Atos do Poder Executivo")  # Exemplo de seleção
    except:
        driver.quit()
        return {}, {}, {}, {}, {}, {}
    

    ## Obtendo as noticias ##
    noticia_url = {} # Dicionario para colocar a url da notícia
    titulo_dou = {} # Dicionario para colocar o titulo da notícia
    texto_dou = {} # Dicionario para texto da noticia
    secao_dou ={} # Dicionario para numero da seção
    data_dou = {}# Dicionario para data de publicação
    sub_dou = {}

    i = 0
    iterations = 0

    while iterations < 1:
        try:
            noticias = driver.find_elements(By.CLASS_NAME, "resultados-wrapper") # Obtem as classes de noticias existentes na aba

            for _, noticia in enumerate(noticias):
                try:
                    link_element = noticia.find_element(By.TAG_NAME, "a") # Encontrar link
                    noticia_url[f'Noticia {i}'] = link_element.get_attribute("href") # Coletar o link

                    driver.execute_script("window.open(arguments[0]);", noticia_url[f'Noticia {i}']) # Abrir em nova aba
                    driver.switch_to.window(driver.window_handles[1]) # Ir para a nova aba

                    WebDriverWait(driver, 10).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, "dou-paragraph"))
                    ) # Esperar o texto da notícia carregar

                    titulo_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "identifica").text # Coletar titulo
                    # texto_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "texto-dou").text # Coletar notícia
                    texto_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "texto-dou").get_attribute('outerHTML') # Coletar notícia
                    data_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "publicado-dou-data").text # Coletar data
                    secao_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "secao-dou").text # Coletar secao
                    sub_dou[f'Noticia {i}'] = driver.find_element(By.CLASS_NAME, "orgao-dou-data").text # Coletar orgão
                    texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('Objeto:', '\n<b>Objeto:</b>')
                    texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('Contratante:', '\n<b>Contratante:</b>')
                    texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('Contratado:', '\n<b>Contratado:</b>')
                    texto_dou[f'Noticia {i}'] = texto_dou[f'Noticia {i}'].replace('\n', '<br>')
                    
                    driver.close() # Fechar a aba adicional
                    driver.switch_to.window(driver.window_handles[0])  # Voltar à aba principal

                    noticias = driver.find_elements(By.CLASS_NAME, "resultados-wrapper") # Atualizar a lista das notícias na pagina
                    i += 1
                except Exception as e:
                    print(f"Erro ao processar a notícia {i+1}: {e}") # Se der erro, ele avisa e ficamos tristes

            nextPage = driver.find_element(By.XPATH, "//span[contains(@class, 'pagination-button') and contains(text(), 'Próximo »')]")
            nextPage.click()  # Vai para a próxima tela
            print("Foi pra proxima pagina")
            time.sleep(2)
            iterations += 1
        except:
            break # Sai do loop se não existir próxima tela

    driver.quit() # Sai da pagina da web
    
    return noticia_url, titulo_dou, texto_dou, secao_dou, data_dou, sub_dou #, texto_IA
