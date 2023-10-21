import customtkinter as ctk 
from message import EliminarServicio
from pdf import PanelPDFViewer, CTkPDFViewer
from pylatex import Document
from pylatex.utils import NoEscape
from pylatex.package import Package
import sqlite3
import os
import datetime

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
        print(datetime.datetime.now().date())
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
        
        self.pdf_factura = PanelPDFViewer(self.master.master.master, 1.0, 0.7, "Solicitud de Pago", f"{self.proveedor}")
        self.factura = ctk.CTkButton(self, text = "Sol. pago", font = self.font, command = self.sol_factura)
        self.factura.place(relx = 0.7, rely = 0.6, relwidth = 0.25, relheight = 0.11)       

        self.eliminar = ctk.CTkButton(self, text = "Eliminar", font = self.font, command = self.message.animate, hover_color = "red")
        self.eliminar.place(relx = 0.7, rely = 0.8, relwidth = 0.25, relheight = 0.11)
        
        self.pack(expand = "True", fill = "x", padx = 5, pady = 5)
    
    def sol_factura(self):
        self.pdf_factura.animate()
        self.generate_PDF()
        path = os.path.join("temporal.pdf")
        self.pdf_viewer = CTkPDFViewer(self.pdf_factura.frame, path = path ,file = f"temporal.pdf")

    def extract_from_database_to_generate_pdf(self):
        conn = sqlite3.connect(os.path.join("contratos.db"))
        cursor = conn.cursor()

        instruccion = f"SELECT * FROM Contratos WHERE proveedor = '{self.proveedor}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()

        return datos

    def generate_PDF(self):
        datos = self.extract_from_database_to_generate_pdf()
        descripcion = self.descripcion.split()
        res = []
        s = ""
        i = 0
        while i < len(descripcion):
            if len(s) > 80:
                res.append(s)
                s = ""
            s = s + " " + descripcion[i]
            i += 1        
        res.append(s)
        
        with open("solicitud.tex") as file:
            tex = file.readlines()
        
        tex.insert(33, r"\put(160,-87.09998){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{self.proveedor}" +"}\n")
        tex.insert(36, r"\put(115,-135.46){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{datos[0][8]}" +"}\n")
        tex.insert(38,  r"\put(420,-135.46){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{datos[0][9]}" +"}\n")
        tex.insert(42, r"\put(160,-187.66){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{datos[0][13]}" +"}\n" )
        tex.insert(109,  r"\put(120,-250.33){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{datos[0][12]}" +"}\n")
        tex.insert(161, r"\put(90,-288.73){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{datos[0][10]}" +"}\n")
        tex.insert(212, r"\put(100,-327.13){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{self.show_importe}" +"}\n")

        pos = 0
        y_pos = -400.13
        while pos < len(res):
            tex.insert(292 + pos, f"\put(30,{y_pos})" + r"{\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{res[pos]}" +"}\n")
            pos += 1 
            y_pos -= 25 
        
        fecha = self.fecha.split("/")
        pos = 0
        x_pos = 390
        for i in range(len(fecha)):
            tex.insert(374 + pos, f"\put({x_pos},-560.46)" + r"{\fontsize{12}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}" + f"{fecha[i]}" +"}\n")
            pos += 1
            if i == 0:
                x_pos += 20
            elif i == 1:
                x_pos += 80
            
        doc = Document('temporal', font_size=None)

        doc.preamble.append(NoEscape("".join(tex)))
        
        #doc.generate_tex()
        doc.generate_pdf(clean_tex=False)
    
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
        
        #self.factura.destroy()
        self.master.master.master.servicios()

