from calendar import isleap
from datetime import datetime
from tkinter import *
from tkinter import ttk
import sqlite3
import psycopg2
import pandas as pd

menu = Tk()

class Books():

    cor_de_fundo = "BurlyWood"
    bordas_frames = "Black"
    cor_letras = "Black"
    cor_botoes = "SlateGray"

    def __init__(self):
        self.menu = menu
        self.home_page()
        self.frames_home_page()
        self.labels_home_page()
        self.buttons_home_page()
        self.center(self.menu)
        self.menu.mainloop()

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

    def books_page(self):
        self.books = Toplevel(self.menu)
        self.books.title("Controle dos meus livros")
        self.books.geometry("600x500")
        self.books.configure(background= self.cor_de_fundo)
        self.books.resizable(False, False)
        self.frames_books_page()
        self.labels_books_page()
        self.buttons_books_page()
        self.center(self.books)
        self.books.mainloop()

    def courses_page(self):
        self.courses = Toplevel(self.menu)
        self.courses.title("Controle dos meus cursos")
        self.courses.geometry("400x400")
        self.courses.configure(background= self.cor_de_fundo)
        self.courses.resizable(False, False)
        self.center(self.courses)
        self.courses.mainloop()

    def home_page(self):
        self.menu.title("Controle dos meus livros")
        self.menu.geometry("250x250")
        self.menu.configure(background= self.cor_de_fundo)
        self.menu.resizable(False, False)

    def frames_home_page(self):

        self.frame_titulo = Frame(self.menu,
                                  bd= 4,
                                  bg= self.cor_de_fundo,
                                  highlightbackground= self.bordas_frames,
                                  highlightthickness= 0)
        self.frame_titulo.place(rely= 0.01, relx= 0.01, relwidth= 0.98, relheight= 0.9)

    def labels_home_page(self):

        self.lb_title = Label(self.frame_titulo, text= "CURSOS E LIVROS", font= "-weight bold -size 17",
                              bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_title.place(rely= 0.1, relx= 0.07, relwidth= 0.9)

    def buttons_home_page(self):

        self.bt_cursos = Button(self.frame_titulo, text= "Cursos", background= self.cor_botoes, bd= 6, font= "-weight bold -size 13", command= self.courses_page)
        self.bt_cursos.place(rely= 0.5, relx= 0.07, relwidth= 0.3)

        self.bt_books = Button(self.frame_titulo, text= "Livros", background= self.cor_botoes, bd= 6, font= "-weight bold -size 13", command= self.books_page)
        self.bt_books.place(rely= 0.5, relx= 0.6, relwidth= 0.3)

    def frames_books_page(self):

        self.frame_book_titulo = Frame(self.books,
                                       bd= 4,
                                       bg= self.cor_de_fundo,
                                       highlightbackground= self.bordas_frames,
                                       highlightthickness= 1)
        self.frame_book_titulo.place(rely= 0.01, relx= 0.022, relwidth= 0.95, relheight= 0.15)

        self.frame_book_information = Frame(self.books,
                                            bd= 4,
                                            bg= self.cor_de_fundo,
                                            highlightbackground= self.bordas_frames,
                                            highlightthickness= 1)
        self.frame_book_information.place(rely= 0.17, relx= 0.022, relwidth= 0.95, relheight= 0.2)

    def labels_books_page(self):
        self.lb_title = Label(self.frame_book_titulo, text= "MEUS LIVROS", font= "-weight bold -size 20",
                              bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_title.place(rely= 0.2, relx= 0.07, relwidth= 0.9)

        self.lb_book_name = Label(self.frame_book_information, text= "Nome", font= "-weight bold -size 15",
                                  bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_book_name.place(rely= 0.01, relx= 0.025, relwidth= 0.1)

        self.entry_book_name = Entry(self.frame_book_information)
        self.entry_book_name.place(rely= 0.3, relx= 0.025, relwidth= 0.12)

        self.lb_book_publish_company = Label(self.frame_book_information, text= "Editora", font= "-weight bold -size 15",
                                             bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_book_publish_company.place(rely= 0.01, relx= 0.18, relwidth= 0.12)

        self.entry_book_publish_company = Entry(self.frame_book_information)
        self.entry_book_publish_company.place(rely= 0.3, relx= 0.18, relwidth= 0.12)

        self.lb_author = Label(self.frame_book_information, text= "Autor", font= "-weight bold -size 15", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_author.place(rely= 0.01, relx= 0.34, relwidth= 0.1)

        self.entry_author = Entry(self.frame_book_information)
        self.entry_author.place(rely= 0.3, relx= 0.34, relwidth= 0.12)


        self.lb_pages = Label(self.frame_book_information, text= "Paginas", font= "-weight bold -size 15", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_pages.place(rely= 0.01, relx= 0.5, relwidth= 0.13)

        self.entry_pages = Entry(self.frame_book_information)
        self.entry_pages.place(rely= 0.3, relx= 0.5, relwidth= 0.08)


        self.lb_dt_initial = Label(self.frame_book_information, text= "Inicio", font= "-weight bold -size 15", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_dt_initial.place(rely= 0.01, relx= 0.65, relwidth= 0.1)

        self.entry_dt_initial = Entry(self.frame_book_information)
        self.entry_dt_initial.place(rely= 0.3, relx= 0.65, relwidth= 0.11)


        self.lb_dt_end = Label(self.frame_book_information, text= "Fim", font= "-weight bold -size 15", bg= self.cor_de_fundo, fg= self.cor_letras)
        self.lb_dt_end.place(rely= 0.01, relx= 0.8, relwidth= 0.057)

        self.entry_dt_end = Entry(self.frame_book_information)
        self.entry_dt_end.place(rely= 0.3, relx= 0.8, relwidth= 0.11)

    def buttons_books_page(self):

        self.bt_books_cadastrar = Button(self.frame_book_information, text= "Inserir", background= self.cor_botoes, bd= 6, font= "-weight bold -size 13")
        self.bt_books_cadastrar.place(rely= 0.57, relx= 0.02, relwidth= 0.12, relheight= 0.35)

        self.bt_books_update = Button(self.frame_book_information, text= "Alterar", background= self.cor_botoes, bd= 6, font= "-weight bold -size 13")
        self.bt_books_update.place(rely= 0.57, relx= 0.18, relwidth= 0.12, relheight= 0.35)

        self.bt_books_delete = Button(self.frame_book_information, text= "Excluir", background= self.cor_botoes, bd= 6, font= "-weight bold -size 13")
        self.bt_books_delete.place(rely= 0.57, relx= 0.335, relwidth= 0.12, relheight= 0.35)
    def list_frame(self):

        self.list = ttk.Treeview()
Books()