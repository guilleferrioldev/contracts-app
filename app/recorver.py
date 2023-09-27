import customtkinter as ctk 
import sqlite3
from message import Actualizar, Message

class Frame(ctk.CTkFrame):
    def __init__(self, master, proveedor, objeto):
        super().__init__(master = master,
                         width = 200,
                         fg_color = "white")

        self.proveedor = proveedor 
        self.objeto = objeto

        self.proveedor_label = ctk.CTkLabel(self, text = f"{self.proveedor}", font = ctk.CTkFont("Helvetica", 30, "bold"), anchor = "w")
        self.proveedor_label.place(relx = 0.03, rely = 0.2, relwidth = 0.9, relheight = 0.4)
        
        self.objeto_label = ctk.CTkLabel(self, text = f"{self.objeto}", font = ctk.CTkFont("Helvetica", 15), anchor = "w")
        self.objeto_label.place(relx = 0.03, rely = 0.55, relwidth = 0.6, relheight = 0.2)
        

        self.bind("<Button>", lambda event: RecorverData(self, self.proveedor))
        self.objeto_label.bind("<Button>", lambda event: RecorverData(self, self.proveedor))
        self.proveedor_label.bind("<Button>", lambda event: RecorverData(self, self.proveedor))

        self.pack(expand = True, fill = "x", padx = 5, pady = 5)


class Search(ctk.CTkEntry):
    def __init__(self, master):
        super().__init__(master = master, placeholder_text = "Buscar")

        self.bind("<KeyRelease>", lambda event: self.buscar())

        self.place(relx = 0.7, rely = 0.08, relwidth = 0.2, relheight = 0.043)

    def buscar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = f"SELECT proveedor, objeto FROM Recuperar_Contratos WHERE proveedor like '%{self.get()}%' ORDER BY proveedor"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
                
        conn.commit()
        conn.close()

        for child in self.master.scroll.winfo_children():
            if child.widgetName == "frame":
                child.destroy()

        i = 0 
        while i < len(datos):
            Frame(self.master.scroll, datos[i][0], datos[i][1])
            i +=1



class Recorver(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        # widgets
        self.font = ctk.CTkFont("Helvetica", 15)
        
        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx = 0.01, rely = 0.015, relwidth = 0.98, relheight = 0.97)

        self.scroll = ctk.CTkScrollableFrame(self.frame)
        self.scroll.place(relx = 0.05, rely = 0.15, relwidth = 0.9, relheight = 0.7)
        
        self.create_frames()
        self.search = Search(self)

        self.label = ctk.CTkLabel(self.frame, text = "Recuperar contrato", font = ctk.CTkFont("Helvetica", 25, "bold"), anchor = "w")
        self.label.place(relx = 0.05, rely = 0.05, relwidth = 0.4, relheight = 0.043)

        self.atras_button = ctk.CTkButton(self.frame, text = "Atrás", font = self.font,hover_color = "red",command = self.animate)
        self.atras_button.place(relx = 0.43, rely = 0.9, relwidth = 0.1, relheight = 0.043)
        

        # layout 
        self.place(relx = self.start_pos, rely = 0.01, relwidth = 0.99, relheight = 0.99)

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
        else:
            self.animate_backwards()

    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.999 
            self.place(relx = self.pos, rely = 0.01, relwidth = 0.99, relheight = 0.99)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.999 
            self.place(relx = self.pos, rely = 0.01, relwidth = 0.99, relheight = 0.99)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

    def create_frames(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = "SELECT proveedor, objeto FROM Recuperar_Contratos ORDER BY proveedor"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
                
        conn.commit()
        conn.close()
        
        i = 0 
        while i < len(datos):    
            Frame(self.scroll, datos[i][0], datos[i][1])
            i += 1 



class RecorverData(ctk.CTkToplevel):
    def __init__(self, master, title):
        super().__init__(master = master)
        
        self.master = master
        
        self.title(title)
        self.transient(master)
        self.width = int(self.winfo_screenwidth()/1.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)
        self.titulo = title

        # database
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
               
        instruccion = f"SELECT * FROM Recuperar_Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        
        conn.commit()
        conn.close()

        # widgets
        self.font = ctk.CTkFont("Helvetica", 15)

        self.proveedor = ctk.CTkLabel(self, text = title, font = ctk.CTkFont("Helvetica", 25, "bold"))
        self.proveedor.place(relx = 0.05, rely = 0.05)

        self.area = ctk.CTkLabel(self, text = f"Área: {datos[0][1]}", font = self.font)
        self.area.place(relx = 0.05, rely = 0.10)

        self.objeto = ctk.CTkLabel(self, text = f"Objeto: {datos[0][4]}", font = self.font)
        self.objeto.place(relx = 0.05, rely = 0.15)
        
        self.fecha = ctk.CTkLabel(self, text = f"Fecha del contrato: No existe", font = self.font)
        self.fecha.place(relx = 0.05, rely = 0.23)

        self.fecha_vencimiento = ctk.CTkLabel(self, text = f"Fecha de vencimiento: No existe", font = self.font)
        self.fecha_vencimiento.place(relx = 0.05, rely = 0.28)

        self.direccion = ctk.CTkLabel(self, text = f"Dirección: {datos[0][5]}", font = self.font)
        self.direccion.place(relx = 0.05, rely = 0.33)

        self.codigo_nit = ctk.CTkLabel(self, text = f"Código NIT: {datos[0][6]}", font = self.font)
        self.codigo_nit.place(relx = 0.05, rely = 0.38)
        
        self.codigo_reup = ctk.CTkLabel(self, text = f"Código REUP: {datos[0][7]}", font = self.font)
        self.codigo_reup.place(relx = 0.05, rely = 0.43)

        self.codigo_versat = ctk.CTkLabel(self, text = f"Código VERSAT: {datos[0][8]}", font = self.font)
        self.codigo_versat.place(relx = 0.05, rely = 0.48)

        self.banco = ctk.CTkLabel(self, text = f"Banco: {datos[0][9]}", font = self.font)
        self.banco.place(relx = 0.05, rely = 0.53)

        self.sucursal = ctk.CTkLabel(self, text = f"Sucursal bancaria: {datos[0][10]}", font = self.font)
        self.sucursal.place(relx = 0.05, rely = 0.58)
        
        self.cuenta = ctk.CTkLabel(self, text = f"Cuenta bancaria: {datos[0][11]}", font = self.font)
        self.cuenta.place(relx = 0.05, rely = 0.63)
        
        self.titular = ctk.CTkLabel(self, text = f"Titular de la cuenta: {datos[0][12]}", font = self.font)
        self.titular.place(relx = 0.05, rely = 0.68)
        
        self.telefono = ctk.CTkLabel(self, text = f"Teléfono del titular: {datos[0][13]}", font = self.font)
        self.telefono.place(relx = 0.05, rely = 0.73)

        self.autorizado = ctk.CTkLabel(self, text = f"Aut.firmar factura: {datos[0][14]}", font = self.font)
        self.autorizado.place(relx = 0.05, rely = 0.78)

        self.atras_button = ctk.CTkButton(self, text = "Atrás",font = self.font, command =  self.atras, hover_color= "red")
        self.atras_button.place(relx = 0.3, rely = 0.9)
        
        self.message_recuperar = Message(self, 1.0, 0.7, "Recuperar")

        self.aceptar = ctk.CTkButton(self.message_recuperar, text = "Si", font = self.font, command = self.recuperar, hover_color= "green")
        self.aceptar.place(relx = 0.7, rely = 0.8, relwidth = 0.2)
    
        self.denegar = ctk.CTkButton(self.message_recuperar, text = "No", font = self.font, command = self.message_recuperar.animate, hover_color = "red")
        self.denegar.place(relx = 0.4, rely = 0.8, relwidth = 0.2)

        self.recuperar_button = ctk.CTkButton(self, text = "Recuperar",font = self.font, command = self.message_recuperar.animate, hover_color = "green")
        self.recuperar_button.place(relx = 0.55, rely = 0.9)
        
        self.message_eliminar = Message(self, 1.0, 0.7, "Eliminar")

        self.aceptar = ctk.CTkButton(self.message_eliminar, text = "Si", font = self.font, command = self.eliminar, hover_color= "red")
        self.aceptar.place(relx = 0.7, rely = 0.8, relwidth = 0.2)
    
        self.denegar = ctk.CTkButton(self.message_eliminar, text = "No", font = self.font, command = self.message_eliminar.animate, hover_color= "green")
        self.denegar.place(relx = 0.4, rely = 0.8, relwidth = 0.2)

        self.eliminar_button = ctk.CTkButton(self, text = "Eliminar",font = self.font, command = self.message_eliminar.animate, hover_color = "red")
        self.eliminar_button.place(relx = 0.8, rely = 0.05)
        
        self.actualizar_frame = Actualizar(self, 1.0, 0.35, "recuperar")

        self.actualizar_button = ctk.CTkButton(self, text = "Actualizar", font = self.font, command = self.actualizar_frame.animate)
        self.actualizar_button.place(relx = 0.65, rely = 0.05)
        
        self.guardar_button = ctk.CTkButton(self.actualizar_frame, text = "Guardar", font = self.font, command = self.actualizar, hover_color= "green")
        self.guardar_button.place(relx = 0.55, rely = 0.85, relheight = 0.1, relwidth = 0.2)
    

    def eliminar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = f"DELETE FROM Recuperar_Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)

        conn.commit()
        conn.close()

        for child in self.master.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()

        self.master.master.master.master.master.master.create_frames()


    def atras(self):
        for child in self.master.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        
        self.master.master.master.master.master.master.create_frames()

        
    def recuperar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = f"SELECT * FROM Recuperar_Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        data_insert_query = ''' INSERT INTO Contratos 
                    (proveedor,
                    area,
                    fecha_del_contrato, 
                    fecha_de_vencimiento,
                    objeto, direccion,
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

        data_insert_tuple = datos[0]
        cursor.execute(data_insert_query, data_insert_tuple)
        
        instruccion = f"DELETE FROM Recuperar_Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)

        conn.commit()
        conn.close()
        
        for child in self.master.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        
        self.master.master.master.master.master.master.create_frames() 
        self.master.master.master.master.master.master.animate()
        self.master.master.master.master.master.master.master.animate()


    def actualizar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
        
        for frame in self.actualizar_frame.frames:
            if frame.text == "Proveedor":
                prov = (frame.entry.get()[0]).upper() + frame.entry.get()[1:]
                instruccion = f"UPDATE Recuperar_Contratos SET proveedor='{prov}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.titulo = prov
                self.proveedor.configure(text = f"{prov}")
            
            elif frame.text == "Área":           
                instruccion = f"UPDATE Recuperar_Contratos SET area='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.area.configure(text = f"Área: {frame.entry.get()}")

            elif frame.text == "Fecha del contrato":           
                instruccion = f"UPDATE Recuperar_Contratos SET fecha_del_contrato='{frame.day.get()}/{frame.month.get()}/{frame.year.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.fecha.configure(text = f"Fecha del contrato: {frame.day.get()}/{frame.month.get()}/{frame.year.get()}")
            
            elif frame.text == "Fecha de vencimiento":           
                instruccion = f"UPDATE Recuperar_Contratos SET fecha_de_vencimiento ='{frame.day.get()}/{frame.month.get()}/{frame.year.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.fecha_vencimiento.configure(text = f"Fecha de vencimiento: {frame.day.get()}/{frame.month.get()}/{frame.year.get()}")


            elif frame.text == "Dirección":           
                instruccion = f"UPDATE Recuperar_Contratos SET direccion='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.direccion.configure(text = f"Dirección: {frame.entry.get()}")
            
            elif frame.text == "Código NIT":           
                instruccion = f"UPDATE Recuperar_Contratos SET codigo_nit='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.codigo_nit.configure(text = f"Código NIT: {frame.entry.get()}")

            elif frame.text == "Código REUP":           
                instruccion = f"UPDATE Recuperar_Contratos SET codigo_reup='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.codigo_reup.configure(text = f"Código REUP: {frame.entry.get()}")
            
            elif frame.text == "Código VERSAT":           
                instruccion = f"UPDATE Recuperar_Contratos SET codigo_versat='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.codigo_versat.configure(text = f"Código VERSAT: {frame.entry.get()}")

            elif frame.text == "Sucursal bancaria":           
                instruccion = f"UPDATE Recuperar_Contratos SET sucursal='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.sucursal.configure(text = f"Sucursal bancaria: {frame.entry.get()}")

            elif frame.text == "Cuenta bancaria":           
                instruccion = f"UPDATE Recuperar_Contratos SET cuenta='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.cuenta.configure(text = f"Cuenta bancaria: {frame.entry.get()}")

            elif frame.text == "Titular de la cuenta":           
                instruccion = f"UPDATE Recuperar_Contratos SET titular='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.titular.configure(text = f"Titular de la cuenta: {frame.entry.get()}")
            
            elif frame.text == "Teléfono del titular":           
                instruccion = f"UPDATE Recuperar_Contratos SET telefono='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.telefono.configure(text = f"Teléfono del titular: {frame.entry.get()}")

            elif frame.text == "Aut.firmar factura":           
                instruccion = f"UPDATE Recuperar_Contratos SET autorizado_por='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.autorizado.configure(text = f"Aut.firmar factura: {frame.entry.get()}")

        conn.commit()
        conn.close()

        self.actualizar_frame.animate()






