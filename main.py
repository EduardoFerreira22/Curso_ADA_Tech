import pyodbc
from tkinter import messagebox
from collections import Counter
import random


class Conections():
    def conect_SqlServer():
        pass
    def conn_SqLite3(self):
        import sqlite3
        conn = sqlite3.connect('MegaData.db')
        cursor = conn.cursor()
        try:
            cursor.execute(''' CREATE TABLE  IF NOT EXISTS HIST_MEGA_SENA
                        (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL
                        ,CONCURSO INTEGER , DATA_CONCURSO DATE, APOSTA TEXT, VENCEDOR TEXT)''')
        
         
            if cursor:
                messagebox.showinfo("Sucesso!", "Tabela criada com sucesso!")

        except Exception as e:
            print(f"Não foi possível criar a tabela {e}")

conect = Conections()
conect.conn_SqLite3()
        


def insert_in_database():
    # Configurações de conexão com o banco de dados SQL Server
    conexao = pyodbc.connect(
        'DRIVER={SQL Server};'
        f'SERVER=DESKTOP-S778AIB\\ED_SYSTEM;'
        'DATABASE=My_Projects;'
        'UID=systemadm;'
        'PWD=1234;'
    )
    cursor = conexao.cursor()

    if cursor:
        print("Conectado com sucesso!")

    # Inicializar variáveis para armazenar os dados do concurso
    concurso = ""
    data_concurso = ""
    apostas = ""
    vencedor = ""

    # Abrir o arquivo de texto
    with open("dados_concursos.txt", "r") as arquivo:
        for linha in arquivo:
            linha = linha.strip()  # Remover espaços em branco

            if linha.startswith("Concurso:"):
                # Extrair o número do concurso
                concurso = linha.split("Concurso:")[1].split('-')[0].strip()
                vencedor = "Ganhadora" if "Ganhadora" in linha else ""
            elif linha.startswith("Data:"):
                # Extrair a data do concurso no formato "dd/mm/yyyy"
                data_concurso = linha.split("Data:")[1].strip()
                # Converter para o formato "aaaa-mm-dd" esperado pelo SQL Server
                data_concurso = data_concurso.split("/")
                data_concurso = f"{data_concurso[2]}-{data_concurso[1]}-{data_concurso[0]}"
            elif linha.startswith("Aposta:"):
                # Extrair a sequência de números da aposta
                apostas = linha.split("Aposta:")[1].strip()

                # Inserir os dados no banco de dados quando todas as informações estiverem disponíveis
                if concurso and data_concurso and apostas:
                    try:
                        # Inserir os dados na tabela do banco de dados
                        cursor.execute("INSERT INTO MEGA_SENA (Concurso, Data_concurso, Aposta, Vencedor) VALUES (?, ?, ?, ?)",
                                    (concurso, data_concurso, apostas, vencedor))
                        conexao.commit()
                        # Limpar as variáveis
                        concurso = ""
                        data_concurso = ""
                        apostas = ""
                        vencedor = ""
                    except Exception as e:
                        print("Erro", str(e))

    # Fechar a conexão com o banco de dados
    conexao.close()

def gerador_de_num():


    # Lista para armazenar os números das apostas ganhadoras
    numeros_apostas_ganhadoras = []

    # Abre o arquivo para leitura
    with open('dados_concursos.txt', 'r') as arquivo:
        linhas = arquivo.readlines()

    for linha in linhas:
        # Remove espaços em branco no início e no final da linha
        linha = linha.strip()
        
        if linha.startswith("Aposta:") and "Ganhadora" in linha:
            # Divide a linha da aposta em números separados
            numeros = [int(num) for num in linha.split(": ")[1].split("-")]
            numeros_apostas_ganhadoras.extend(numeros)

    # Conta a frequência de cada número nas apostas ganhadoras
    contagem_numeros = Counter(numeros_apostas_ganhadoras)

    # Encontre os 6 números mais frequentes
    seis_mais_frequentes = [numero for numero, _ in contagem_numeros.most_common(6)]

    # Gere um jogo baseado nos 6 números mais frequentes
    jogo = random.choices(seis_mais_frequentes, k=6)

    print("Os 6 números mais frequentes nas apostas ganhadoras são:", seis_mais_frequentes)
    print("Seu jogo gerado com base nesses números é:", jogo)

