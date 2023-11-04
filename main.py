import pyodbc
from tkinter import *
from tkinter import Tk,ttk
from tkcalendar import Calendar,DateEntry
from collections import Counter
import random
import sqlite3


#dicionários de fontes e cores
st_f = {'f1':('M Hei PRC', 10, 'bold'),'f2':('Helvetica', 8,'bold','italic'),'f3':('Helvetica', 10, 'bold'),'f4':("Helvetica", 12, "bold"),'f5':('Helvetica', 7, 'italic'),'f6':('New', 9),'f7':('Arial', 10, 'bold')}

#DICIONÁRIO DE CORES USADAS DENTRO DO PROGRAMA.
# C REPRESENTA CORES
		#CORES	LARANJA			BRANCO		 AZUL ESCURO	AZUL CEU	  VERDE			VERMELHO
c: dict = {'1':'#e69138', '2':'#ffffff','3':'#033364', '4':'#f0ffff','5':'#44ab4c','6':'#e32636','7':'#000000'}
root = Tk()
#criando a class que executará a tela da aplicação 
class Aplication:
    def __init__(self):
        self.root = root
        self.winConfig()
        self.frames()
        self.windgets_app()
        root.mainloop()
        pass
    #Função para todas as configurações da tela
    def winConfig(self):
        self.root.geometry("400x300")
        self.root.config(bg=c['3'])
        self.root.resizable(False,False)# impede que a tela seja maximizada ou minimizada
        #Define que a tela sempre seja criada no meio da tela do computador--------------------------------------------------------------
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        win_width = 400
        win_height = 300
        # Calcula as coordenadas para centralizar a janela
        x = int(screen_width / 2 - win_width / 2)
        y = int(screen_height / 2 - win_height / 1)
        # Define as coordenadas da janela
        self.root.geometry(f"{win_width}x{win_height}+{x}+{y}")
        #--------------------------------------------------------------------------------------------------------------------------------
    #função que cria os frames da tela
    def frames(self):
        self.fm_superior = Frame(self.root,width=378, height=160)
        self.fm_superior.place_configure(x=10,y=45)
        
        self.fm_baixo = Frame(self.root,width=378,height=70)
        self.fm_baixo.place_configure(x=10,y=215)

    #Função que cria e exibe todos os Widgets da tela
    def windgets_app(self):
        self.style = ttk.Style()
        self.style.configure('my.DataEntry.TButton',
                fieldbackground='light green',
                background='dark green',
                foreground=c['3'],
                arrowcolor='white'
                )

        self.entry_concurso = Entry(self.fm_superior)
        self.entry_concurso.place_configure(x=20, y=20, width=100,height=25)

        self.data_conc = DateEntry(self.fm_superior,style='my.DataEntry.TButton',width=12,locale='pt_br',font=st_f['f6'])
        self.data_conc.place_configure(x=150, y=20, height=27)

        self.bt_pesquisar = Button(self.fm_superior,text="Pesquisar",font=st_f['f2'])
        self.bt_pesquisar.place_configure(x=280, y=20, width=90, height=25)

        self.entry_num = Entry(self.fm_superior)
        self.entry_num.place_configure(x=20, y=70, width=175,height=25)

        self.options= ttk.Combobox(self.fm_superior,values=['Sim','Não'])
        self.options.place_configure(x=215, y=70, width=50,height=25)
        self.options.bind("<<ComboboxSelected>>", self.combobox_selected)


        self.valor_vencedor = None  # Variável para rastrear o Entry de valor premiado
    #lógica das escolhas do ComboBox
    def combobox_selected(self, event):
        selected_option = self.options.get()
        if selected_option == "Sim":
            self.show_entry()
        elif selected_option == "Não":
            self.hide_entry()
    
    #Essa Função mostra o entry que recebe o valor que foi premiado no concurso apenas quando o Combobox chama a opção "Sim"
    def show_entry(self,event=None):
        if self.options.get() == "Sim":
            self.valor_vencedor = Entry(self.fm_superior)
            self.valor_vencedor.place_configure(x=20,y=120,width=175, height=25)
    # Função que esconde o entry que recebe o valor que foi premiado no concurso apenas quando o Combobox chama a opção "Não"
    def hide_entry(self):
        if self.valor_vencedor is not None:
            self.valor_vencedor.place_forget()
            self.valor_vencedor = None





if __name__ == "__main__":
    Aplication()

         


def insert_in_database():
    conn = sqlite3.connect('MegaData.db')
    cursor = conn.cursor()
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
                        cursor.execute("INSERT INTO HIST_MEGA_SENA (Concurso, Data_concurso, Aposta, Vencedor) VALUES (?, ?, ?, ?)",
                                    (concurso, data_concurso, apostas, vencedor))
                        conn.commit()
                        # Limpar as variáveis
                        concurso = ""
                        data_concurso = ""
                        apostas = ""
                        vencedor = ""
                    except Exception as e:
                        print("Erro", str(e))

    # Fechar a conexão com o banco de dados
    cursor.close()

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

