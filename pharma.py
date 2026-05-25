# pip install selenium webdriver-manager requests
# Caso não tenha as dependências instaladas, descomente a linha acima

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from datetime import datetime
import time
import requests

MESES = {
    1: "Janeiro", 2: "Fevereiro", 3: "Março", 4: "Abril",
    5: "Maio", 6: "Junho", 7: "Julho", 8: "Agosto",
    9: "Setembro", 10: "Outubro", 11: "Novembro", 12: "Dezembro"
}

def iniciar_driver():
    options = Options()
    # options.add_argument("--headless")  # Descomente para rodar sem abrir janela
    driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))
    return driver

def mes_do_link(href):
    """Retorna (ano, mes) numérico do link, ou None se não reconhecer."""
    for num, nome in MESES.items():
        if nome in href:
            for ano in range(2020, 2035):
                if str(ano) in href:
                    return (ano, num)
    return None

def filtrar_links_do_mes(links_xlsx):
    agora = datetime.now()
    ano_atual = agora.year
    mes_atual = agora.month

    # Mês seguinte
    if mes_atual == 12:
        prox_ano, prox_mes = ano_atual + 1, 1
    else:
        prox_ano, prox_mes = ano_atual, mes_atual + 1

    links_por_competencia = {}
    for link in links_xlsx:
        href = link.get_attribute("href")
        competencia = mes_do_link(href)
        if competencia in ((ano_atual, mes_atual), (prox_ano, prox_mes)):
            links_por_competencia.setdefault(competencia, []).append(href)

    if not links_por_competencia:
        print("Nenhum link encontrado para o mês atual ou próximo.")
        return []

    # Prioriza o mês mais avançado disponível
    competencia_escolhida = max(links_por_competencia.keys())
    ano_esc, mes_esc = competencia_escolhida

    if competencia_escolhida == (prox_ano, prox_mes):
        print(f"Mês futuro encontrado ({MESES[mes_esc]}/{ano_esc}), ignorando o atual.")
    else:
        print(f"Usando mês atual ({MESES[mes_esc]}/{ano_esc}).")

    links_escolhidos = links_por_competencia[competencia_escolhida]
    print(f"Encontrados {len(links_escolhidos)} links para baixar:")
    for href in links_escolhidos:
        print(f"  - {href}")

    return links_escolhidos

def planserv(driver):
    try:
        driver.get("https://planserv.ba.gov.br/planserv/prestador/tabelas-planserv")
        time.sleep(3)

        links_xlsx = driver.find_elements(By.XPATH, "//a[contains(@href, '.xlsx')]")

        if not links_xlsx:
            links_xlsx = driver.find_elements(By.CSS_SELECTOR, "a[href*='.xlsx']")

        if not links_xlsx:
            print("Nenhum link para arquivo Excel encontrado.")
            return

        print(f"Encontrados {len(links_xlsx)} links para arquivos Excel")

        links_do_mes = filtrar_links_do_mes(links_xlsx)

        headers = {"User-Agent": "Mozilla/5.0"}
        for url in links_do_mes:
            nome = url.split("/")[-1]
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                with open(nome, "wb") as f:
                    f.write(response.content)
                print(f"Baixado: {nome}")
            else:
                print(f"Erro ao baixar {nome}: {response.status_code}")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

if __name__ == "__main__":
    driver = iniciar_driver()
    try:
        planserv(driver)
    finally:
        driver.quit()
        print("Navegador fechado.")