import customtkinter as ctk
from message import Junta, OnlyNumbers
import sqlite3

class Service(ctk.CTkFrame):
    def __init__(self, master, relx, rely, relwidth, relheight):
        super().__init__(master = master)
        
        self.master = master
        
        self.add_service_label = ctk.CTkLabel(self, text = "Servicios/Pagos", font = ctk.CTkFont(family = "Helvetica", size = 20 ))
        self.add_service_label.place(relx = 0.05, rely = 0.02, relwidth = 0.4, relheight = 0.1)

        self.scroll_frame = Scrollable(self, relx = 0.05, rely = 0.13, relwidth = 0.9, relheight = 0.8)        
 
        self.importe_label = ctk.CTkLabel(self, font = ctk.CTkFont(family = "Helvetica", size =15))
        self.importe_label.place(relx = 0.56, rely = 0.935)

        self.frames = []
        
        self.place(relx = relx, rely = rely, relwidth = relwidth, relheight = relheight)
        
   

class Scrollable(ctk.CTkScrollableFrame):
    def __init__(self, master, relx, rely, relwidth, relheight):
        super().__init__(master = master)
        
        self.master = master

        self.place(relx = relx, rely = rely, relwidth = relwidth, relheight = relheight)

class Frames(ctk.CTkFrame):
    def __init__(self, master, text, proveedor= None):
        super().__init__(master = master,
                         height = 230,
                         fg_color = "white")
        
        self.text = text
        self.master = master 
        self.proveedor = proveedor
        
        self.values = []
        if self.text == "contracts":
            for child in self.master.master.master.objeto_frame.scroll.winfo_children():
                if child.widgetName == "frame":
                    if child.check_var.get() == "on":
                        self.values.append(child.text)
        
        elif self.text == "anadir":
            conn = sqlite3.connect("contratos.db")
            cursor = conn.cursor()

            instruction = f"Select objeto FROM Contratos WHERE proveedor = '{self.proveedor}'"
            cursor.execute(instruction)
            datos = cursor.fetchall()
            
            splitting = datos[0][0].split(",")
            
            objects = [i.strip() for i in splitting]
            
            i = 0 
            while i < len(objects):
                self.values.append(objects[i])
                i += 1

            conn.commit()
            conn.close()
        
        elif self.text == "recorver":
            conn = sqlite3.connect("contratos.db")
            cursor = conn.cursor()

            instruction = f"Select objeto FROM Recuperar_Contratos WHERE proveedor = '{self.proveedor}'"
            cursor.execute(instruction)
            datos = cursor.fetchall()
            
            splitting = datos[0][0].split(",")
            
            objects = [i.strip() for i in splitting]
            
            i = 0 
            while i < len(objects):
                self.values.append(objects[i])
                i += 1

            conn.commit()
            conn.close()

        self.nombre_servicio_label = ctk.CTkLabel(self, text = "Servicio")
        self.nombre_servicio_label.place(relx = 0.05, rely =0.03)
    
        self.nombre_servicio_entry = ctk.CTkOptionMenu(self, values = self.values)
        self.nombre_servicio_entry.place(relx = 0.35, rely =0.03, relwidth = 0.6)
        self.nombre_servicio_entry.set("Seleccionar objeto")

        self.desc_servicio_label = ctk.CTkLabel(self, text = "Descripción")
        self.desc_servicio_label.place(relx = 0.05, rely =0.16)

        self.desc_servicio_entry = ctk.CTkEntry(self)
        self.desc_servicio_entry.place(relx = 0.35, rely =0.16, relwidth = 0.6)
        
        self.factura_label = ctk.CTkLabel(self, text = "No. Factura")
        self.factura_label.place(relx = 0.05, rely =0.29)

        self.factura_entry = ctk.CTkEntry(self)
        self.factura_entry.place(relx = 0.35, rely =0.29, relwidth = 0.6)

        self.fecha_serv_label = ctk.CTkLabel(self, text = "Fecha")
        self.fecha_serv_label.place(relx = 0.05, rely = 0.42)

        self.fecha_serv_day = ctk.CTkOptionMenu(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.fecha_serv_day.place(relx = 0.35, rely = 0.42)
        
        self.fecha_serv_mes = ctk.CTkOptionMenu(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.fecha_serv_mes.place(relx = 0.505, rely = 0.42)

        
        self.fecha_serv_year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2024)], width = 70)
        self.fecha_serv_year.place(relx = 0.785, rely = 0.42)

        self.pagado_label = ctk.CTkLabel(self, text = "Pagado")
        self.pagado_label.place(relx = 0.05, rely =0.55)

        self.pagado_entry = ctk.CTkEntry(self)
        self.pagado_entry.place(relx = 0.35, rely =0.55, relwidth = 0.6)
        
        self.onlynumbers = OnlyNumbers(self.master.master.master, 1.0, 0.7)

        self.valor_label = ctk.CTkLabel(self, text = "Valor")
        self.valor_label.place(relx = 0.05, rely =0.68)
        
        self.valor_entry = ctk.CTkEntry(self)
        self.valor_entry.place(relx = 0.35, rely =0.68, relwidth = 0.6)

        self.valor_entry.bind("<KeyRelease>", lambda event: self.comp_change())

        if self.text == "anadir":
            self.cancel_button = ctk.CTkButton(self, text = "Cancelar", command = self.delete_service, hover_color = "red")
            self.cancel_button.place(relx = 0.25, rely = 0.82, relwidth = 0.2, relheight = 0.12)
            
            self.anadir_button = ctk.CTkButton(self, text = "Añadir", hover_color = "green", command = self.new_service)
            self.anadir_button.place(relx = 0.55, rely = 0.82, relwidth = 0.2, relheight = 0.12)
        
        else:
            self.cancel_button = ctk.CTkButton(self, text = "Cancelar", command = self.delete_contracts, hover_color = "red")
            self.cancel_button.place(relx = 0.35, rely = 0.82)
        
        self.pack(expand = "True", fill = "x", padx = 5, pady = 5)

    def comp_change(self):
        if self.valor_entry.get().isdigit():
            self.change_importe()
        elif not self.valor_entry.get().isdigit() and len(self.valor_entry.get()) != 0:
            self.valor_entry.delete(0, "end")
            self.onlynumbers.animate()

    def change_importe(self):
        values = []
        importe = 0
        if self.text == "contracts":
            i = 0
            while i < len(self.master.master.master.service.frames):
                values.append(self.master.master.master.service.frames[i].valor_entry.get())
                i+=1
        
            for val in values:
                if val != "":
                    importe += int(val)

        elif self.text == "anadir":
            for child in self.master.winfo_children():
                if child.widgetName == "frame":
                    if child.text == "anadir":
                        if child.valor_entry.get() == "":
                            values.append(0)
                        else:
                            values.append(int(child.valor_entry.get()))
                    elif child.text == "datos_servicios":
                        importe += child.importe 
        
            for i in values:
                importe += i
        else:
            valors = []
            for child in self.master.winfo_children():
                valors.append(child.valor_entry.get())
                
            importe = sum([int(i) for i in valors if i != ""])
        
        if len(str(importe)) < 4:
            show_importe = importe
        elif len(str(importe)) == 4:
            show_importe = str(importe)[0] + " " + str(importe)[1:] 
        elif len(str(importe)) == 5:
            show_importe = str(importe)[0:2] + " " + str(importe)[2:] 
        elif len(str(importe)) == 6:
            show_importe = str(importe)[0:3] + " " + str(importe)[3:] 
        elif len(str(importe)) == 7:
            show_importe = str(importe)[0] + " " + str(importe)[1:4] + " " + str(importe)[4:]
        else:    
            show_importe = str(importe)[0:2] + " " + str(importe)[2:5] + " " + str(importe)[5:]
        

        if self.text == "contracts":
            if self.master.master.master.junta_button.get() == "off":
                if importe <= 1000000:
                    self.master.master.master.service.importe_label.configure(text = f"Importe: {show_importe} CUP")
                else:
                    self.valor_entry.delete(0, "end")
                    self.master.master.master.suma()
                    self.junta_message = Junta(self.master.master.master, 1.0, 0.7, 1000000, "contracts").animate()
            else:
                if importe <= int(self.master.master.master.monto_junta_entry.get()):
                    self.master.master.master.service.importe_label.configure(text = f"Importe: {show_importe} CUP")
                else:
                    self.valor_entry.delete(0, "end")
                    self.master.master.master.suma()
                    self.junta_message = Junta(self.master.master.master, 1.0, 0.7, self.master.master.master.monto_junta_entry.get()).animate()

        elif self.text == "anadir":
            if self.master.master.master.datos_junta == []:
                if importe <= 1000000:
                    self.master.master.master.importe_label.configure(text = f"Importe: {show_importe} CUP")
                else:
                    self.valor_entry.delete(0, "end")
                    self.master.master.master.suma()
                    self.junta_message = Junta(self.master.master.master, 1.0, 0.7, 1000000, "anadir").animate()
            else:
                if importe <= int(self.master.master.master.datos_junta[0][2]):
                    self.master.master.master.importe_label.configure(text = f"Importe: {show_importe} CUP")
                else:
                    self.valor_entry.delete(0, "end")
                    self.junta_message = Junta(self.master.master.master, 1.0, 0.7, self.master.master.master.datos_junta[0][2], "anadir").animate()
        
        elif self.text == "recorver":
            conn = sqlite3.connect("contratos.db")
            cursor = conn.cursor()
        
            instruccion = f"SELECT * FROM Autorizo_Junta WHERE proveedor = '{self.master.master.master.titulo}'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

            conn.commit()
            conn.close()
            
            if datos == []:
                if importe <= 1000000:
                    self.master.master.master.importe_label.configure(text = f"Importe: {show_importe} CUP")
                else:
                    self.valor_entry.delete(0, "end")
                    for child in self.master.winfo_children():
                        child.valor_entry.configure(state = "disabled")
                    self.master.master.master.suma()
                    self.junta_message = Junta(self.master.master.master, 1.0, 0.7, 1000000, "recorver").animate()
            else:
                if importe <= int(datos[0][2]):
                    self.master.master.master.importe_label.configure(text = f"Importe: {show_importe} CUP")
                else:
                    self.valor_entry.delete(0, "end")
                    for child in self.master.winfo_children():
                        child.valor_entry.configure(state = "disabled")
                    self.master.master.master.suma()
                    self.junta_message = Junta(self.master.master.master, 1.0, 0.7, datos[0][2], "recorver").animate()



    def delete_contracts(self):
        if self.text == "contracts":
            self.master.master.frames = [i for i in self.master.master.frames if i != self]
            self.destroy()
            self.master.master.master.menu.set(str(int(self.master.master.master.menu.get())-1))
            self.master.master.master.suma()
        else:
            self.master.master.master.servicios_menu.set(str(int(self.master.master.master.servicios_menu.get())-1))
            self.destroy()
            self.master.master.master.suma()

    def delete_service(self):
        self.master.master.master.servicios_menu.set(str(int(self.master.master.master.servicios_menu.get())-1))
        self.destroy()
        self.change_importe()
        
    
    def new_service(self):
        proveedor = self.proveedor
        nombre_del_servicio = self.nombre_servicio_entry.get()       
        descripcion = self.desc_servicio_entry.get()       
        no_factura = self.factura_entry.get()       
        fecha_servicio = f"{self.fecha_serv_day.get()}/{self.fecha_serv_mes.get()}/{self.fecha_serv_year.get()}"       
        pagado = self.pagado_entry.get()       
        valor = self.valor_entry.get() if len(self.valor_entry.get()) > 0 else 0       


        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
        
        data_insert_query_service = '''INSERT INTO Servicios
                                    (proveedor,
                                    nombre_del_servicio,
                                    descripcion, 
                                    no_factura,
                                    fecha_servicio,
                                    pagado,
                                    valor )
                                    VALUES (?,?,?,?,?,?,?)'''

        data_insert_tuple_service = (proveedor,
                                    nombre_del_servicio,
                                    descripcion, 
                                    no_factura,
                                    fecha_servicio,
                                    pagado,
                                    valor)
 
        cursor.execute(data_insert_query_service, data_insert_tuple_service)

        conn.commit()
        conn.close()

        for child in self.master.master.master.servicios_scroll.winfo_children():
            if child.widgetName == "frame":
                if child.text != "anadir":
                    child.destroy()
        
        self.master.master.master.servicios()
        self.delete_service()












