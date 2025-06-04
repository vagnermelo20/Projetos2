from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time


service = Service(ChromeDriverManager().install())
nav = webdriver.Chrome(service=service)
nav.get("https://web.whatsapp.com")
time.sleep(30)

mensagem = "Teste"

lista_contatos = ["+55 88 9822-4668","+55 81 8980-8485","+55 87 9934-9066",]

novo_contato = ["+55 87 9934-9066"]

if novo_contato[0] not in lista_contatos:
    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[3]/header/header/div/span/div/div[1]').click()
    time.sleep(2)
    print("clicar em nova conversa")
    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/div[1]/div[2]/div').click()
    time.sleep(2)
    print("clicar em novo contato")
    lista_contatos.append(novo_contato[0])
    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div/div/div[1]/div[2]/div/div[2]/div').click()
    print("clicar em adicionar nome")
    time.sleep(2)
    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div/div/div[1]/div[2]/div/div[2]/div/div/div').send_keys("Davi")
    time.sleep(2)
    print("Adicionar o nome")
    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div/div/div[3]/div[2]/div/div/div[2]/div[2]/div/div/form/input').click()
    print("clicar número de telefone")
    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div/div/div[3]/div[2]/div/div/div[2]/div[2]/div/div/form/input').send_keys("87 9934-9066")
    print("colocar o número de telefone")
    time.sleep(2)
    novo_contato.pop(0)

    nav.find_element('xpath', '//*[@id="app"]/div/div[3]/div/div[2]/div[1]/span/div/span/div/div[2]/span/div/span').click()
    time.sleep(2)
    
for x in lista_contatos:
    print(x)

nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p').click()
nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p').send_keys("+55 88 9822-4668")
nav.find_element('xpath', '//*[@id="side"]/div[1]/div/div[2]/div/div/div[1]/p').send_keys(Keys.ENTER)
time.sleep(2)

nav.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]/p').send_keys(mensagem)
nav.find_element('xpath', '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[3]/div[1]/p').send_keys(Keys.ENTER)
time.sleep(2)


qtd_contatos = len(lista_contatos)

if qtd_contatos % 5 == 0:
    qtd_blocos = qtd_contatos/5
else:
    qtd_blocos = int(qtd_contatos/5) + 1


for i in range(qtd_blocos):
    i_inicial = i * 5
    i_final = (i+1)*5 
    lista_enviar = lista_contatos[i_inicial:i_final]

    lista_elementos = nav.find_elements('class name', '_amk5')
    for item in lista_elementos:
        mensagem = mensagem.replace("\n","")
        texto = item.text.replace("\n","")
        if mensagem in texto:
            elemento = item

    ActionChains(nav).move_to_element(elemento).perform()
    elemento.find_element('class name', '_ahkm').click()
    print("click")
    time.sleep(2)
    nav.find_element('xpath', '//*[@id="app"]/div/span[6]/div/ul/div/div[5]/li/div').click()
    print("click")
    nav.find_element('xpath', '//*[@id="main"]/span/div/button[2]').click()
    print("click")

    time.sleep(4)

    for nome in lista_enviar:
        nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/p').send_keys(nome)
        time.sleep(1)
        print("1")

        nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/p').send_keys(Keys.ENTER)
        time.sleep(1)
        print("2")
        nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/div[1]/div/div[2]/div/div/div/p').send_keys(Keys.BACKSPACE)
        time.sleep(3)
    nav.find_element('xpath', '//*[@id="app"]/div/span[2]/div/div/div/div/div/div/div/span/div/div/div/span').click()
    time.sleep(2)
    print("4")
    time.sleep(4)