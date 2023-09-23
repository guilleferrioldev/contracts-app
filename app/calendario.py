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

        self.dateframe = DateFrame(self, 1.0, 0.7, "")
        self.calendar.calevent_create(self.date, "Hoy", tags="Today")
        self.calendar.tag_config("Today", background = ctk.ThemeManager.theme["CTkButton"]["fg_color"][1])
        

        self.calendar.bind("<<CalendarSelected>>", lambda event :  self.show_date())

        self.grid(row = row, column = column, columnspan = columnspan,padx = padx, pady = pady, sticky = sticky)
    
    def show_date(self):
        if self.dateframe.text != self.calendar.get_date():
            self.dateframe.destroy()
            self.dateframe = DateFrame(self, 1.0, 0.7, f"{self.calendar.get_date()}")
            
            date = self.calendar.get_date().split("-")
            
            if date[0] == "01":
                date[0] = "1"
            elif date[0] == "02":
                date[0] = "2"
            elif date[0] == "03":
                date[0] = "3"
            elif date[0] == "04":
                date[0] = "4"
            elif date[0] == "05":
                date[0] = "5"
            elif date[0] == "06":
                date[0] = "6"
            elif date[0] == "07":
                date[0] = "7"
            elif date[0] == "08":
                date[0] = "8"
            elif date[0] == "09":
                date[0] = "9"
                           
            if date[1] == "01":
                date[1] = "Enero"
            elif date[1] == "02":
                date[1] = "Febrero"
            elif date[1] == "03":
                date[1] = "Marzo"
            elif date[1] == "04":
                date[1] = "Abril"
            elif date[1] == "05":
                date[1] = "Mayo"
            elif date[1] == "06":
                date[1] = "Junio"
            elif date[1] == "07":
                date[1] = "Julio"
            elif date[1] == "08":
                date[1] = "Agosto"
            elif date[1] == "09":
                date[1] = "Septiembre"
            elif date[1] == "10":
                date[1] = "Octubre"
            elif date[1] == "11":
                date[1]= "Noviembre"
            elif date[1] == "12":
                date[1] = "Diciembre"

            date = "/".join(date)
            
            conn = sqlite3.connect("contratos.db")
            cursor = conn.cursor()

            instruccion = f"SELECT proveedor, fecha_de_vencimiento FROM Contratos WHERE fecha_de_vencimiento = '{date}'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

            conn.commit()
            conn.close()

            if datos != []:
                self.dateframe.animate()

            i = 0 
            while i < len(datos):
                InfoFrame(self.dateframe.scroll_frame, datos[i][0])
                i += 1
                

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
   
class DateFrame(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, text):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True

        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15, "bold")

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.03, relwidth = 0.9, relheight = 0.05)

        self.scroll_frame = ctk.CTkScrollableFrame(self)
        self.scroll_frame.place(relx = 0.05, rely = 0.1,relwidth = 0.9,  relheight = 0.8)

        self.back_button = ctk.CTkButton(self, text = "Atrás", command = self.animate)
        self.back_button.place(relx = 0.4, rely = 0.92, relwidth = 0.2, relheight = 0.05)
        
        # layout 
        self.place(relx = self.start_pos, rely = 0.05, relwidth = 0.3, relheight = 0.93)

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
        else:
            self.animate_backwards()


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.08 
            self.place(relx = 0.4, rely = 0.05, relwidth = 0.59, relheight = 0.93)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.08
            self.place(relx = self.pos, rely = 0.05, relwidth = 0.59, relheight = 0.93)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

class InfoFrame(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         height = 100,
                         fg_color =  "white")
        
        self.text = text
        
        self.proveedor = ctk.CTkLabel(self, text = self.text, font = ctk.CTkFont("Helvetica", 15), anchor = "w")
        self.proveedor.place(relx = 0.05, rely = 0.3, relwidth = 0.8, relheight = 0.4)

        self.pack(expand= True, fill = "x", padx = 5, pady = 5)
