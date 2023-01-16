from calendar import isleap
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter.ttk import Combobox

import psycopg2
import pandas as pd

menu = Tk()
class Functions():
    def limpar_tela(self):
        self.entry_id.delete(0, END)
        self.entry_book_name.delete(0, END)
        self.entry_book_publish_company.delete(0, END)
        self.entry_author.delete(0, END)
        self.entry_compra.delete(0, END)

    def conectar_bd(self):

        self.conn = psycopg2.connect(host='localhost',
                                     database='Biblioteca',
                                     user='postgres',
                                     password='flamengo52')
        print("Iniciando conexão")
        self.cursor = self.conn.cursor()
        print("Conectado ao Banco de Dados")

    def desconecta_bd(self):
        self.conn.close()

    def montaTabelas(self):
        self.conectar_bd()
        print("Banco de dados conectado")

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Control(
                            id INTEGER PRIMARY KEY,
                            livro VARCHAR(200) NOT NULL,
                            editora VARCHAR(200) NOT NULL,
                            autor VARCHAR(200) NOT NULL,
                            compra BOOLEAN NOT NULL
                        );
                    """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def select_bd(self):
        self.list.delete(*self.list.get_children())
        self.conectar_bd()
        self.cursor.execute("""
                            SELECT id, livro, editora, autor, compra 
                            FROM Control 
                            ORDER BY id ASC;
                            """)

        searchTar = self.cursor.fetchall()
        print(searchTar)

        lista_melhorada = []

        for i in searchTar:
            aux = []
            for k in range(0, len(i)):
                if k == 4:
                    if i[k] == True:
                        aux.append("Completa")
                        pass
                    else:
                        aux.append("Incompleta")
                else:
                    aux.append(i[k])
            lista_melhorada.append(aux)

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista_melhorada:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.desconecta_bd()

    def inserirBook(self):
        self.book = self.entry_book_name.get()
        self.editory = self.entry_book_publish_company.get()
        self.author = self.entry_author.get()
        self.compra = self.entry_compra.get()

        if self.compra == 'Completa':
            self.compra = True
        else:
            self.compra = False

        self.conectar_bd()
        self.cursor.execute("""
                            SELECT id, livro, editora, autor, compra 
                            FROM Control 
                            ORDER BY id ASC;
                            """)
        lista = self.cursor.fetchall()
        id = 0

        if len(lista) != 0:
            for i in lista:
                id = i[0]


        self.cursor.execute("""
                       INSERT INTO Control (id, livro, editora, autor, compra)
                        VALUES (%s, %s, %s, %s, %s)""", (id+1, self.book, self.editory, self.author, self.compra))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.list.selection()

        for n in self.list.selection():
            col1, col2, col3, col4, col5 = self.list.item(n, 'values')
            self.entry_id.insert(END, col1)
            self.entry_book_name.insert(END, col2)
            self.entry_book_publish_company.insert(END, col3)
            self.entry_author.insert(END, col4)
            self.entry_compra.insert(END, col5)

    def deleteBook(self):
        self.id = self.entry_id.get()
        self.book = self.entry_book_name.get()
        self.editory = self.entry_book_publish_company.get()
        self.author = self.entry_author.get()
        self.compra = self.entry_compra.get()

        self.conectar_bd()
        self.cursor.execute("""DELETE FROM Control WHERE id = %s """, (self.id, ))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()

    def updateBook(self):
        self.id = self.entry_id.get()
        self.book = self.entry_book_name.get()
        self.editory = self.entry_book_publish_company.get()
        self.author = self.entry_author.get()
        self.compra = self.entry_compra.get()

        if self.compra == 'Completa':
            self.compra = True
        else:
            self.compra = False

        self.conectar_bd()
        self.cursor.execute("""
                        UPDATE Control SET livro = %s, editora = %s, autor = %s, compra = %s
                        WHERE id = %s""", (self.book, self.editory, self.author, self.compra, self.id))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()

    def searchBought(self): # procurar comprados
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute("""
                        SELECT id, livro, editora, autor, compra 
                        FROM Control
                        WHERE compra = TRUE
                        ORDER BY id ASC
                        """)
        lista = self.cursor.fetchall()
        lista_melhorada = []

        for i in lista:
            aux = []
            for k in range(0, len(i)):
                if k == 4:
                    if i[k] == True:
                        aux.append("Completa")
                        pass
                    else:
                        aux.append("Incompleta")
                else:
                    aux.append(i[k])
            lista_melhorada.append(aux)

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista_melhorada:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.limpar_tela()
        self.desconecta_bd()

    def searchForWishlist(self): # buscar lista de desejos
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute("""
                        SELECT id, livro, editora, autor, compra 
                        FROM Control
                        WHERE compra = FALSE
                        ORDER BY id ASC
                        """)
        lista = self.cursor.fetchall()
        lista_melhorada = []

        for i in lista:
            aux = []
            for k in range(0, len(i)):
                if k == 4:
                    if i[k] == True:
                        aux.append("Completa")
                        pass
                    else:
                        aux.append("Incompleta")
                else:
                    aux.append(i[k])
            lista_melhorada.append(aux)

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista_melhorada:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.limpar_tela()
        self.desconecta_bd()

class Books(Functions):

    cor_de_fundo = "Gray"
    bordas_frames = "Black"
    cor_letras = "Black"
    cor_botoes = "SlateGray"

    def __init__(self):
        self.books = menu
        self.books.title("Controle dos meus livros")
        self.books.geometry("600x600")
        self.books.configure(background=self.cor_de_fundo)
        self.books.resizable(False, False)
        self.frames_books_page()
        self.labels_books_page()
        self.buttons_books_page()
        self.list_frame()
        self.montaTabelas()
        self.select_bd()
        self.center(self.books)
        self.books.mainloop()

    def center(self, page):
        """ FUNÇÃO RESPONSAVEL POR CENTRALIZAR AS PAGES NA TELA"""

        page.withdraw()
        page.update_idletasks()  # Update "requested size" from geometry manager

        x = (page.winfo_screenwidth() - page.winfo_reqwidth()) / 4
        y = (page.winfo_screenheight() - page.winfo_reqheight()) / 6
        page.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        page.deiconify()

    def frames_books_page(self):

        self.frame_book_information = Frame(self.books,
                                       bd= 4,
                                       bg= self.cor_de_fundo,
                                       highlightbackground= self.bordas_frames,
                                       highlightthickness= 1)
        self.frame_book_information.place(rely= 0.01, relx= 0.02, relwidth= 0.96, relheight= 0.98)

    def labels_books_page(self):
        self.lb_title = Label(self.frame_book_information, text= "Minha Biblioteca", font= "-weight bold -size 15",
                              bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_title.place(rely= 0.01, relx= 0.37, relwidth= 0.274)

        self.lb_id = Label(self.frame_book_information, text= "Id", font= "-weight bold -size 12",
                           bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_id.place(rely= 0.07, relx= 0.01, relwidth= 0.023)

        self.entry_id = Entry(self.frame_book_information)
        self.entry_id.place(rely= 0.115, relx= 0.01, relwidth= 0.045)

        self.lb_book_name = Label(self.frame_book_information, text= "Nome", font= "-weight bold -size 12",
                                  bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_book_name.place(rely= 0.07, relx= 0.09, relwidth= 0.082)

        self.entry_book_name = Entry(self.frame_book_information)
        self.entry_book_name.place(rely= 0.115, relx= 0.09, relwidth= 0.12)
        #
        self.lb_book_publish_company = Label(self.frame_book_information, text= "Editora", font= "-weight bold -size 12",
                                            bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_book_publish_company.place(rely= 0.07, relx= 0.245, relwidth= 0.1)
        #
        self.entry_book_publish_company = Entry(self.frame_book_information)
        self.entry_book_publish_company.place(rely= 0.115, relx= 0.245, relwidth= 0.12)
        #
        self.lb_author = Label(self.frame_book_information, text= "Autor", font= "-weight bold -size 12", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_author.place(rely= 0.07, relx= 0.4, relwidth= 0.073)
        #
        self.entry_author = Entry(self.frame_book_information)
        self.entry_author.place(rely= 0.115, relx= 0.4, relwidth= 0.12)
        #
        #
        self.lb_compra = Label(self.frame_book_information, text= "Compra", font= "-weight bold -size 12", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_compra.place(rely= 0.07, relx= 0.555, relwidth= 0.11)
        #
        self.entry_compra = Combobox(self.frame_book_information, values=['Completa', 'Incompleta'])
        self.entry_compra.place(rely= 0.115, relx= 0.555, relwidth= 0.15)

    def buttons_books_page(self):

        self.bt_books_cadastrar = Button(self.frame_book_information, text= "Inserir", background= self.cor_botoes, bd= 6,
                                         font= "-weight bold -size 11", command= self.inserirBook)
        self.bt_books_cadastrar.place(rely= 0.175, relx= 0.01, relwidth= 0.1, relheight= 0.06)
        #
        self.bt_books_update = Button(self.frame_book_information, text= "Alterar", background= self.cor_botoes, bd= 6,
                                      font= "-weight bold -size 11", command= self.updateBook)
        self.bt_books_update.place(rely= 0.175, relx= 0.14, relwidth= 0.105, relheight= 0.06)
        #
        self.bt_books_delete = Button(self.frame_book_information, text= "Excluir", background= self.cor_botoes, bd= 6,
                                      font= "-weight bold -size 11", command= self.deleteBook)
        self.bt_books_delete.place(rely= 0.175, relx= 0.275, relwidth= 0.105, relheight= 0.06)

        self.bt_books_exit = Button(self.frame_book_information, text= "Sair", background= self.cor_botoes , bd= 6,
                                    font= "-weight bold -size 11", command= self.books.quit)
        self.bt_books_exit.place(rely= 0.175, relx= 0.41, relwidth= 0.09, relheight= 0.06)

        self.bt_books_mys = Button(self.frame_book_information, text= "Meus \nLivros", background= self.cor_botoes, bd= 6,
                                   font= "-weight bold -size 11", command= self.searchBought)
        self.bt_books_mys.place(rely= 0.147, relx= 0.717, relwidth= 0.105, relheight= 0.09)

        self.bt_books_dreams = Button(self.frame_book_information, text= "Lista de\nDesejos", background= self.cor_botoes, bd= 6,
                                      font= "-weight bold -size 11", command= self.searchForWishlist)
        self.bt_books_dreams.place(rely= 0.147, relx= 0.85, relwidth= 0.13, relheight= 0.09)

    def list_frame(self):
    #
       self.list = ttk.Treeview(self.frame_book_information, height=3,
                                columns=("col1", "col2", "col3", "col4", "col5"))
    #
       self.list.heading("#0", text="")
       self.list.heading("#1", text="Id")
       self.list.heading("#2", text="Nome")
       self.list.heading("#3", text="Editora")
       self.list.heading("#4", text="Autor")
       self.list.heading("#5", text="Compra")
    #
       self.list.column("#0", width=1)
       self.list.column("#1", width=1)
       self.list.column("#2", width=100)
       self.list.column("#3", width=70)
       self.list.column("#4", width=70)
       self.list.column("#5", width=35)
    #
       self.list.place(rely=0.25, relx=0.01, relwidth=0.97, relheight=0.745)
    #
       self.scrollList = Scrollbar(self.frame_book_information, orient="vertical")
       self.list.configure(yscroll=self.scrollList.set)
       self.scrollList.place(relx=0.97, rely=0.25, relwidth=0.02, relheight=0.745)
       self.list.bind("<Double-1>", self.OnDoubleClick)

Books()