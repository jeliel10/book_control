import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from tkinter.ttk import Combobox
import psycopg2

menu = Tk()
class Functions():
    def limpar_tela(self):
        self.entry_id_book_dreams.delete(0, END)
        self.entry_name_book_dreams.delete(0, END)
        self.entry_book_editory_dreams.delete(0, END)
        self.entry_tipo_leitura_dreams.delete(0, END)

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
                        CREATE TABLE IF NOT EXISTS Books(
                            id INTEGER PRIMARY KEY,
                            nome VARCHAR(200) NOT NULL,
                            editora VARCHAR(200) NOT NULL,
                            tipo_leitura VARCHAR(100) NOT NULL,
                            status BOOLEAN NOT NULL
                        );
                    """)
        self.conn.commit()
        print("Banco de dados criado")
        self.desconecta_bd()

    def montaTabelas2(self):
        self.conectar_bd()

        self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS Comprados(
                            id INTEGER PRIMARY KEY,
                            nome VARCHAR(200) NOT NULL,
                            editora VARCHAR(200) NOT NULL,
                            tipo_leitura VARCHAR(100) NOT NULL
                        );
                    """)
        self.conn.commit()
        self.desconecta_bd()

    def select_bd(self):
        self.list.delete(*self.list.get_children())

        self.conectar_bd()
        self.cursor.execute("""
                            SELECT id, nome, editora, tipo_leitura 
                            FROM Books 
                            WHERE status = True
                            ORDER BY id ASC;
                            """)

        lista = self.cursor.fetchall()
        print(lista)


        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.desconecta_bd()

    def selectBdComprados(self):
        self.list2.delete(*self.list2.get_children())

        self.conectar_bd()
        self.cursor.execute("""
                                    SELECT id, nome, editora, tipo_leitura 
                                    FROM Comprados 
                                    ORDER BY id ASC;
                                    """)

        lista = self.cursor.fetchall()
        print(lista)

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list2.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list2.insert("", END, values=k)
        self.desconecta_bd()

    def inserirBook(self):
        self.nome =  self.entry_name_book.get()
        self.editora = self.entry_book_editory.get()
        self.tipo_leitura = self.entry_tipo_leitura.get()
        self.status = True


        self.conectar_bd()
        self.cursor.execute("""
                            SELECT id, nome, editora, tipo_leitura, status 
                            FROM Books 
                            ORDER BY id ASC;
                            """)
        lista = self.cursor.fetchall()
        id = 0

        if len(lista) != 0:
            for i in lista:
                id = i[0]

        if len(self.nome) and len(self.editora) and len(self.tipo_leitura) != 0:
            self.cursor.execute("""
                                       INSERT INTO Books (id, nome, editora, tipo_leitura, status)
                                        VALUES (%s, %s, %s, %s, %s)""",
                                (id + 1, self.nome, self.editora, self.tipo_leitura, self.status))
            self.conn.commit()
            self.desconecta_bd()
            tkinter.messagebox.showinfo("Cadastro dos Livros", "Livro adicionado com sucesso!")
            self.windows_cadastro.destroy()
        else:
            tkinter.messagebox.showinfo("Cadastro dos Livros", "Erro! Livro não adicionado")
            self.desconecta_bd()
            self.windows_cadastro.destroy()

        # self.select_bd()
        # self.limpar_tela()

    # Comprar Livro Lista de Desejos
    def comprarBook(self):
        self.id = self.entry_id_book_dreams.get()
        self.nome = self.entry_name_book_dreams.get()
        self.editora = self.entry_book_editory_dreams.get()
        self.tipo_leitura = self.entry_tipo_leitura_dreams.get()

        self.conectar_bd()
        self.cursor.execute("""
                        INSERT INTO Comprados (id, nome, editora, tipo_leitura)
                        VALUES (%s, %s, %s, %s)
                        """, (self.id, self.nome, self.editora, self.tipo_leitura))

        self.cursor.execute("""
                        UPDATE Books SET status = False
                        WHERE id = %s """, (self.id, ))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()


    def OnDoubleClick(self, event):
        self.limpar_tela()
        self.list.selection()
        for n in self.list.selection():
            col1, col2, col3, col4 = self.list.item(n, 'values')
            self.entry_id_book_dreams.insert(END, col1)
            self.entry_name_book_dreams.insert(END, col2)
            self.entry_book_editory_dreams.insert(END, col3)
            self.entry_tipo_leitura_dreams.insert(END, col4)


    # Excluir Livro Lista de Desejos
    def deleteBook(self):
        self.id = self.entry_id_book_dreams.get()

        self.conectar_bd()
        self.cursor.execute("""
                            UPDATE Books SET status = False 
                            WHERE id = %s """, (self.id, ))
        # self.cursor.execute("""DELETE FROM Control WHERE id = %s """, (self.id, ))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.select_bd()


    # Atualizar Livro Lista de Desejos
    def updateBook(self):
        self.id = self.entry_id_book_dreams.get()
        self.nome = self.entry_name_book_dreams.get()
        self.editora = self.entry_book_editory_dreams.get()
        self.tipo_leitura = self.entry_tipo_leitura_dreams.get()


        self.conectar_bd()
        self.cursor.execute("""
                        UPDATE Books SET nome = %s, editora = %s, tipo_leitura = %s
                        WHERE id = %s""", (self.nome, self.editora, self.tipo_leitura, self.id))
        self.conn.commit()
        self.desconecta_bd()
        self.select_bd()
        self.limpar_tela()


    # Procurar p/nome Lista de Desejos
    def searchName(self):
        self.nome = self.entry_name_book_dreams.get()

        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute("""
                        SELECT id, nome, editora, tipo_leitura 
                        FROM Books
                        WHERE nome = %s AND status = True
                        ORDER BY id ASC
                        """, (self.nome, ))
        lista = self.cursor.fetchall()

        if len(lista) == 0:
            tkinter.messagebox.showinfo("Lista de Desejos", "Nenhum livro encontrado")
        else:
            new_lista = [[0, 0, 0, 0]]
            try:
                for i in lista:
                    self.list.insert("", END, values=i)
            except:
                for k in new_lista:
                    self.list.insert("", END, values=k)
            self.limpar_tela()
            self.desconecta_bd()

    def searchNameComprados(self): # buscar Comprados
        self.selectBdComprados()
        self.conectar_bd()
        self.list2.delete(*self.list2.get_children())

        self.cursor.execute("""
                                SELECT id, nome, editora, tipo_leitura 
                                FROM Comprados
                                ORDER BY nome ASC
                                """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list2.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list2.insert("", END, values=k)
        self.desconecta_bd()

    def searchEditoraComprados(self):
        self.selectBdComprados()
        self.conectar_bd()
        self.list2.delete(*self.list2.get_children())

        self.cursor.execute("""
                                        SELECT id, nome, editora, tipo_leitura 
                                        FROM Comprados
                                        ORDER BY editora ASC
                                        """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list2.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list2.insert("", END, values=k)
        self.desconecta_bd()


    # Ordenar p/editora Lista de Desejos
    def searchEditoraDreams(self):
        self.select_bd()
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute("""   
                            SELECT id, nome, editora, tipo_leitura 
                            FROM Books
                            WHERE status = True
                            ORDER BY editora ASC
                            """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.desconecta_bd()

    def searchTipoLeitura(self):
        self.selectBdComprados()
        self.conectar_bd()
        self.list2.delete(*self.list2.get_children())

        self.cursor.execute("""
                                        SELECT id, nome, editora, tipo_leitura 
                                        FROM Comprados
                                        ORDER BY tipo_leitura ASC
                                        """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list2.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list2.insert("", END, values=k)
        self.desconecta_bd()


    # Ordenar p/Tipo Leitura Lista de Desejos
    def searchTipoLeituraDreams(self):
        self.select_bd()
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute(""" 
                            SELECT id, nome, editora, tipo_leitura 
                            FROM Books
                            WHERE status = True
                            ORDER BY tipo_leitura ASC 
                        """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.desconecta_bd()


    # Ordenar p/nome Lista de Desejos
    def ordenarNameDreams(self):
        self.select_bd()
        self.conectar_bd()
        self.list.delete(*self.list.get_children())

        self.cursor.execute("""  
                            SELECT id, nome, editora, tipo_leitura 
                            FROM Books
                            WHERE status = True
                            ORDER BY nome ASC
                        """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list.insert("", END, values=k)
        self.desconecta_bd()

    def searchIdComprados(self):
        self.selectBdComprados()
        self.conectar_bd()
        self.list2.delete(*self.list2.get_children())

        self.cursor.execute("""
                                        SELECT id, nome, editora, tipo_leitura 
                                        FROM Comprados
                                        ORDER BY id ASC
                                        """)
        lista = self.cursor.fetchall()

        new_lista = [[0, 0, 0, 0]]
        try:
            for i in lista:
                self.list2.insert("", END, values=i)
        except:
            for k in new_lista:
                self.list2.insert("", END, values=k)
        self.desconecta_bd()

    def contarBooks(self, tipo_leitura):
        self.conectar_bd()
        leitura = tipo_leitura
        self.cursor.execute(""" SELECT id, nome, editora, tipo_leitura
                                FROM Comprados
                                WHERE tipo_leitura = %s
                                ORDER BY id ASC
                                """, (leitura, ))
        lista = self.cursor.fetchall()
        print(lista)
        print(len(lista))

        self.desconecta_bd()

        return  len(lista)

class Books(Functions):

    cor_de_fundo = "DarkGray"
    bordas_frames = "Black"
    cor_letras = "Black"
    cor_botoes = "SlateGray"

    def __init__(self):
        self.books = menu
        self.books.title("Controle dos meus livros")
        self.books.geometry("300x200")
        self.books.configure(background=self.cor_de_fundo)
        self.books.resizable(False, False)
        self.frames_books_page()
        self.labels_books_page()
        self.buttons_books_page()
        self.montaTabelas()
        self.montaTabelas2()
        self.center(self.books)
        self.books.mainloop()

    def center(self, page):
        """ FUNÇÃO RESPONSAVEL POR CENTRALIZAR AS PAGES NA TELA"""

        page.withdraw()
        page.update_idletasks()  # Update "requested size" from geometry manager

        x = (page.winfo_screenwidth() - page.winfo_reqwidth()) / 2.5
        y = (page.winfo_screenheight() - page.winfo_reqheight()) / 4
        page.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        page.deiconify()

    def center2(self, page):
        """ FUNÇÃO RESPONSAVEL POR CENTRALIZAR AS PAGES NA TELA"""

        page.withdraw()
        page.update_idletasks()  # Update "requested size" from geometry manager

        x = (page.winfo_screenwidth() - page.winfo_reqwidth()) / 3.2
        y = (page.winfo_screenheight() - page.winfo_reqheight()) / 8.5
        page.geometry("+%d+%d" % (x, y))

        # This seems to draw the window frame immediately, so only call deiconify()
        # after setting correct window position
        page.deiconify()

    def homeCadastro(self):
        self.windows_cadastro = Toplevel(self.books)

        self.windows_cadastro.title("Cadastro dos Livros")
        self.windows_cadastro.geometry("400x400")
        self.windows_cadastro.configure(background= self.cor_de_fundo)
        self.windows_cadastro.resizable(False, False)
        self.center(self.windows_cadastro)

        # Frame
        self.frame_home_cadastro = Frame(self.windows_cadastro,
                                         bd= 4,
                                         bg= self.cor_de_fundo,
                                         highlightbackground= self.bordas_frames,
                                         highlightthickness= 1)
        self.frame_home_cadastro.place(rely= 0.01, relx= 0.02, relwidth= 0.96, relheight= 0.98)

        # Labels
        self.lb_title_home_cadastro = Label(self.frame_home_cadastro, text= "Cadastro de Livros", font= "-weight bold -size 18",
                                            bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_title_home_cadastro.place(rely= 0.01, relx= 0.2, relwidth= 0.58)

        self.lb_name_book = Label(self.frame_home_cadastro, text= "Nome", font= "-weight bold -size 13",
                                  bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_name_book.place(rely= 0.1, relx= 0.03, relwidth= 0.118)

        self.entry_name_book = Entry(self.frame_home_cadastro)
        self.entry_name_book.place(rely= 0.17, relx= 0.028, relwidth= 0.4)

        self.lb_book_editory = Label(self.frame_home_cadastro, text= "Editora", font= "-weight bold -size 13",
                                     bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_book_editory.place(rely= 0.25, relx= 0.03, relwidth= 0.155)

        self.entry_book_editory = Entry(self.frame_home_cadastro)
        self.entry_book_editory.place(rely= 0.32, relx= 0.028, relwidth= 0.4)

        self.lb_tipo_leitura = Label(self.frame_home_cadastro, text= "Tipo de Leitura", font= "-weight bold -size 13",
                                     bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_tipo_leitura.place(rely= 0.4, relx= 0.03, relwidth= 0.315)

        self.entry_tipo_leitura = Combobox(self.frame_home_cadastro, values= ['Literatura', 'Informatica', 'Investimento',
                                                                              'Filosofia', 'Vida Espiritual', 'Historia', 'Economia',
                                                                              'Psicologia', 'Política', 'Biografias', 'Liturgia',
                                                                              'Teologia', 'Doutrina'])
        self.entry_tipo_leitura.place(rely= 0.47, relx= 0.028, relwidth= 0.4)

        # Botões
        self.bt_cadastrar = Button(self.frame_home_cadastro, text= "Adicionar",
                                   background= self.cor_botoes, bd= 4, font= "-weight bold -size 10",
                                   command= self.inserirBook)
        self.bt_cadastrar.place(rely= 0.6, relx= 0.03, relwidth= 0.19)
        # self.windows_cadastro.mainloop()
    def homeListaDesejos(self):
        self.window_list_dreams = Toplevel(self.books)

        self.window_list_dreams.title("Lista de Desejos")
        self.window_list_dreams.geometry("750x700")
        self.window_list_dreams.configure(background= self.cor_de_fundo)
        self.window_list_dreams.resizable(False, False)

        self.center2(self.window_list_dreams)

        # self.window_list_dreams.mainloop()
        # Frame
        self.frame_home_list_dreams = Frame(self.window_list_dreams,
                                            bd= 4,
                                            bg= self.cor_de_fundo,
                                            highlightbackground= self.bordas_frames,
                                            highlightthickness= 1)
        self.frame_home_list_dreams.place(rely= 0.01, relx= 0.02, relwidth= 0.96, relheight= 0.2)

        self.frame_list_of_dreams = Frame(self.window_list_dreams,
                                          bd= 4, bg= self.cor_de_fundo, highlightbackground= self.bordas_frames,
                                          highlightthickness= 1)
        self.frame_list_of_dreams.place(rely= 0.23, relx= 0.02, relwidth= 0.96, relheight= 0.76)

        # Labels
        self.lb_title_list_dreams = Label(self.frame_home_list_dreams, text= "Lista de Desejos", font= "-weight bold -size 18",
                                         bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_title_list_dreams.place(rely= 0.01, relx= 0.37, relwidth= 0.267)

        self.lb_id_book_dreams = Label(self.frame_home_list_dreams, text= "Id", font= "-weight bold -size 13",
                                       bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_id_book_dreams.place(rely= 0.26, relx= 0.01, relwidth= 0.02)

        self.entry_id_book_dreams = Entry(self.frame_home_list_dreams)
        self.entry_id_book_dreams.place(rely= 0.45, relx= 0.01, relwidth= 0.05)

        self.lb_name_book_dreams = Label(self.frame_home_list_dreams, text= "Nome", font= "-weight bold -size 13",
                                         bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_name_book_dreams.place(rely= 0.26, relx= 0.1, relwidth= 0.065)

        self.entry_name_book_dreams = Entry(self.frame_home_list_dreams)
        self.entry_name_book_dreams.place(rely= 0.45, relx= 0.1, relwidth= 0.2)

        self.lb_book_editory_dreams = Label(self.frame_home_list_dreams, text= "Editora", font= "-weight bold -size 13",
                                            bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_book_editory_dreams.place(rely= 0.26, relx= 0.34, relwidth= 0.082)

        self.entry_book_editory_dreams = Entry(self.frame_home_list_dreams)
        self.entry_book_editory_dreams.place(rely= 0.45, relx= 0.34, relwidth= 0.18)

        self.lb_tipo_leitura_dreams = Label(self.frame_home_list_dreams, text= "Tipo de Leitura", font= "-weight bold -size 13",
                                            bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_tipo_leitura_dreams.place(rely= 0.26, relx= 0.56, relwidth= 0.17)

        self.entry_tipo_leitura_dreams = Entry(self.frame_home_list_dreams)
        self.entry_tipo_leitura_dreams.place(rely= 0.45, relx= 0.56, relwidth= 0.2)

        # Botôes

        self.bt_comprar = Button(self.frame_home_list_dreams, text= "Comprar",
                                 background= self.cor_botoes, bd= 4,
                                 font= "-weight bold -size 10", command= self.comprarBook)
        self.bt_comprar.place(rely= 0.71, relx= 0.01, relwidth= 0.1)

        self.bt_alterar = Button(self.frame_home_list_dreams, text= "Alterar", background= self.cor_botoes, bd= 4,
                                 font= "-weight bold -size 10", command= self.updateBook)
        self.bt_alterar.place(rely= 0.71, relx= 0.14, relwidth= 0.1)

        self.bt_buscar_books = Button(self.frame_home_list_dreams, text= "Buscar P/Nome", background= self.cor_botoes, bd= 4,
                                      font= "-weight bold -size 10", command= self.searchName)
        self.bt_buscar_books.place(rely= 0.71, relx= 0.61, relwidth= 0.15)

        self.bt_ordenar_books = Button(self.frame_home_list_dreams, text= "Ordenar P/Nome", background= self.cor_botoes,
                                       bd= 4, font= "-weight bold -size 10", command= self.ordenarNameDreams)
        self.bt_ordenar_books.place(rely= 0.1, relx= 0.77, relwidth= 0.23)

        self.bt_buscar_editora_dreams = Button(self.frame_home_list_dreams, text= "Ordenar P/Editora",
                                               background= self.cor_botoes, bd= 4, font= "-weight bold -size 10",
                                               command= self.searchEditoraDreams)
        self.bt_buscar_editora_dreams.place(rely= 0.4, relx= 0.77, relwidth= 0.23)

        self.bt_buscar_tipo_dreams = Button(self.frame_home_list_dreams, text= "Ordenar P/Tipo Leitura",
                                            background= self.cor_botoes, bd= 4, font= "-weight bold -size 10",
                                            command= self.searchTipoLeituraDreams)
        self.bt_buscar_tipo_dreams.place(rely= 0.71, relx= 0.77, relwidth= 0.23)

        self.bt_excluir_books = Button(self.frame_home_list_dreams, text= "Excluir", background= self.cor_botoes, bd= 4,
                                       font= "-weight bold -size 10", command= self.deleteBook)
        self.bt_excluir_books.place(rely= 0.71, relx= 0.27, relwidth= 0.1)

        # Lista
        self.list_frame()
        self.select_bd()

    def homeBooksCompradosInformation(self):
        self.window_information = Toplevel(self.window_book_comprados)

        self.window_information.title("Livros Comprados - Relatorio")
        self.window_information.geometry("300x300")
        self.window_information.configure(background= self.cor_de_fundo)
        self.window_information.resizable(False, False)

        self.center(self.window_information)

        # Frame
        self.frame_home_books_information = Frame(self.window_information, bd= 4, bg= self.cor_de_fundo,
                                                  highlightbackground= self.bordas_frames,
                                                  highlightthickness= 1)
        self.frame_home_books_information.place(rely= 0.02, relx= 0.02, relwidth= 0.96, relheight= 0.96)

        # Labels
        self.lb_relatorys = Label(self.frame_home_books_information, text="Relatorio",
                                          font="-weight bold -size 18",
                                          bg= self.cor_de_fundo, fg=self.cor_letras)
        self.lb_relatorys.place(rely= 0.01, relx= 0.31, relwidth= 0.375)


        self.lb_vida_espiritual = Label(self.frame_home_books_information, text= "Vida Espiritual: ",
                                        font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_vida_espiritual.place(rely= 0.13, relx= 0.01, relwidth= 0.36)

        self.lb_vida = Label(self.frame_home_books_information, text= self.contarBooks("Vida Espiritual"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_vida.place(rely= 0.13, relx= 0.37, relwidth= 0.11)


        self.lb_literatura = Label(self.frame_home_books_information, text= "Literatura: ",
                                   font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_literatura.place(rely= 0.13, relx= 0.55, relwidth= 0.25)

        self.lb_lit = Label(self.frame_home_books_information, text= self.contarBooks("Literatura"),
                            font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_lit.place(rely= 0.13, relx= 0.83, relwidth= 0.11)

        self.lb_informatica = Label(self.frame_home_books_information, text= "Informática: ",
                                    font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_informatica.place(rely= 0.24, relx= 0.01, relwidth= 0.29)

        self.lb_info = Label(self.frame_home_books_information, text= self.contarBooks("Informática"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_info.place(rely= 0.24, relx= 0.33, relwidth= 0.11)

        self.lb_investimento = Label(self.frame_home_books_information, text= "Investimentos: ",
                                     font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_investimento.place(rely= 0.24, relx= 0.55, relwidth= 0.34)

        self.lb_invest = Label(self.frame_home_books_information, text= self.contarBooks("Investimentos"),
                               font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_invest.place(rely= 0.24, relx= 0.88, relwidth= 0.11)

        self.lb_filosofia = Label(self.frame_home_books_information, text= "Filosofia: ",
                                  font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_filosofia.place(rely= 0.35, relx= 0.01, relwidth= 0.22)

        self.lb_filo = Label(self.frame_home_books_information, text= self.contarBooks("Filosofia"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_filo.place(rely= 0.35, relx= 0.33, relwidth= 0.11)

        self.lb_historia = Label(self.frame_home_books_information, text= "História: ",
                                 font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_historia.place(rely= 0.35, relx= 0.55, relwidth= 0.2)

        self.lb_hist = Label(self.frame_home_books_information, text= self.contarBooks("História"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_hist.place(rely= 0.35, relx= 0.83, relwidth= 0.11)

        self.lb_economia = Label(self.frame_home_books_information, text= "Economia: ",
                                 font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_economia.place(rely= 0.46, relx= 0.01, relwidth= 0.255)

        self.lb_econ = Label(self.frame_home_books_information, text= self.contarBooks("Economia"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_econ.place(rely= 0.46, relx= 0.33, relwidth= 0.11)

        self.lb_psicologia = Label(self.frame_home_books_information, text= "Psicologia: ",
                                   font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_psicologia.place(rely= 0.46, relx= 0.55, relwidth= 0.265)

        self.lb_psic = Label(self.frame_home_books_information, text= self.contarBooks("Psicologia"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_psic.place(rely= 0.46, relx= 0.83, relwidth= 0.11)

        self.lb_politica = Label(self.frame_home_books_information, text= "Política: ",
                                 font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_politica.place(rely= 0.57, relx= 0.01, relwidth= 0.2)

        self.lb_polit = Label(self.frame_home_books_information, text= self.contarBooks("Política"),
                              font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_polit.place(rely= 0.57, relx= 0.33, relwidth= 0.11)

        self.lb_biografia = Label(self.frame_home_books_information, text= "Biografia: ",
                                  font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_biografia.place(rely= 0.57, relx= 0.55, relwidth= 0.233)

        self.lb_biog = Label(self.frame_home_books_information, text= self.contarBooks("Biografia"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_biog.place(rely= 0.57, relx= 0.83, relwidth= 0.11)

        self.lb_liturgia = Label(self.frame_home_books_information, text= "Liturgia: ",
                                 font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_liturgia.place(rely= 0.68, relx= 0.01, relwidth= 0.205)

        self.lb_lit = Label(self.frame_home_books_information, text= self.contarBooks("Liturgia"),
                            font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_lit.place(rely= 0.68, relx= 0.33, relwidth= 0.11)

        self.lb_teologia = Label(self.frame_home_books_information, text= "Teologia: ",
                                 font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_teologia.place(rely= 0.68, relx= 0.55, relwidth= 0.23)

        self.lb_teo = Label(self.frame_home_books_information, text= self.contarBooks("Teologia"),
                            font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_teo.place(rely= 0.68, relx= 0.83, relwidth= 0.11)

        self.lb_doutrina = Label(self.frame_home_books_information, text= "Doutrina: ",
                                 font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_doutrina.place(rely= 0.79, relx= 0.55, relwidth= 0.223)

        self.lb_dout = Label(self.frame_home_books_information, text= self.contarBooks("Doutrina"),
                             font= "-weight bold -size 10", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_dout.place(rely= 0.79, relx= 0.83, relwidth= 0.11)

    def homeBooksComprados(self):
        self.window_book_comprados = Toplevel(self.books)

        self.window_book_comprados.title("Livros Comprados")
        self.window_book_comprados.geometry("750x700")
        self.window_book_comprados.configure(background=self.cor_de_fundo)
        self.window_book_comprados.resizable(False, False)

        self.center2(self.window_book_comprados)

        # Frames
        self.frame_home_books_comprados = Frame(self.window_book_comprados,
                                            bd=4,
                                            bg=self.cor_de_fundo,
                                            highlightbackground=self.bordas_frames,
                                            highlightthickness=1)
        self.frame_home_books_comprados.place(rely=0.01, relx=0.02, relwidth=0.96, relheight=0.13)

        self.frame_list_books_comprados = Frame(self.window_book_comprados,
                                                bd= 4, bg= self.cor_de_fundo, highlightbackground= self.bordas_frames,
                                                highlightthickness= 1)
        self.frame_list_books_comprados.place(rely= 0.16, relx= 0.02, relwidth= 0.96, relheight= 0.83)

        # Labels
        self.lb_title_books_comprados = Label(self.frame_home_books_comprados, text="Livros Comprados",
                                          font="-weight bold -size 18",
                                          bg= self.cor_de_fundo, fg=self.cor_letras)
        self.lb_title_books_comprados.place(rely=0.01, relx=0.35, relwidth=0.3)

        # Botôes
        self.bt_buscar_nome = Button(self.frame_home_books_comprados, text="Buscar Nome",
                                 background=self.cor_botoes, bd=4,
                                 font="-weight bold -size 10", command= self.searchNameComprados)
        self.bt_buscar_nome.place(rely=0.49, relx=0.01, relwidth=0.15)

        self.bt_buscar_editora = Button(self.frame_home_books_comprados, text= "Buscar Editora",
                                        background= self.cor_botoes, bd= 4,
                                        font= "-weight bold -size 10", command= self.searchEditoraComprados)
        self.bt_buscar_editora.place(rely= 0.49, relx= 0.18, relwidth= 0.15)

        self.bt_buscar_tipo = Button(self.frame_home_books_comprados, text= "Buscar Tipo Leitura",
                                     background= self.cor_botoes, bd= 4,
                                     font= "-weight bold -size 10", command= self.searchTipoLeitura)
        self.bt_buscar_tipo.place(rely= 0.49, relx= 0.35, relwidth= 0.19)

        self.bt_buscar_id = Button(self.frame_home_books_comprados, text= "Buscar Id",
                                   background= self.cor_botoes, bd= 4,
                                   font= "-weight bold -size 10", command= self.searchIdComprados)
        self.bt_buscar_id.place(rely= 0.49, relx= 0.56, relwidth= 0.13)

        self.bt_informacoes = Button(self.frame_home_books_comprados, text= "Relatorio", background= self.cor_botoes,
                                     bd= 4, font= "-weight bold -size 10", command= self.homeBooksCompradosInformation)
        self.bt_informacoes.place(rely= 0.49, relx= 0.87, relwidth= 0.11)

        # Lista
        self.listFrameBooksComprados()
        self.selectBdComprados()

    def frames_books_page(self):

        self.frame_book_information = Frame(self.books,
                                       bd= 4,
                                       bg= self.cor_de_fundo,
                                       highlightbackground= self.bordas_frames,
                                       highlightthickness= 1)
        self.frame_book_information.place(rely= 0.01, relx= 0.02, relwidth= 0.96, relheight= 0.98)

    def labels_books_page(self):
        self.lb_title = Label(self.frame_book_information, text= "Minha Biblioteca", font= "-weight bold -size 18",
                              bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_title.place(rely= 0.1, relx= 0.16, relwidth= 0.7)

    def buttons_books_page(self):

        self.bt_books_cadastrar = Button(self.frame_book_information, text= "Cadastrar", background= self.cor_botoes, bd= 6,
                                          font= "-weight bold -size 10", command= self.homeCadastro)
        self.bt_books_cadastrar.place(rely= 0.4, relx= 0.02, relwidth= 0.28, relheight= 0.25)

        self.bt_dream_list = Button(self.frame_book_information, text= "Lista de\nDesejos", background= self.cor_botoes, bd= 6,
                                    font= "-weight bold -size 10", command= self.homeListaDesejos)
        self.bt_dream_list.place(rely= 0.4, relx= 0.37, relwidth= 0.26, relheight= 0.25)

        self.bt_my_books = Button(self.frame_book_information, text= "Minhas \nCompras", background= self.cor_botoes, bd= 6,
                                  font= "-weight bold -size 10", command= self.homeBooksComprados)
        self.bt_my_books.place(rely= 0.4, relx= 0.7, relwidth= 0.26, relheight= 0.25)

    # Lista do frame da Lista de Desejos
    def list_frame(self):
    #
       self.list = ttk.Treeview(self.frame_list_of_dreams, height=3,
                                columns=("col1", "col2", "col3", "col4"))
    #
       self.list.heading("#0", text="")
       self.list.heading("#1", text="Id")
       self.list.heading("#2", text="Nome")
       self.list.heading("#3", text="Editora")
       self.list.heading("#4", text="Tipo de Leitura")
    #
       self.list.column("#0", width=1)
       self.list.column("#1", width=1)
       self.list.column("#2", width=180)
       self.list.column("#3", width=120)
       self.list.column("#4", width=150)
    #
       self.list.place(rely=0.01, relx=0.01, relwidth=0.97, relheight=0.98)
    #
       self.scrollList = Scrollbar(self.frame_list_of_dreams, orient="vertical")
       self.list.configure(yscroll=self.scrollList.set)
       self.scrollList.place(relx=0.97, rely=0.01, relwidth=0.02, relheight=0.98)
       self.list.bind("<Double-1>", self.OnDoubleClick)

    def listFrameBooksComprados(self):
        self.list2 = ttk.Treeview(self.frame_list_books_comprados, height=3,
                                 columns=("col1", "col2", "col3", "col4"))
        #
        self.list2.heading("#0", text="")
        self.list2.heading("#1", text="Id")
        self.list2.heading("#2", text="Nome")
        self.list2.heading("#3", text="Editora")
        self.list2.heading("#4", text="Tipo de Leitura")
        #
        self.list2.column("#0", width=1)
        self.list2.column("#1", width=1)
        self.list2.column("#2", width=180)
        self.list2.column("#3", width=120)
        self.list2.column("#4", width=150)
        #
        self.list2.place(rely=0.01, relx=0.01, relwidth=0.97, relheight=0.98)
        #
        self.scrollList = Scrollbar(self.frame_list_books_comprados, orient="vertical")
        self.list2.configure(yscroll=self.scrollList.set)
        self.scrollList.place(relx=0.97, rely=0.01, relwidth=0.02, relheight=0.98)

Books()