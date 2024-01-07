import customtkinter as ctk
from contracts import Contracts
from calendario import Calendario
from new import NewButton, SlidePanel
from sorting import Sort
from message import Message
from deleter_contracts import MessageDeleter
import sqlite3
import datetime 

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # setup
        ctk.set_appearance_mode("System")
        self.title("GECON")
        self.width = int(self.winfo_screenwidth()/1.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}") 
        #self.geometry("1920x1080") 
        self.minsize(self.width,self.height)
        self.maxsize(self.winfo_screenwidth(), self.winfo_screenheight())
        self.resizable(True, True)
        
        self.main_frame = ctk.CTkFrame(master=self)
        self.main_frame.pack(expand=True, fill="both", padx=10, pady=10)

        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(2, weight=1)
        self.font = ctk.ThemeManager.theme["CTkFont"]["family"]
         
        self.label = ctk.CTkLabel(master=self.main_frame, text="GECON", font=(self.font,25,"bold"))
        self.label.grid(row=0, column=0, padx=20, pady=10)
        
        self.create_database()
        self.delete_date_contracts()
        font = ctk.CTkFont("Helvetica", 15)

        # layout
        self.comprobation = MessageDeleter(self, 1.0, 0.7)
        if self.comprobation.comp:
            self.comprobation.animate()
        
        self.create_search()
        
        # Sort Option Menu
        self.sort_var = ctk.StringVar(value = "Proveedor")
        self.values = ["Proveedor","Área","Fecha contrato", "Fecha vencimiento","Objeto", "Importe total", "Servicios", "Aut.firm factura"]
        self.sort = Sort(master = self.main_frame, 
                    width = 140,
                    values = self.values,
                    row = 0,
                    column = 1,
                    pady = 10, 
                    sticky = "e",
                    variable = self.sort_var,
                    command = self.option_sort)



        # Insert contracts panel
        self.slide = SlidePanel(self.main_frame,0,-0.98)

        self.new = NewButton(master = self.main_frame,
                    text = "+",
                    width = 30,
                    row = 0,
                    column = 2, 
                    padx = 10,
                    pady = 10,
                    sticky = "e",
                    command = self.animate_new)


        self.guardar_button = ctk.CTkButton(self.slide, text = "Guardar",font = font, command = self.save, hover_color = "green")
        self.guardar_button.place(relx = 0.42, rely = 0.94, relwidth=0.11, relheight = 0.043) 
        
        self.option_type = ctk.CTkSegmentedButton(self.main_frame, values=["Contratos","Calendario"], command = self.switch_frame)
        self.option_type.set("Contratos")
        self.option_type.grid(row=1, column=0, columnspan=3, padx=10, pady=10, sticky="ew")
         

        self.contracts = Contracts(master = self.main_frame, 
                    row=2, 
                    column=0, 
                    columnspan=3,
                    padx=10, 
                    pady=(0,10),
                    sticky="nsew")        

        self.mainloop() 
    
    def animate_new(self):
        if self.option_type.get() == "Calendario":
            self.switch_frame("Contratos")
            self.option_type.set("Contratos")
        self.slide.animate()

    def save(self):  
        self.slide.confirmar()
        #self.slide.insert_database()
        #self.buscar()
 
    def create_search(self):
        self.search = ctk.CTkEntry(master = self.main_frame, placeholder_text = "Buscar", width = 250)
        self.search.grid(row = 0,
                      column = 1,
                      padx = 150,
                      pady = 10, 
                      sticky = "e")
        self.search.bind("<KeyRelease>", lambda e: self.buscar())



    def option_sort(self, choice):
        for child in self.contracts.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        
        self.contracts.readOrdered(self.search.get(), choice)


    # Method to switch between frames
    def switch_frame(self, type_):
        if type_ == "Contratos":
            self.contracts = Contracts(master = self.main_frame, 
                                    row=2, 
                                    column=0, 
                                    columnspan=3,
                                    padx=10, 
                                    pady=(0,10),
                                    sticky="nsew")
            
            self.search.configure(state = "normal")
            self.sort.configure(state = "normal")
    

        elif type_ == "Calendario":
            self.calendar = Calendario(master = self.main_frame, 
                            row=2, 
                            column=0, 
                            columnspan=3,
                            padx=10, 
                            pady=(0,10),
                            sticky="nsew")
            
            self.search.destroy()
            self.create_search()
            self.search.configure(state = "disabled") 
            self.sort.set("Proveedor")
            self.sort.configure(state = "disabled")
    
    def buscar(self):
        for child in self.contracts.winfo_children():
             if child.widgetName == "frame":
                child.destroy()
        
        self.contracts.readOrdered(self.search.get(), self.sort_var.get())

            
    def create_database(self):
        conn  = sqlite3.connect("contratos.db")
        

        cursor = conn.cursor()
        
        table_create_query = ''' CREATE TABLE IF NOT EXISTS Contratos
                (id_contrato INTEGER PRIMARY KEY AUTOINCREMENT,
                proveedor TEXT,
                area TEXT,
                fecha_del_contrato TEXT,
                fecha_de_vencimiento TEXT,
                objeto TEXT,
                direccion TEXT,
                codigo_nit TEXT,
                codigo_reup TEXT,
                codigo_versat TEXT,
                banco TEXT,
                sucursal TEXT,
                cuenta  TEXT,
                titular TEXT,
                telefono INTEGER,
                autorizado_por TEXT)
        '''
        conn.execute(table_create_query)

        
        tabla_junta = """ CREATE TABLE IF NOT EXISTS Autorizo_Junta
                    (proveedor TEXT,
                    acuerdo_junta TEXT,
                    monto_junta INTEGER,
                    fecha_de_autorizo TEXT)
        """
        conn.execute(tabla_junta)

    
        tabla_service = """CREATE TABLE IF NOT EXISTS Servicios
                (proveedor TEXT,
                nombre_del_servicio TEXT,
                descripcion TEXT, 
                no_factura INTEGER,
                fecha_servicio TEXT,
                pagado TEXT,
                valor INTEGER)
        """
        conn.execute(tabla_service)
        
        table_recorver = ''' CREATE TABLE IF NOT EXISTS Recuperar_Contratos
                (proveedor TEXT, 
                area TEXT,
                fecha_del_contrato TEXT,
                fecha_de_vencimiento TEXT,
                objeto TEXT,
                direccion TEXT,
                codigo_nit TEXT,
                codigo_reup TEXT,
                codigo_versat TEXT,
                banco TEXT,
                sucursal TEXT,
                cuenta  TEXT,
                titular TEXT,
                telefono INTEGER,
                autorizado_por TEXT)
        '''
        conn.execute(table_recorver)
        
       
        tabla_objeto = '''CREATE TABLE IF NOT EXISTS Objetos
                (objeto TEXT, 
                marcado INTEGER)
        '''
        conn.execute(tabla_objeto)
        
        tabla_autorizado = '''CREATE TABLE IF NOT EXISTS Autorizado_Firmar_Factura
                (autorizado_por TEXT, 
                marcado INTEGER)
        '''
        conn.execute(tabla_autorizado)
        
        tabla_area = '''CREATE TABLE IF NOT EXISTS Area_que_Tramita
                (area TEXT, 
                email TEXT)
        '''
        conn.execute(tabla_area)

        conn.commit()
        conn.close()
        
    def delete_date_contracts(self):
        def get_date():
            date = str(datetime.datetime.now().date()).split("-")
            date[0], date[2] = date[2], date[0]
            
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
            
            return date

        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
        instruccion = f"SELECT * FROM Contratos WHERE fecha_de_vencimiento = '{get_date()}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        
        if not datos:
            conn.commit()
            conn.close()
            return
        
        datos_copy = [list(i) for i in datos]
        
        data_insert_query = ''' INSERT INTO Recuperar_Contratos 
                    (proveedor,
                    area,
                    fecha_del_contrato, 
                    fecha_de_vencimiento,
                    objeto,
                    direccion,
                    codigo_nit, 
                    codigo_reup, 
                    codigo_versat,
                    banco, 
                    sucursal,
                    cuenta,
                    titular,
                    telefono,
                    autorizado_por) 
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''
        
        for d in datos_copy:
            d[3], d[4] = "", ""
            cursor.execute(data_insert_query, d[1:])
        
        names = []
        for n in datos:
            names.append(n[1])
            
        for c in datos:
            instruccion = f"Delete FROM Contratos WHERE proveedor = '{c[1]}'"
            cursor.execute(instruccion)
        
            instruccion = f"DELETE FROM Servicios WHERE proveedor = '{c[1]}'"
            cursor.execute(instruccion)

            instruccion = f"DELETE FROM Autorizo_Junta WHERE proveedor = '{c[1]}'"
            cursor.execute(instruccion)
            
        conn.commit()
        conn.close()
        

if __name__ == "__main__":    
    App()
