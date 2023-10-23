import customtkinter as ctk
from datetime import datetime, timedelta
from datos_contratos import Datos
import os
import sqlite3

class MessageDeleter(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        #self.width = abs(start_pos - end_pos)
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        self.today = datetime.now().date()
        self.a_day = timedelta(days=1)
        self.a_week = timedelta(days=7)
        self.two_weeks = timedelta(days=15)
        self.a_month = timedelta(days=30)

        # layout
        self.font = ctk.CTkFont("Helvetica", 15)

        self.text = ctk.CTkLabel(self, text = "Aviso de vencimiento", anchor = "w", font = self.font)
        self.text.place(relx = 0.05, rely = 0.05, relwidth = 0.8, relheight = 0.1)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.place(relx = 0.05, rely = 0.15, relwidth = 0.9, relheight = 0.7)

        self.button = ctk.CTkButton(self, text = "OK", command = self.animate)
        self.button.place(relx = 0.45, rely = 0.86, relwidth = 0.1, relheight = 0.1)
        
        self.comp = 0
        self.comprobation()
        
        # layout 
        self.place(relx = self.start_pos, rely = 0.25, relwidth = 0.6, relheight = 0.4)
    
    def comprobation(self):
        dicc = self.convert_dict()
        correct_values = {key:(value-self.today) for key, value in sorted(dicc.items(), key= lambda x: x[1]) if (value - self.today) < timedelta(days=30)}
        
        for key, value in correct_values.items():
            Label(self.scroll, key, value)
        
        if len(correct_values):
            self.comp = 1
        
        
    def convert_dict(self):
        dates = dict(self.extract_from_database())
        
        for key, value in dates.items():
            dates[key] = self.convert(self.change_date(value))
        
        return dates
    

    def extract_from_database(self):
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
        
        instruccion = "SELECT proveedor, fecha_de_vencimiento from Contratos"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()

        return datos
        
    def change_date(self, date):
        date = date.split("/")

        if date[1] == "Enero":
            month = "Jan"
        elif date[1] == "Febrero":
            month = "Feb"
        elif date[1] == "Marzo":
            month = "Mar"
        elif date[1] == "Abril":
            month = "Apr"
        elif date[1] == "Mayo":
            month = "May"
        elif date[1] == "Junio":
            month = "Jun"
        elif date[1] == "Julio":
            month = "Jul"
        elif date[1] == "Agosto":
            month = "Aug"
        elif date[1] == "Septiembre":
            month = "Sep"
        elif date[1] == "Octubre":
            month = "Oct"
        elif date[1] == "Noviembre":
            month = "Nov"
        elif date[1] == "Diciembre":
            month = "Dec"
        
        date[1] = month

        return "/".join(date)

    def convert(self, date_time):
        format = '%d/%b/%Y'
        datetime_str = datetime.strptime(date_time, format)
        
        return datetime_str.date()

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
        else:
            self.animate_backwards()
            self.tkraise()

    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = 0.2, rely = 0.25, relwidth = 0.6, relheight = 0.4)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.25, relwidth = 0.6, relheight = 0.4)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True


class Label(ctk.CTkFrame):
    def __init__(self, master, text, date):
        super().__init__(master = master, fg_color = "white", height = 50)
        self.font = ctk.CTkFont("Helvetica", 15)
        
        self.text = text
        self.date = str(date).split()[0] + " días"

        self.text_label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.text_label.place(relx = 0.05, rely = 0.25, relwidth = 0.8)
        
        self.date_label = ctk.CTkLabel(self, text = self.date , anchor = "w", font = self.font)
        self.date_label.place(relx = 0.85, rely = 0.25, relwidth = 0.2)

        self.bind("<Button>", lambda event: Datos(self, self.text, "warning"))
        self.text_label.bind("<Button>", lambda event: Datos(self, self.text, "warning"))
        self.date_label.bind("<Button>", lambda event: Datos(self, self.text, "warning"))

        self.pack(expand = True, fill = "x", pady = 5, padx = 5)



