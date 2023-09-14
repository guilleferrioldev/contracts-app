import customtkinter as ctk 

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
    def __init__(self, master):
        super().__init__(master = master,
                         height = 200,
                         fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"])
        
        self.master = master 
        
        #self.values = self.master.master.master.values_objeto
        
        self.nombre_servicio_label = ctk.CTkLabel(self, text = "Nombre del servicio")
        self.nombre_servicio_label.place(relx = 0.05, rely =0.03)

        #self.nombre_servicio_entry = ctk.CTkComboBox(self, values = self.values)
        self.nombre_servicio_entry = ctk.CTkEntry(self)
        self.nombre_servicio_entry.place(relx = 0.35, rely =0.03, relwidth = 0.6)

        self.desc_servicio_label = ctk.CTkLabel(self, text = "Descripción")
        self.desc_servicio_label.place(relx = 0.05, rely =0.18)

        self.desc_servicio_entry = ctk.CTkEntry(self)
        self.desc_servicio_entry.place(relx = 0.35, rely =0.18, relwidth = 0.6)
        
        self.factura_label = ctk.CTkLabel(self, text = "No. Factura")
        self.factura_label.place(relx = 0.05, rely =0.33)

        self.factura_entry = ctk.CTkEntry(self)
        self.factura_entry.place(relx = 0.35, rely =0.33, relwidth = 0.6)

        self.fecha_serv_label = ctk.CTkLabel(self, text = "Fecha")
        self.fecha_serv_label.place(relx = 0.05, rely = 0.48)

        self.fecha_serv_day = ctk.CTkComboBox(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.fecha_serv_day.place(relx = 0.35, rely = 0.48)
        
        self.fecha_serv_mes = ctk.CTkComboBox(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.fecha_serv_mes.place(relx = 0.49, rely = 0.48)

        
        self.fecha_serv_year = ctk.CTkComboBox(self, values = [str(i) for i in range(2020, 2024)], width = 70)
        self.fecha_serv_year.place(relx = 0.77, rely = 0.48)

        self.pagado_label = ctk.CTkLabel(self, text = "Pagado")
        self.pagado_label.place(relx = 0.05, rely =0.63)

        self.pagado_entry = ctk.CTkEntry(self)
        self.pagado_entry.place(relx = 0.35, rely =0.63, relwidth = 0.6)
        

        self.valor_label = ctk.CTkLabel(self, text = "Valor")
        self.valor_label.place(relx = 0.05, rely =0.78)

        self.valor_entry = ctk.CTkEntry(self)
        self.valor_entry.place(relx = 0.35, rely =0.78, relwidth = 0.6)

        self.pack(expand = "True", fill = "x", padx = 5, pady = 5)


class Menu(ctk.CTkOptionMenu):
    def __init__(self, master, relx, rely, command ):
        super().__init__(master = master, 
                         values = [str(i) for i in range(11)],
                         width = 70, 
                         command = command)
        
        self.place(relx = relx, rely = rely)
