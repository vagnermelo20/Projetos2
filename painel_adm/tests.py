from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from home.models import Usuario
from django.contrib.auth.hashers import make_password
import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
class Test1_Criar_Curso(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test1_Criar_curso(self):
        driver = self.driver  # ✅ Aqui está o que você queria
        time.sleep(5)
        driver.get(self.live_server_url)

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")
        time.sleep(1) 

        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        # 1: Criar curso sem nome
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()
        time.sleep(2)

        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "É necessário preencher todas as informações.")
        )
        time.sleep(2)
        # 2: Criar curso correto
        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        # 3: Criar curso com nome repetido
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()
        time.sleep(2)
        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Você já tem um curso com este nome.")
        )
        time.sleep(2)


    









class Test2_Gerenciar_Curso(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test2_Gerenciar_curso(self):
        driver = self.driver
        time.sleep(10)
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
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "button").click()
        # 1 visualizar cursos
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()
        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Java")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Java")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        time.sleep(5)
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
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "É necessário preencher todas as informações.")
        )
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
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Você já tem um curso com este nome.")
        )
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
        time.sleep(5)
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




class Test3_Criar_Processo_Seletivo(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test3_Criar_Processo_Seletivo(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
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
        time.sleep(3)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)
        driver.find_element(By.LINK_TEXT, "Voltar").click()



        time.sleep(1)


        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()

        # 1 Criar processo seletivo Para um curso que nao existe.

        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("13-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Inteligência Artificial")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Esse curso não existe")
        )

        # 2 Criar processo seletivo que inicia antes de hoje.
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_inicio").send_keys("03-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("13-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "O processo seletivo não pode iniciar antes do dia de hoje.")
        )    
        time.sleep(2)
        # 3 Criar processo seletivo que termina depois de iniciar.

        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("08-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "A data de início não pode ser posterior ou igual à data final.")
        )            
        time.sleep(2)
        # 4 Criar processo seletivo correto
        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)




class Test4_Gerenciar_Processo_Seletivo(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )



    def test4_Gerenciar_Processo_Seletivo(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")

        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(1)

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()

        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
    
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 1: Visualizar processo seletivo

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Editar"))
        ).click()
        time.sleep(1)
        # 2: Editar processo seletivo com data que inicia antes de hoje
        campo_inicio = driver.find_element(By.ID, "campo_data_inicio")
        campo_inicio.clear()
        campo_inicio.send_keys("03-06-2025")

        campo_fim = driver.find_element(By.ID, "campo_data_fim")
        campo_fim.clear()
        campo_fim.send_keys("13-06-2025")

        campo_participantes = driver.find_element(By.ID, "campo_max_participantes")
        campo_participantes.clear()
        campo_participantes.send_keys("100")

        campo_aulas = driver.find_element(By.ID, "campo_data_inicio_aulas")
        campo_aulas.clear()
        campo_aulas.send_keys("16-06-2025")
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "O processo seletivo não pode iniciar antes do dia de hoje.")
        )

        time.sleep(2)

        # 3: Editar processo seletivo com data de fim anterior à de início
        campo_inicio = driver.find_element(By.ID, "campo_data_inicio")
        campo_inicio.clear()
        campo_inicio.send_keys("09-06-2025")

        campo_fim = driver.find_element(By.ID, "campo_data_fim")
        campo_fim.clear()
        campo_fim.send_keys("08-06-2025")

        campo_participantes = driver.find_element(By.ID, "campo_max_participantes")
        campo_participantes.clear()
        campo_participantes.send_keys("100")

        campo_aulas = driver.find_element(By.ID, "campo_data_inicio_aulas")
        campo_aulas.clear()
        campo_aulas.send_keys("16-06-2025")
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "A data de início não pode ser posterior ou igual à data final.")
        )

        time.sleep(2)

        # 4: Editar processo seletivo corretamente
        campo_inicio = driver.find_element(By.ID, "campo_data_inicio")
        campo_inicio.clear()
        campo_inicio.send_keys("09-06-2025")

        campo_fim = driver.find_element(By.ID, "campo_data_fim")
        campo_fim.clear()
        campo_fim.send_keys("13-06-2025")

        campo_participantes = driver.find_element(By.ID, "campo_max_participantes")
        campo_participantes.clear()
        campo_participantes.send_keys("100")

        campo_aulas = driver.find_element(By.ID, "campo_data_inicio_aulas")
        campo_aulas.clear()
        campo_aulas.send_keys("16-06-2025")
        time.sleep(5)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 5: Deletar processo seletivo
        botao_deletar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form/button[contains(text(), 'Deletar')]"))
        )
        botao_deletar.click()
        time.sleep(1)

        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)


























class Test5_Criar_Contas(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test5_Criar_Conta(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
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
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()


        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Gerir contas"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar contas"))
        ).click()


        # 1: Conta professor sem curso
        driver.find_element(By.ID, "campo_nome").send_keys("prof_invalido")
        driver.find_element(By.ID, "campo_email").send_keys("prof@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Professor")
        driver.find_element(By.ID, "campo_curso_conta").send_keys("Curso Inexistente")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Esse curso não existe")
        )
        time.sleep(2)

        # 2: Conta admin sem nome
        driver.find_element(By.ID, "campo_email").send_keys("admin_sem_nome@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Administrador")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()

        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "É necessário preencher todas as informações.")
        )
        time.sleep(2)

        # 3: Conta admin correta

        driver.find_element(By.ID, "campo_nome").send_keys("admin_valido")
        driver.find_element(By.ID, "campo_email").send_keys("admin@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Administrador")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(2)

        # 4: Conta professor correta
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar contas"))
        ).click()



        driver.find_element(By.ID, "campo_nome").send_keys("prof_valido")
        driver.find_element(By.ID, "campo_email").send_keys("prof@valido.com")
        driver.find_element(By.ID, "campo_senha").send_keys("senha123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Professor")
        driver.find_element(By.ID, "campo_curso_conta").send_keys("Curso de Python")  # o curso deve existir no banco!
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(2)
    














class Test6_Gerenciar_Contas(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test6_Gerenciar_Conta(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")

        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Gerir contas"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar contas"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("admin_valido")
        driver.find_element(By.ID, "campo_email").send_keys("admin@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Administrador")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()
        # 1: Visualizar conta
        time.sleep(2)
        
        # 2: Editar conta sem nome

        
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Alterar"))
        ).click()

        driver.find_element(By.ID, "campo_username").clear()
        driver.find_element(By.ID, "campo_email").send_keys("admin@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("admin123")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "É necessário preencher todas as informações.")
        )
        time.sleep(2)

        # 3: Editar conta corretamente
        driver.find_element(By.ID, "campo_username").send_keys("admin_alterado")
        driver.find_element(By.ID, "campo_email").send_keys("admin@alterado.com")
        driver.find_element(By.ID, "campo_senha").send_keys("adminalterado")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        # 4: deletar conta

        botao_deletar = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//form/button[contains(text(), 'Deletar')]"))
        )
        botao_deletar.click()
        time.sleep(1)

        alerta = driver.switch_to.alert
        alerta.accept()
        time.sleep(2)






















class Test7_Entrar_Processo_Seletivo(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test7_Entrar_Processo_Seletivo(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        time.sleep(2)
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        )
        link.click()
        time.sleep(2)
        # 1 Entrar sem nome
        driver.find_element(By.ID, "campo_telefone").send_keys("888888888") 
        driver.find_element(By.ID, "campo_idade").send_keys("25")
        time.sleep(2)
        driver.find_element(By.ID, "campo_bairro").send_keys("Centro")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Médio Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Noite")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Todos os campos são obrigatórios.")
        )
        time.sleep(2)
        # 2 Criar inscrição correta
        driver.find_element(By.ID, "campo_nome").send_keys("nome1")
        driver.find_element(By.ID, "campo_telefone").send_keys("888888888") 
        driver.find_element(By.ID, "campo_idade").send_keys("30")
        time.sleep(2)
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro Novo")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        # 3 Criar inscrição com telefone repetido
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        time.sleep(2)
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        )
        link.click()
        driver.find_element(By.ID, "campo_nome").send_keys("nome2")
        driver.find_element(By.ID, "campo_telefone").send_keys("888888888") 
        driver.find_element(By.ID, "campo_idade").send_keys("27")
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro velho")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
            EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "Número já cadastrado. Insira outro número e tente novamente.")
        )
        time.sleep(2)

        # Agora vamos ver o aluno dentro do processo seletivo
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")

        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Alunos"))
        ).click()
        time.sleep(5)
# # Falta o teste de aceitar aluno em processo seletivo





















class Test8_dar_notas_alunos_Professor(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )



    def test8_dar_notas_alunos_Professor(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()

        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        time.sleep(2)



        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Gerir contas"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar contas"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("professor")
        driver.find_element(By.ID, "campo_email").send_keys("professor@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("Profsenha123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Professor")
        driver.find_element(By.ID, "campo_curso_conta").send_keys("Curso de Python")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        ).click()


        driver.find_element(By.ID, "campo_nome").send_keys("nome1")
        driver.find_element(By.ID, "campo_telefone").send_keys("888888888") 
        driver.find_element(By.ID, "campo_idade").send_keys("30")
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro Novo")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("professor@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("Profsenha123")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Gerenciamento acadêmico"))
        )
        link.click()
        time.sleep(2)

# Cenário 1: Enviar presença sem marcar tudo

        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(4)

# Cenário 2: Enviar presença marcando tudo
        driver.find_element(By.ID, "teste").click()
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(4)
# cENÁRIO 3: Ver as notas dos alunos 
        driver.find_element(By.LINK_TEXT, "Visualizar alunos").click()
        time.sleep(4)





















class Test9_dar_avaliacao_Professor(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )

    def test9_dar_avaliacao_alunos_Professor(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()

        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        time.sleep(2)



        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Gerir contas"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar contas"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("professor")
        driver.find_element(By.ID, "campo_email").send_keys("professor@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("Profsenha123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Professor")
        driver.find_element(By.ID, "campo_curso_conta").send_keys("Curso de Python")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        ).click()


        driver.find_element(By.ID, "campo_nome").send_keys("nome1")
        driver.find_element(By.ID, "campo_telefone").send_keys("888888888") 
        driver.find_element(By.ID, "campo_idade").send_keys("30")
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro Novo")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("professor@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("Profsenha123")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Gerenciamento acadêmico"))
        )
        link.click()
        time.sleep(15)

        driver.find_element(By.ID, "teste2").click()
        time.sleep(2)
        Select(driver.find_element(By.ID, "comunicacao")).select_by_visible_text("4")
        time.sleep(2)
        Select(driver.find_element(By.ID, "conhecimento")).select_by_visible_text("2")
        time.sleep(2)
        Select(driver.find_element(By.ID, "participacao")).select_by_visible_text("3")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(4)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        time.sleep(4)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar alunos"))
        ).click()

        time.sleep(6)





















class Test10_visualizar_aluno(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()

    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )

    def test10_visualizar_alunos(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()

        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        time.sleep(2)



        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Gerir contas"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar contas"))
        ).click()

        driver.find_element(By.ID, "campo_nome").send_keys("professor")
        driver.find_element(By.ID, "campo_email").send_keys("professor@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("Profsenha123")
        driver.find_element(By.ID, "campo_tipo_conta").send_keys("Professor")
        driver.find_element(By.ID, "campo_curso_conta").send_keys("Curso de Python")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        ).click()


        driver.find_element(By.ID, "campo_nome").send_keys("nome1")
        driver.find_element(By.ID, "campo_telefone").send_keys("81990949392") 
        driver.find_element(By.ID, "campo_idade").send_keys("30")
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro Novo")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        ).click()


        driver.find_element(By.ID, "campo_nome").send_keys("nome2")
        driver.find_element(By.ID, "campo_telefone").send_keys("81990949399") 
        driver.find_element(By.ID, "campo_idade").send_keys("30")
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro Novo")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)


        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("professor@exemplo.com")
        driver.find_element(By.ID, "campo_senha").send_keys("Profsenha123")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()

        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar alunos"))
        )
        link.click()
        time.sleep(15)




































class Test11_Entrar_Whatsaap(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        options = Options()
        if os.environ.get('GITHUB_ACTIONS') == 'true':
            options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        super().tearDownClass()


    def setUp(self):
        # Cria um usuário no seu modelo customizado
        self.usuario = Usuario.objects.create(
            Username='testeuser',
            E_mail='teste@email.com',
            Senha='123',  # ou só: 'minhasenha123' e deixar o save() cuidar
            Tipos_conta='Admin'
        )


    def test11_Entrar_Whatsaap(self):
        driver = self.driver
        driver.get(self.live_server_url)
        time.sleep(6)
        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Cursos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar curso"))
        ).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_nome").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_descricao").send_keys("Curso introdutório de programação em Python")
        driver.find_element(By.ID, "campo_n_alunos").send_keys("30")
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        driver.find_element(By.LINK_TEXT, "Voltar").click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Criar processo seletivo"))
        ).click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_data_inicio").send_keys("09-06-2025")
        time.sleep(2)
        driver.find_element(By.ID, "campo_data_fim").send_keys("12-06-2025")
        time.sleep(1)
        driver.find_element(By.ID, "campo_max_participantes").send_keys("100")
        driver.find_element(By.ID, "campo_curso_para_processo").send_keys("Curso de Python")
        driver.find_element(By.ID, "campo_data_inicio_curso").send_keys("16-06-2025")
        time.sleep(2)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)

        
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Voltar"))
        ).click()
        time.sleep(2)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Processo seletivo"))
        ).click()

        time.sleep(2)
        link = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Curso de Python"))
        )
        link.click()
        time.sleep(2)

        # 2 Criar inscrição correta
        driver.find_element(By.ID, "campo_nome").send_keys("nome1")
        driver.find_element(By.ID, "campo_telefone").send_keys("888888888") 
        driver.find_element(By.ID, "campo_idade").send_keys("30")
        time.sleep(2)
        driver.find_element(By.ID, "campo_bairro").send_keys("Bairro Novo")
        Select(driver.find_element(By.ID, "campo_educacao")).select_by_visible_text("Superior Completo")
        Select(driver.find_element(By.ID, "campo_periodo_estudo")).select_by_visible_text("Manhã")
        time.sleep(4)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(2)
 

        driver.find_element(By.LINK_TEXT, "Login").click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "campo_email"))
        )

        driver.find_element(By.ID, "campo_email").send_keys("teste@email.com")
        driver.find_element(By.ID, "campo_senha").send_keys("123")

        driver.find_element(By.TAG_NAME, "button").click()

        time.sleep(1)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Processos"))
        ).click()
        time.sleep(3)
        WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Visualizar Alunos"))
        ).click()
        time.sleep(5)

        # Parte nova

        driver.find_element(By.ID, "aceitar1").click()
        time.sleep(1)
        driver.find_element(By.ID, "campo_mensagem").send_keys("mensagem")
        time.sleep(1)
        driver.find_element(By.TAG_NAME, "button").click()
        time.sleep(15)
