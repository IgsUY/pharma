#pip install selenium #Caso não tenha o Selenium instalado, descomente esta linha para instalar

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import requests

# Iniciar o navegador
driver = webdriver.Firefox()  # Certifique-se de ter o Firefox instalado e no PATH

try:

def planserv():
    # Acessar o site da farmácia - Planserv
    driver.get("https://planserv.ba.gov.br/planserv/prestador/tabelas-planserv")

    # Encontra um elemento xlsx a ser encontrado:
    elemento_xlsx = driver.find_element(By.XPATH, "//a[contains(@href, 'xlsx')]")

    if not elemento_xlsx:
        elemento_xlsx = driver.find_element(By.CSS_SELECTOR, "a[href*='xlsx']") 
        print(f"Encontrados {len(links_xlsx)} links para arquivos Excel")
    
planserv()
except Exception as e:
    print(f"Ocorreu um erro: {e}")
finally:
    # Fechar o navegador
    driver.quit()