import customtkinter as ctk
from tkcalendar import Calendar
import datetime
import sqlite3

class Calendario(ctk.CTkFrame):
    def __init__(self, master, row, column, columnspan, padx, pady, sticky):
        super().__init__(master = master)

        self.date = datetime.datetime.now().date()


        self.calendar = Calendar(self, selectmode = "day", year = self.date.year, month = self.date.month, day = self.date.day,
                                 background = ctk.ThemeManager.theme["CTkButton"]["fg_color"][0], date_pattern = "dd-mm-y")
        

        self.calendar.place(relx = 0.005, rely = 0.005, relwidth = 0.99, relheight = 0.99)
        
        self.grad_date()

        self.calendar.calevent_create(self.date, "Hoy", tags="Today")
        self.calendar.tag_config("Today", background = ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        
        self.calendar.bind("<<CalendarSelected>>", lambda event :  print(self.calendar.get_date()))

        self.grid(row = row, column = column, columnspan = columnspan,padx = padx, pady = pady, sticky = sticky)

    def grad_date(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = f"SELECT proveedor, fecha_de_vencimiento FROM Contratos"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()
        
        date_intermediate = []
        i = 0 
        while i < len(datos):
            date = tuple(datos[i][1].split("/"))
            date_intermediate.append(date)
            i += 1
        
        date_result = []
        i = 0 
        while i < len(date_intermediate):
            month = ""
            if date_intermediate[i][1] == "Enero":
                month = "Jan"
            elif date_intermediate[i][1] == "Febrero":
                month = "Feb"
            elif date_intermediate[i][1] == "Marzo":
                month = "Mar"
            elif date_intermediate[i][1] == "Abril":
                month = "Apr"
            elif date_intermediate[i][1] == "Mayo":
                month = "May"
            elif date_intermediate[i][1] == "Junio":
                month = "Jun"
            elif date_intermediate[i][1] == "Julio":
                month = "Jul"
            elif date_intermediate[i][1] == "Agosto":
                month = "Aug"
            elif date_intermediate[i][1] == "Septiembre":
                month = "Sep"
            elif date_intermediate[i][1] == "Octubre":
                month = "Oct"
            elif date_intermediate[i][1] == "Noviembre":
                month = "Nov"
            elif date_intermediate[i][1] == "Diciembre":
                month = "Dec"

            date = date_intermediate[i][0] + "/" + month + "/" + date_intermediate[i][2]
            date_result.append(date)
            i += 1

        i = 0 
        while i < len(date_result):
            conv = self.convert(date_result[i])
            self.calendar.calevent_create(conv, datos[i][0], tags="Contrato")
            self.calendar.tag_config("Contrato", background = "red")
            i += 1

 
    # Function to convert string to datetime
    def convert(self, date_time):
        format = '%d/%b/%Y'
        datetime_str = datetime.datetime.strptime(date_time, format)
 
        return datetime_str
   

