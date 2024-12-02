import customtkinter as ctk
import requests
import subprocess

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
from random import randint
from datetime import datetime

class URL_Uvicorn():
    def iniciar_uvicorn(self):
        comando = ["uvicorn", "main:app", "--reload"]
        try:
            subprocess.Popen(comando)
            print("Servidor Uvicorn iniciado...")
        except subprocess.CalledProcessError as e:
            print(f"Erro ao iniciar o servidor: {e}")
    def url_uvicorn(self):
        try:
            url = f"http://127.0.0.1:8000"
        except ValueError:
            print("Não foi possivel acessar o servidor")
        return url
    def __init__ (self):
       self.iniciar_uvicorn()
        
class Atendente():
    def tela_atendente(self):
        painel_atendente = ctk.CTkToplevel()
        self.painel_atendente = painel_atendente
        self.painel_atendente.title('Painel Atendente')
        
        largura = 430 
        altura = 260
        largura_atendentex = (self.painel_atendente.winfo_screenwidth() / 2) - (largura) - 5
        altura_atendentey = (self.painel_atendente.winfo_screenheight() / 2) - (altura) - 40
        self.painel_atendente.geometry(f'{largura}x{altura}+{int(largura_atendentex)}+{int(altura_atendentey)}"')
        self.painel_atendente.transient(self.janela)
        self.painel_atendente.resizable(False,False)
        
        self.frames_atendente()
        self.lista_cliente()
    def frames_atendente(self):
        self.frame_atendente = ctk.CTkFrame(self.painel_atendente, width=400, height=240)
        self.frame_atendente.place(x=15, y=10)
        
        self.label_atendente = ctk.CTkLabel(self.frame_atendente, text="Clientes Aguardando", font=('verdana',14,'bold'))
        self.label_atendente.place(x= 120, y = 5)
        
        self.bottomProximo = ctk.CTkButton(self.frame_atendente, text= "Chamar Proximo", fg_color='#483D8B', hover_color='#836FFF', height=35, command=self.chamar_proximo)
        self.bottomProximo.place(x=125, y=195)
    def lista_cliente(self):
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            # reverse sort next time
            tv.heading(col, text=col, command=lambda _col=col: \
                        treeview_sort_column(tv, _col, not reverse))

        columns = ('POS', 'ID', 'NOME','DATA', 'TIPO')
        self.listaClientes = ttk.Treeview(self.frame_atendente, height= 3, columns=columns, show = 'headings')

        self.listaClientes.column('POS', width=30, anchor='center')
        self.listaClientes.column('ID', width=30, anchor='center')
        self.listaClientes.column('NOME', width=130, anchor='w')
        self.listaClientes.column('DATA', width=120, anchor='center')
        self.listaClientes.column('TIPO', width=50, anchor='center')

        self.listaClientes.place(x=15 , y=40, width=360, height=150)
        for col in columns:
            self.listaClientes.heading(col, text=col, command=lambda _col=col: \
            treeview_sort_column(self.listaClientes, _col, False))

        self.scroolLista = Scrollbar(self.frame_atendente, orient='vertical')
        self.listaClientes.configure(yscroll=self.scroolLista.set)
        self.scroolLista.configure(command=self.listaClientes.yview)
        self.scroolLista.place(x= 367, y=40, width=18, height=150)
        self.mostra_aguardando()
    def mostra_aguardando(self):
        resp = requests.get(f'{self.data}/fila')
        self.lista = resp.json()
        try:
            self.listaClientes.delete(*self.listaClientes.get_children())
            count = 0
            self.listaClientes.tag_configure('oddrow', background="white")
            self.listaClientes.tag_configure('evenrow', background="gray95")
            for dic in self.lista:
                tipoA = dic['nome'][-3:]
                dic['nome'] = dic['nome'][:-3]
                data_str = dic['data_entrada']
                data_obj = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')  # Converter para objeto datetime
                data_formatada = data_obj.strftime('%d/%m - %H:%M') + 'h'  # Formatar como '26/11 - 17:33h'
                dic['data_entrada'] = data_formatada
                if count % 2 == 0:
                    self.listaClientes.insert('',END, values=(*dic.values(),tipoA,), tags = ('evenrow'))
                else:
                    self.listaClientes.insert('',END, values=(*dic.values(),tipoA,), tags = ('oddrow'))
                count +=1
        except:
            print(self.lista['detail'])
    def chamar_proximo(self):
        resp = requests.put(f'{self.data}/fila')
        json = resp.json()
        msg = json[-1]['mensagem']

        index = [index for index in enumerate(json[1]) if msg[:5] == "Todos"]
        if not index:
            self.mostra_aguardando()
            id_atendido = json[0][0]['id_cliente']
            nome_atendido = json[0][0]['nome'][:-3]
            ############# logica dos ultimos atendidos #############
            ult1, ult2, ult3, ult4, ult5 = "-", "-", "-", "-", "-", 
            ult = {}
            for i in range(1, 6):
                if json[0][-1]['atendido'] == False:
                    for i in range(1, 6):
                        ult[f'ult{i}'] = "-"
                else:
                    try:    
                        if json[0][-i]['atendido'] == True and json[0][-i] != json[0][0]:
                                ult[f'ult{i}'] = json[0][-i]['id_cliente']
                        else:
                            ult[f'ult{i}'] = "-"
                    except:
                        ult[f'ult{i}'] = "-"
            ult1 = f"{ult['ult1']}"
            ult2 = f"{ult['ult2']}"
            ult3 = f"{ult['ult3']}"
            ult4 = f"{ult['ult4']}"
            ult5 = f"{ult['ult5']}"
            #########################################################
            Visor.update(self, id_atendido, nome_atendido, ult1, ult2, ult3, ult4, ult5)
            Controle.update(self, resp.json()[0][0])
        else:
            messagebox.showinfo('Atendimento', "Todos os clientes foram Atendidos!")
    def update(self):
        self.mostra_aguardando()
    def __init__(self):
        self.tela_atendente()
        
class Controle():
    def tela_controle(self):
        painel_controle = ctk.CTkToplevel()
        self.painel_controle = painel_controle
        self.painel_controle.title('Painel Controle')
        
        largura = 430 
        altura = 260
        largura_controlex = (self.painel_controle.winfo_screenwidth() / 2) - (largura) - 5
        altura_controley = (self.painel_controle.winfo_screenheight() / 2)
        self.painel_controle.geometry(f'{largura}x{altura}+{int(largura_controlex)}+{int(altura_controley)}"')
        self.painel_controle.transient(self.janela)
        self.painel_controle.resizable(False,False)
        
        self.todos_cliente = []
        
        self.frames_controle()
        self.lista_cliente_completa()      
    def frames_controle(self):
        self.frame_controle = ctk.CTkFrame(self.painel_controle, width=400, height=240)
        self.frame_controle.place(x=15, y=10)
        
        self.label_controle = ctk.CTkLabel(self.frame_controle, text="Painel de Controle", font=('verdana',14,'bold'))
        self.label_controle.place(x= 120, y = 5)
        
        self.removeID = ctk.CTkButton(self.frame_controle, text= "Remover ID:", fg_color='#483D8B', hover_color='#836FFF', width=70, height=35, command=self.remove_id)
        self.removeID.place(x=15, y=200)
        
        self.removeID_entry = ctk.CTkEntry(self.frame_controle, placeholder_text= "ID", width=30)
        self.removeID_entry.place(x=110, y=204)
        
        self.removePOS = ctk.CTkButton(self.frame_controle, text= "Remover POS:", fg_color='#483D8B', hover_color='#836FFF', width=70, height=35, command=self.remove_pos)
        self.removePOS.place(x=250, y=200)
        
        self.removePOS_entry = ctk.CTkEntry(self.frame_controle, placeholder_text= "POS", width=40)
        self.removePOS_entry.place(x=350, y=204)
    def lista_cliente_completa(self):
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)

            # rearrange items in sorted positions
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)

            # reverse sort next time
            tv.heading(col, text=col, command=lambda _col=col: \
                        treeview_sort_column(tv, _col, not reverse))

        columns = ('POS', 'ID', 'NOME','DATA', 'TIPO','STATUS')
        self.listaClientesCompleto = ttk.Treeview(self.frame_controle, height= 3, columns=columns, show = 'headings')

        self.listaClientesCompleto.column('POS', width=30, anchor='center')
        self.listaClientesCompleto.column('ID', width=30, anchor='center')
        self.listaClientesCompleto.column('NOME', width=80, anchor='w')
        self.listaClientesCompleto.column('DATA', width=90, anchor='center')
        self.listaClientesCompleto.column('TIPO', width=40, anchor='center')
        self.listaClientesCompleto.column('STATUS', width=90, anchor='center')

        self.listaClientesCompleto.place(x=15 , y=40, width=360, height=150)
        for col in columns:
            self.listaClientesCompleto.heading(col, text=col, command=lambda _col=col: \
            treeview_sort_column(self.listaClientesCompleto, _col, False))

        self.scroolLista = Scrollbar(self.frame_controle, orient='vertical')
        self.listaClientesCompleto.configure(yscroll=self.scroolLista.set)
        self.scroolLista.configure(command=self.listaClientesCompleto.yview)
        self.scroolLista.place(x= 367, y=40, width=18, height=150)
        self.id_atendido = None
        self.mostra_clientes_completo()
    def mostra_clientes_completo(self):
        self.lista = self.todos_cliente
        self.listaClientesCompleto.delete(*self.listaClientesCompleto.get_children())
        count = 0
        self.listaClientesCompleto.tag_configure('oddrow', background="white")
        self.listaClientesCompleto.tag_configure('evenrow', background="gray95")
        
        for dic in self.lista:
            pos = self.lista.index(dic)
            if dic['atendimento'] == False:
                status = 'Aguardando'
            else:
                status = 'Atendido'
            data_str = dic['data_entrada']
            try:
                if dic['nome'][-1:] == ")":
                    dic['nome'] = dic['nome'][:-3]
                data_obj = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')  # Converter para objeto datetime
                data_formatada = data_obj.strftime('%d/%m - %H:%M') + 'h'  # Formatar como '26/11 - 17:33h'
                dic['data_entrada'] = data_formatada
            except:
                pass
            if count % 2 == 0:
                self.listaClientesCompleto.insert('',END, values=(pos,dic['id_cliente'],dic['nome'],dic['data_entrada'],f"({dic['tipo_atendimento']})",status), tags = ('evenrow'))
            else:
                self.listaClientesCompleto.insert('',END, values=(pos,dic['id_cliente'],dic['nome'],dic['data_entrada'],f"({dic['tipo_atendimento']})",status), tags = ('oddrow'))
            count +=1
    def remove_id(self):
        if self.removeID_entry == "":
            messagebox.showwarning("Erro", "Por favor insira o ID do cliente a ser excluido!")
        else:
            id_removido = self.removeID_entry.get()
            
            resp = requests.delete(f'{self.data}/fila/id/{id_removido}')
            if resp.status_code == 404:
                messagebox.showinfo("404 Not Found","O ID do cliente informado nao foi encontrado")
                print(resp)
            else:
                msg = resp.json()
                messagebox.showinfo('Removido',f"{msg['mensagem']}")
                self.removeID_entry.destroy()
                self.removeID_entry = ctk.CTkEntry(self.frame_controle, placeholder_text= "ID", width=30)
                self.removeID_entry.place(x=110, y=204)
                
                self.todos_cliente = [cliente for cliente in self.todos_cliente if str(cliente['id_cliente']) != str(id_removido)]
                self.mostra_clientes_completo()
                Atendente.update(self)                
    def remove_pos(self):
        if self.removePOS_entry == "":
            messagebox.showwarning("Erro", "Por favor insira a posição do cliente a ser excluido!")
        else:
            pos_removido = self.removePOS_entry.get()
            
            resp = requests.delete(f'{self.data}/fila/id/{pos_removido}')
            if resp.status_code == 404:
                messagebox.showinfo("404 Not Found","A posição do cliente informado nao foi encontrado")
                print(resp)
            else:
                msg = resp.json()
                messagebox.showinfo('Removido',f"{msg['mensagem']}")
                self.removePOS_entry.destroy()
                self.removePOS_entry = ctk.CTkEntry(self.frame_controle, placeholder_text= "POS", width=40)
                self.removePOS_entry.place(x=350, y=204)

                self.todos_cliente = [cliente for cliente in self.todos_cliente if str(cliente['pos']) != str(pos_removido)]
                
                self.mostra_clientes_completo()
                Atendente.update(self)
    def update(self, resp):
        if isinstance(resp, dict):
            id = resp['id_cliente']
            self.status_atendido = True
            for item in self.listaClientesCompleto.get_children():
                item_id = self.listaClientesCompleto.item(item)['values'][1]
                if item_id == id:
                    for index in self.todos_cliente:
                        if index['id_cliente'] == id:
                            index['atendimento'] = True
                            break
        else:
            for clientes in self.todos_cliente:
                if clientes['pos'] >= resp.json()['pos']:
                    clientes['pos'] += 1
                
            self.todos_cliente.insert(resp.json()['pos'], resp.json())
        self.mostra_clientes_completo()
    def __init__(self):
        self.tela_controle()

class Visor():
    def tela_visor(self):
        painel_visor = ctk.CTkToplevel()
        self.painel_visor = painel_visor
        self.painel_visor.title('Painel Visor')
        
        largura = 430 
        altura = 260
        largura_visorx = (self.painel_visor.winfo_screenwidth() / 2) + 5
        altura_visory = (self.painel_visor.winfo_screenheight() / 2) - (altura) - 40
        self.painel_visor.geometry(f'{largura}x{altura}+{int(largura_visorx)}+{int(altura_visory)}"')
        self.painel_visor.transient(self.janela)
        self.painel_visor.resizable(False,False)
        
        self.frames_atendimento('','')
        self.frames_atendido("-","-","-","-","-")
    def frames_atendimento(self, id: str, nome: str):
        def centraliza(nome):
            largura = 20
            return nome.center(largura)
        mesa = randint(1,9)
        
        self.frame_visor = ctk.CTkFrame(self.painel_visor, width=100, height=100)
        self.frame_visor.place(x=165, y=20)
        
        self.label_id_atendido = ctk.CTkLabel(self.frame_visor, text=f'{id}', font=('verdana',35,'bold'))
        self.label_id_atendido.place(x=35, y=5)
        
        self.label_nome = ctk.CTkLabel(self.frame_visor, text=centraliza(f'  {nome}'), width=20, anchor="center")
        self.label_nome.place(x=0, y=45)
        
        self.label_mesa = ctk.CTkLabel(self.frame_visor, text=f'Mesa: {mesa}',font=('verdana',15,'bold'))
        self.label_mesa.place(x=15, y=70)
    def update(self, id: str, nome: str, ult1, ult2, ult3, ult4, ult5):
        self.frames_atendimento(id, nome)
        self.frames_atendido(ult1, ult2, ult3, ult4, ult5)
    def frames_atendido(self, ult1, ult2, ult3, ult4, ult5):
        self.label_ultimos = ctk.CTkLabel(self.painel_visor, text="Ultimos Atendidos:", font=('verdana',15,'bold'))
        self.label_ultimos.place(x = 20, y = 140 )
        
        self.frame_atendido1 = ctk.CTkFrame(self.painel_visor, width=60, height=60)
        self.frame_atendido1.place(x=20, y=170)
        
        self.frame_atendido2 = ctk.CTkFrame(self.painel_visor, width=60, height=60)
        self.frame_atendido2.place(x=102, y=170)
        
        self.frame_atendido3 = ctk.CTkFrame(self.painel_visor, width=60, height=60)
        self.frame_atendido3.place(x=184, y=170)
        
        self.frame_atendido4 = ctk.CTkFrame(self.painel_visor, width=60, height=60)
        self.frame_atendido4.place(x=266, y=170)
        
        self.frame_atendido5 = ctk.CTkFrame(self.painel_visor, width=60, height=60)
        self.frame_atendido5.place(x=348, y=170)
        
        self.label_atendido1 = ctk.CTkLabel(self.frame_atendido1, text = f"{ult1}", font=('verdana',20))
        self.label_atendido1.place(x=22, y=15)
        
        self.label_atendido2 = ctk.CTkLabel(self.frame_atendido2, text = f"{ult2}", font=('verdana',20))
        self.label_atendido2.place(x=22, y=15)
        
        self.label_atendido3 = ctk.CTkLabel(self.frame_atendido3, text = f"{ult3}", font=('verdana',20))
        self.label_atendido3.place(x=22, y=15)
        
        self.label_atendido4 = ctk.CTkLabel(self.frame_atendido4, text = f"{ult4}", font=('verdana',20))
        self.label_atendido4.place(x=22, y=15)
        
        self.label_atendido5 = ctk.CTkLabel(self.frame_atendido5, text = f"{ult5}", font=('verdana',20))
        self.label_atendido5.place(x=22, y=15)
    def __init__(self):
        self.tela_visor()

class Token():
    def tela_token(self):
        painel_token = ctk.CTkToplevel()
        self.painel_token = painel_token
        self.painel_token.title('Painel Token')
        
        largura = 430 
        altura = 260
        largura_tokenx = (self.painel_token.winfo_screenwidth() / 2) + 5
        altura_tokeny = (self.painel_token.winfo_screenheight() / 2) 
        self.painel_token.geometry(f'{largura}x{altura}+{int(largura_tokenx)}+{int(altura_tokeny)}"')
        self.painel_token.transient(self.janela)
        self.painel_token.resizable(False,False)
        
        self.frames_token()
    def frames_token(self):
        self.frame_token = ctk.CTkFrame(self.painel_token, width=370, height=200)
        self.frame_token.place(x=30, y=40)
        
        self.label_token = ctk.CTkLabel(self.frame_token, text="NOME", font=('verdana',20,'bold'))
        self.label_token.place(x= 150, y = 5)
        
        self.entry_token = ctk.CTkEntry(self.frame_token, placeholder_text="Insira seu nome", width=310, height=30)
        self.entry_token.place(x=30, y=40)
        
        self.bottomN = ctk.CTkButton(self.frame_token, text= "  (N)\n  Normal", text_color='black', fg_color='#90EE90', hover_color='#2E8B57', height=60, command=self.func_normal)
        self.bottomN.place(x=40, y=90)
        
        self.bottomP = ctk.CTkButton(self.frame_token, text= "(P)\n  Prioritario", text_color='black', fg_color='#FF7F50', hover_color='#B22222', height=60, command=self.func_prioritario)
        self.bottomP.place(x=190, y=90)
        
        self.bottomF = ctk.CTkButton(self.frame_token, text= "OK", command= self.func_adiciona)
        self.bottomF.place(x=110, y=160)
    def func_limpa(self):
        self.bottomN.configure(fg_color='#90EE90', text_color='black')
        self.bottomP.configure(fg_color='#FF7F50', text_color='black')
        self.entry_token.destroy()
        self.entry_token = ctk.CTkEntry(self.frame_token, placeholder_text="Insira seu nome", width=310, height=30)
        self.entry_token.place(x=30, y=40)
        del self.tipo_atendimento
        del self.nome
    def func_normal(self):
        self.bottomN.configure(fg_color='#90EE90', text_color='black')
        self.tipo_atendimento = 'N'
        self.bottomP.configure(fg_color="darkgray", text_color="white")
    def func_prioritario(self):
        self.bottomP.configure(fg_color='#FF7F50', text_color='black')
        self.tipo_atendimento = 'P'
        self.bottomN.configure(fg_color="darkgray", text_color="white")
    def func_adiciona(self):
        try:
            self.nome = self.entry_token.get()
            if self.nome != "":
                tp_atendimento = self.tipo_atendimento
                
                self.incluido = ctk.CTkLabel(self.painel_token, text=f"Bem vindo {self.nome.upper()}, aguarde e logo sera atendido!", font=('verdana',13,'bold'))
                self.incluido.place(x=25, y=0) 
                self.painel_token.after(3000, self.incluido.destroy)
                
                resp = requests.post(f'{self.data}/fila', json={"nome": f"{self.nome.upper()} ({tp_atendimento})", "tipo_atendimento": f"{tp_atendimento}"})
                
                Atendente.update(self)
                Controle.update(self, resp)
                self.func_limpa()
            else:
                messagebox.showwarning("Identifique-se", "Por favor, insira seu nome e qual o tipo de atendimento que deseja!")
        except:
            messagebox.showwarning("Identifique-se", "Por favor, insira seu nome e qual o tipo de atendimento que deseja!")
    def __init__(self):
        self.nome_cliente: str
        self.tipo_atendimento: str = None| None
        self.tela_token()
        
class Aplication(URL_Uvicorn, Atendente, Controle, Visor, Token):
    def tela(self):
        ctk.set_appearance_mode("dark")
        janela = ctk.CTk()
        self.janela = janela
        self.janela.title('Sistema API Atendimento')
        
        largura = 900
        altura = 600
        largura_janelax = (self.janela.winfo_screenwidth() / 2) - (largura / 2)
        altura_janelay = (self.janela.winfo_screenheight() / 2) - (altura / 2) - 40
        
        self.janela.geometry(f'{largura}x{altura}+{int(largura_janelax)}+{int(altura_janelay)}"')
        self.janela.resizable(False,False)

        self.botao_inicia = ctk.CTkButton(self.janela, text="INICIA", command=self.inicia)
        self.botao_inicia.place(relx = 0.4, rely = 0.4)

        self.janela.mainloop()
    def inicia(self):
        self.tela_token()
        self.tela_visor()
        self.tela_atendente()
        self.tela_controle()
        self.botao_inicia.destroy()
    def __init__(self):
        self.iniciar_uvicorn()
        self.data = self.url_uvicorn()
        self.tela()
        
if __name__ == '__main__':
    Aplication()
