from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from home.models import Usuario
from django.contrib.auth.hashers import make_password

# class Test1_Criar_Curso(LiveServerTestCase):

#     def setUp(self):
#         # Cria um usuário no seu modelo customizado
#         self.usuario = Usuario.objects.create(
#             Username='testeuser',
#             E_mail='teste@email.com',
#             Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
#             Tipos_conta='Admin'
#         )

#         self.driver = webdriver.Chrome()


#     def tearDown(self):
#         self.driver.quit()

#     def test1_Criar_curso(self):
#         driver = self.driver  # ✅ Aqui está o que você queria

#         driver.get(self.live_server_url)

#         driver.find_element(By.LINK_TEXT, "Login").click()

#         WebDriverWait(driver, 10).until(
#             EC.presence_of_element_located((By.ID, "campo_email"))
#         )

#         driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
#         time.sleep(3)  # Espera para garantir que o campo esteja preenchido
#         driver.find_element(By.ID, "campo_senha").send_keys("123")
#         time.sleep(3)  # Espera para garantir que o campo esteja preenchido

#         driver.find_element(By.TAG_NAME, "button").click()

#         time.sleep(5)
#         # 1: Criar curso sem nome
#         WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
#         ).click()
#         time.sleep(2)

#         WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
#         ).click()
#         time.sleep(2)

#         driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
#         driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
#         driver.find_element(By.TAG_NAME, "button").click()

#         WebDriverWait(driver, 10).until(
#             EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "É necessário preencher todas as informações.")
#         )
#         time.sleep(2)
#         # 2: Criar curso correto
#         driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
#         driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
#         driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
#         driver.find_element(By.TAG_NAME, "button").click()
#         time.sleep(2)
#         # 3: Criar curso com nome repetido
#         WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
#         ).click()
#         time.sleep(2)
#         driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
#         driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
#         driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
#         driver.find_element(By.TAG_NAME, "button").click()
#         WebDriverWait(driver, 10).until(
#             EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "'Você já tem um curso com este nome.")
#         )
#         time.sleep(2)


    









class Test2_Gerenciar_Curso(LiveServerTestCase):

    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )

        self.driver = webdriver.Chrome()


    def tearDown(self):
        self.driver.quit()

    def test2_Gerenciar_curso(self):
        driver = self.driver
        driver.get(self.live_server_url)

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")

        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        # 1 visualizar cursos
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()
        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Java")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Java")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))
        ).click()


        # 2 Editar curso sem nome

        nome = driver.find_element(By.ID, "campo_nome_curso")
        nome.clear()

        descricao = driver.find_element(By.ID, "campo_descricao_Curso")
        descricao.clear()
        descricao.send_keys("Descrição atualizada do curso.")

        n_alunos = driver.find_element(By.ID, "campo_n_alunos")
        n_alunos.clear()
        n_alunos.send_keys("50")
        driver.find_element(By.TAG_NAME, "button").click()
        # 3 Editar curso com nome repetido
        time.sleep(2)


        nome = driver.find_element(By.ID, "campo_nome_curso")
        nome.clear()
        nome.send_keys("Curso de Java")
        descricao = driver.find_element(By.ID, "campo_descricao_Curso")
        descricao.clear()
        descricao.send_keys("Descrição atualizada do curso.")

        n_alunos = driver.find_element(By.ID, "campo_n_alunos")
        n_alunos.clear()
        n_alunos.send_keys("50")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        # 4 Editar curso correto

        nome = driver.find_element(By.ID, "campo_nome_curso")
        nome.clear()
        nome.send_keys("Novo Curso Editado")

        descricao = driver.find_element(By.ID, "campo_descricao_Curso")
        descricao.clear()
        descricao.send_keys("Descrição atualizada do curso.")

        n_alunos = driver.find_element(By.ID, "campo_n_alunos")
        n_alunos.clear()
        n_alunos.send_keys("50")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        # 5 Excluir curso


        botao_deletar_sub = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form/button[contains(text(), 'Deletar')]"))
        )
        botao_deletar_sub.click()
        time.sleep(1)
        
        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)