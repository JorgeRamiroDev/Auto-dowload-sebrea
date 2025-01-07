from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import ElementClickInterceptedException, NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import urllib.parse

# Configurações
URL_ALVO = 'https://datasebrae.com.br/fichas-tecnicas-sebraetec/'  # Substitua pela URL real
DIRETORIO_DOWNLOAD = 'downloads_pdfs'  # Diretório onde os PDFs serão salvos

# Cria o diretório de download se não existir
if not os.path.exists(DIRETORIO_DOWNLOAD):
    os.makedirs(DIRETORIO_DOWNLOAD)

# Configura o WebDriver (exemplo com Chrome)
# Substitua o caminho abaixo pelo local onde você extraiu o chromedriver
servico = Service('chromedriver.exe')  # Use barras / ou duplas barras \\
options = webdriver.ChromeOptions()

# Configurações para download automático
prefs = {
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # Evita que o PDF abra no navegador
}
options.add_experimental_option("prefs", prefs)

driver = webdriver.Chrome(service=servico, options=options)

try:
    # Navega até a página alvo
    driver.get(URL_ALVO)

    wait = WebDriverWait(driver, 10)

    # Seleciona o estado "Piauí" no dropdown
    def selecionar_estado():
        try:
            dropdown = wait.until(EC.presence_of_element_located((By.ID, 'dropdown-processos')))
            select = Select(dropdown)
            select.select_by_value('pi')  # Seleciona o estado com value="pi"
            print("Estado 'Piauí' selecionado com sucesso.")
            time.sleep(2)  # Aguarda carregamento dos dados específicos do estado
        except NoSuchElementException:
            print("Dropdown não encontrado.")
        except TimeoutException:
            print("Timeout ao tentar selecionar o estado.")

    selecionar_estado()

    # Função para expandir todas as seções de acordion
    def expandir_todas_as_secoes():
        try:
            toggles = driver.find_elements(By.CSS_SELECTOR, '.omsc-toggle-title')
            for toggle in toggles:
                try:
                    # Verifica se o elemento está visível e clicável
                    
                    if toggle.is_displayed() and toggle.is_enabled():
                        toggle.click()
                        time.sleep(0.5)  # Pequena pausa para permitir o carregamento
                        print("Elemento clicado com sucesso.")
                    else:
                        print("Elemento não está interativo.")
                except ElementClickInterceptedException:
                    print("Elemento não pode ser clicado diretamente (interceptado).")
                except Exception as e:
                    print(f"Erro ao clicar no elemento: {e}")
        except NoSuchElementException:
            print("Nenhuma seção de acordion encontrada.")

    # Expande todas as seções
    expandir_todas_as_secoes()

    # Aguarda até que todos os PDFs estejam visíveis
    time.sleep(2)  # Ajuste conforme necessário

    # Coleta todos os links de PDF
    links_pdf = driver.find_elements(By.XPATH, "//a[contains(@href, '.pdf')]")

    print(f"Total de PDFs encontrados: {len(links_pdf)}")

    # Extrai os URLs dos PDFs
    urls_pdfs = [link.get_attribute('href') for link in links_pdf]

    # Remove possíveis duplicatas
    urls_pdfs = list(set(urls_pdfs))

    print(f"Total de PDFs únicos para baixar: {len(urls_pdfs)}")

    # Função para baixar PDFs
    def baixar_pdf(url, diretorio):
        try:
            resposta = requests.get(url, stream=True)
            if resposta.status_code == 200:
                # Decodifica o nome do arquivo para UTF-8 e mantém caracteres especiais
                nome_arquivo = urllib.parse.unquote(url.split('/')[-1])
                caminho_arquivo = os.path.join(diretorio, nome_arquivo)
                with open(caminho_arquivo, 'wb') as f:
                    for chunk in resposta.iter_content(1024):
                        f.write(chunk)
                print(f"Baixado: {nome_arquivo}")
            else:
                print(f"Falha ao baixar {url}: Status {resposta.status_code}")
        except Exception as e:
            print(f"Erro ao baixar {url}: {e}")

    # Baixa todos os PDFs
    for url_pdf in urls_pdfs:
        baixar_pdf(url_pdf, DIRETORIO_DOWNLOAD)

    print("Download de todos os PDFs concluído.")

finally:
    # Fecha o navegador
    driver.quit()
