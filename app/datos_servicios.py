import customtkinter as ctk 
from message import EliminarServicio
from pdf import PanelPDFViewer
import sqlite3

class DatosServicios(ctk.CTkFrame):
    def __init__(self, master, proveedor, nombre, descripcion, factura, fecha, pagado, valor, text = "datos_servicios"):
        super().__init__(master = master,
                         height = 250,
                         fg_color = "white")

        self.font = ctk.CTkFont("Helvetica", 15) 
        
        self.master = master
        self.proveedor = proveedor
        self.nombre = nombre
        self.descripcion = descripcion
        self.factura = factura
        self.fecha = fecha
        self.pagado = pagado
        self.importe = valor 
        self.text = text

        if len(str(self.importe)) < 4:
            self.show_importe = self.importe
        elif len(str(self.importe)) == 4:
            self.show_importe = str(self.importe)[0] + " " + str(self.importe)[1:] 
        elif len(str(self.importe)) == 5:
            self.show_importe = str(self.importe)[0:2] + " " + str(self.importe)[2:] 
        elif len(str(self.importe)) == 6:
            self.show_importe = str(self.importe)[0:3] + " " + str(self.importe)[3:] 
        elif len(str(self.importe)) == 7:
            self.show_importe = str(self.importe)[0] + " " + str(self.importe)[1:4] + " " + str(self.importe)[4:]
        else:    
            self.show_importe = str(self.importe)[0:2] + " " + str(self.importe)[2:5] + " " + str(self.importe)[5:]


        self.nombre_servicio_label = ctk.CTkLabel(self, text = f"Nombre: {self.nombre}", font = self.font)
        self.nombre_servicio_label.place(relx = 0.05, rely =0.05)

                
        self.desc_servicio_label = ctk.CTkLabel(self, text = f"Descripción:", font = self.font)
        self.desc_servicio_label.place(relx = 0.05, rely =0.17)
        
        self.desc_servicio_info = ctk.CTkScrollableFrame(self)
        self.desc_servicio_info.place(relx = 0.28, rely =0.17, relwidth = 0.7, relheight=0.3)
        
        self.create_descripcion()
        
        self.factura_label = ctk.CTkLabel(self, text = f"No. Factura: {self.factura}", font = self.font)
        self.factura_label.place(relx = 0.05, rely =0.46)

        self.fecha_serv_label = ctk.CTkLabel(self, text = f"Fecha: {self.fecha}", font = self.font)
        self.fecha_serv_label.place(relx = 0.05, rely = 0.58)

        self.pagado_label = ctk.CTkLabel(self, text = f"Pagado {self.pagado}", font = self.font)
        self.pagado_label.place(relx = 0.05, rely =0.70)

        self.valor_label = ctk.CTkLabel(self, text = f"Valor: {self.show_importe}", font = self.font)
        self.valor_label.place(relx = 0.05, rely =0.82)
        
        self.message = EliminarServicio(self, 1.0, 0.7, "Eliminar")

        self.aceptar = ctk.CTkButton(self.message, text = "Si", font = self.font, command = self.delete, hover_color = "red")
        self.aceptar.place(relx = 0.58, rely = 0.65, relwidth = 0.25)
        
        self.denegar = ctk.CTkButton(self.message, text = "No", font = self.font, command = self.message.animate, hover_color = "green")
        self.denegar.place(relx = 0.2, rely = 0.65, relwidth = 0.25)
        
        #self.pdf_factura = PanelPDFViewer(self.master.master.master, 1.0, 0.7, "Solicitud de pago", f"{self.proveedor}")
        #self.factura = ctk.CTkButton(self, text = "Sol. pago", font = self.font,command=  self.pdf_factura.animate)
        #self.factura.place(relx = 0.7, rely = 0.6, relwidth = 0.25, relheight = 0.11)       

        self.eliminar = ctk.CTkButton(self, text = "Eliminar", font = self.font, command = self.message.animate, hover_color = "red")
        self.eliminar.place(relx = 0.7, rely = 0.8, relwidth = 0.25, relheight = 0.11)
        
        self.pack(expand = "True", fill = "x", padx = 5, pady = 5)
    
    def create_descripcion(self):
        start = 0
        while start < len(self.descripcion):
            label = ctk.CTkLabel(self.desc_servicio_info, text = f"{self.descripcion[start:start + 44]}", fg_color = "white", anchor = "w")
            label.pack(expand = True, fill = "x",padx = 2, pady = 0)
            start += 44

    def delete(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = f"DELETE FROM Servicios WHERE proveedor = '{self.proveedor}' AND nombre_del_servicio = '{self.nombre}' AND descripcion = '{self.descripcion}' AND no_factura = '{self.factura}' AND fecha_servicio = '{self.fecha}' AND pagado = '{self.pagado}' AND valor = '{self.importe}'"
        cursor.execute(instruccion)
        
        conn.commit()
        conn.close()
        
        for child in self.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()

        self.master.master.master.servicios()

