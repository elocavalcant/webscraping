
# Módulo para controlar o navegador // simula o navegador com o chrome driver
from selenium import webdriver

# Localizador de elemntos // com ele pedimos pra encontrar classes, ids (elementos)
from selenium.webdriver.common.by import By

# Serviço para configurar o caminho do executável chromedriver //
from selenium.webdriver.chrome.service import Service

# classe que permite executar ações avançadas (o mover do mouse, clique/arraste)
from selenium.webdriver.common.action_chains import ActionChains

# classe que espera de forma explicita até que uma condição seja satisfeita (que um elemento apareça) // pede pro comando aguradar alguns segundos
from selenium.webdriver.support.ui import WebDriverWait

# condições esperadas usadas com o webDriverWait
from selenium.webdriver.support import expected_conditions as ec

#trabalhar com dados em tabelas/dataframe
import pandas as pd

#Uso de funções relacionadas ao tempo
import time

# uso de tratamento de exceção
from selenium.common.exceptions import TimeoutException

#definir o caminho do chromedriver
chrome_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

# configuração do webdriver
service = Service(chrome_driver_path) #navegador controlado pelo selenium
options = webdriver.ChromeOptions() #configurar as opções do navegador 
options.add_argument("--disable-gpu") #evita possiveis erros graficos 
options.add_argument("--window-size=1920,1080") #define uma resolução fixa



# inicialização do webdriver

driver = webdriver.Chrome(service=service, options=options)

# URL incial

url_base = "https://www.kabum.com.br/espaco-gamer/cadeiras-gamer"
driver.get(url_base)

time.sleep(5) #aguarda 5 segundos para garantir que a pagina carregue

# criar um dicionario vazio para armazenar as marcas e preços das cadeiras
dic_produtos = {"marca":[],"preco":[]}

# vamos iniciar na pagina 1 e incrementamos a cada troca de pagina
pagina = 1

while True:
    print(f"\n Coletando dados da página {pagina}...")

    try:

        #WebDriverWait(driver,10) = cria uma espera de até 10 seg
        #until... faz com que o código espere até que a condição seja verdadeira 
        #ec.presence_of_all_elements_located verifica se todos os elementos productCard estão acessiveis
        #By.CLASS_NAME,"productCard" indica que a busca sera feita atraves da clsse css
        WebDriverWait(driver,10).until(
            ec.presence_of_all_elements_located((By.CLASS_NAME,"productCard"))
        )
        print("Elementos encontrados com sucesso!")
    except TimeoutException:
        print("Tempo de espera excedido!")

    produtos = driver.find_elements(By.CLASS_NAME,"productCard")

    for produto in produtos:
        try:
            nome = produto.find_element(By.CLASS_NAME,"nameCard").text.strip()
            preco = produto.find_element(By.CLASS_NAME,"priceCard").text.strip()

            print(f"{nome} - {preco}")

            dic_produtos["marca"].append(nome)
            dic_produtos["preco"].append(preco)

        except Exception:
            print("Erro ao coletar dados:", Exception)

# ENCONTRAR BOTAO DA PROXIMA PAGINA
    try:
        # ENCONTRAR O ELELMENTO/BOTÃO
        botao_proximo = WebDriverWait(driver, 5).until(
            ec.element_to_be_clickable((By.CLASS_NAME, "nextLink"))
        )

        if botao_proximo:
            driver.execute_script("arguments[0].scrollIntoView();",botao_proximo)
            time.sleep(1)

            #CLICAR NO BOTÃO - execute_script simula navegação com o mouse - click é para clicar
            driver.execute_script("arguments[0].click();", botao_proximo)
            print(f"Indo para a página {pagina}")
            pagina+=1
            time.sleep(5)

        else:
            print("Você chegou na última página!")
            break

    except Exception as e:
        print("Erro ao tentar avançar para a próxima página")
        break

# FECHA O NAVEGADOR 
driver.quit()

df = pd.DataFrame(dic_produtos)
df.to_excel("cadeiras.xlsx", index=False)

print(f"Arquivo cadeiras salvo com sucesso! ({len(df)}) produtos capturados!")



