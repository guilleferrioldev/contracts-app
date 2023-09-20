import customtkinter as ctk 
import sqlite3

class Service(ctk.CTkFrame):
    def __init__(self, master, relx, rely, relwidth, relheight):
        super().__init__(master = master)
        
        self.master = master
        
        self.add_service_label = ctk.CTkLabel(self, text = "Servicios/Pagos", font = ctk.CTkFont(family = "Helvetica", size = 20 ))
        self.add_service_label.place(relx = 0.05, rely = 0.05)

        self.scroll_frame = Scrollable(self, relx = 0.05, rely = 0.13, relwidth = 0.9, relheight = 0.8)        

        
        self.importe_label = ctk.CTkLabel(self, font = ctk.CTkFont(family = "Helvetica", size =15))
        self.importe_label.place(relx = 0.55, rely = 0.935)

        self.frames = []
        
        self.place(relx = relx, rely = rely, relwidth = relwidth, relheight = relheight)
        
   

class Scrollable(ctk.CTkScrollableFrame):
    def __init__(self, master, relx, rely, relwidth, relheight):
        super().__init__(master = master)
        
        self.master = master

        self.place(relx = relx, rely = rely, relwidth = relwidth, relheight = relheight)

class Frames(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master,
                         height = 230,
                         fg_color = "white")
        
        self.text = text
        self.master = master 
        
        self.values = []
        if self.text == "contracts":
            for child in self.master.master.master.objeto_frame.scroll.winfo_children():
                if child.widgetName == "frame":
                    if child.check_var.get() == "on":
                        self.values.append(child.text)
        elif self.text == "anadir":
            conn = sqlite3.connect("contratos.db")
            cursor = conn.cursor()

            instruction = f"Select"
            conn.commit()
            conn.close()



        self.nombre_servicio_label = ctk.CTkLabel(self, text = "Servicio")
        self.nombre_servicio_label.place(relx = 0.05, rely =0.03)
    
        self.nombre_servicio_entry = ctk.CTkOptionMenu(self, values = self.values)
        self.nombre_servicio_entry.place(relx = 0.35, rely =0.03, relwidth = 0.6)
        self.nombre_servicio_entry.set("Selecciona nombre")

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
        self.fecha_serv_mes.place(relx = 0.49, rely = 0.42)

        
        self.fecha_serv_year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2024)], width = 70)
        self.fecha_serv_year.place(relx = 0.77, rely = 0.42)

        self.pagado_label = ctk.CTkLabel(self, text = "Pagado")
        self.pagado_label.place(relx = 0.05, rely =0.55)

        self.pagado_entry = ctk.CTkEntry(self)
        self.pagado_entry.place(relx = 0.35, rely =0.55, relwidth = 0.6)
        

        self.valor_label = ctk.CTkLabel(self, text = "Valor")
        self.valor_label.place(relx = 0.05, rely =0.68)

        self.valor_entry = ctk.CTkEntry(self)
        self.valor_entry.place(relx = 0.35, rely =0.68, relwidth = 0.6)

        self.cancel_button = ctk.CTkButton(self, text = "Cancelar", command = self.delete)
        self.cancel_button.place(relx = 0.35, rely = 0.82)

        self.pack(expand = "True", fill = "x", padx = 5, pady = 5)

    def delete(self):
        if self.text == "contracts":
            self.master.master.frames = [i for i in self.master.master.frames if i != self]
            self.destroy()
        if self.text == "anadir":
            self.destroy()


class Menu(ctk.CTkOptionMenu):
    def __init__(self, master, relx, rely, command ):
        super().__init__(master = master, 
                         values = [str(i) for i in range(11)],
                         width = 70, 
                         command = command)
        
        self.place(relx = relx, rely = rely)
