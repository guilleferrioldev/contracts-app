import customtkinter as ctk 
from message import Message, Actualizar, UpdateLabel
from datos_servicios import DatosServicios
from service import Frames
from pdf import PanelPDFViewer, CTkPDFViewer
import sqlite3
import os

class Datos(ctk.CTkToplevel):
    def __init__(self, master, title):
        super().__init__(master = master)
        
        self.master = master
        
        self.title(title)
        self.transient(master)
        self.width = int(self.winfo_screenwidth()/1.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(True, True)
        self.font = ctk.CTkFont("Helvetica", 15)
        self.titulo = title
        
        # database
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
               
        instruccion = f"SELECT * FROM Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        
        conn.commit()
        conn.close()
        
       
        # widgets
        self.proveedor = ctk.CTkLabel(self, text = title, font = ctk.CTkFont("Helvetica", 25, "bold"), anchor = "w")
        self.proveedor.place(relx = 0.05, rely = 0.05, relwidth =0.55, relheight = 0.043)
        
        self.objeto = ctk.CTkLabel(self, text = f"Objeto: {datos[0][4]}", font = self.font)
        self.objeto.place(relx = 0.05, rely = 0.12)
        
        self.fecha = ctk.CTkLabel(self, text = f"Fecha del contrato: {datos[0][2]}", font = self.font)
        self.fecha.place(relx = 0.05, rely = 0.18)

        self.fecha_vencimiento = ctk.CTkLabel(self, text = f"Fecha de vencimiento: {datos[0][3]}", font = self.font)
        self.fecha_vencimiento.place(relx = 0.05, rely = 0.23)

        self.direccion = ctk.CTkLabel(self, text = f"Dirección: {datos[0][5]}", font = self.font)
        self.direccion.place(relx = 0.05, rely = 0.28)

        self.codigo_nit = ctk.CTkLabel(self, text = f"Código NIT: {datos[0][6]}", font = self.font)
        self.codigo_nit.place(relx = 0.05, rely = 0.33)
        
        self.codigo_reup = ctk.CTkLabel(self, text = f"Código REUP: {datos[0][7]}", font = self.font)
        self.codigo_reup.place(relx = 0.05, rely = 0.38)

        self.codigo_versat = ctk.CTkLabel(self, text = f"Código VERSAT: {datos[0][8]}", font = self.font)
        self.codigo_versat.place(relx = 0.05, rely = 0.43)

        self.banco = ctk.CTkLabel(self, text = f"Banco: {datos[0][9]}", font = self.font)
        self.banco.place(relx = 0.05, rely = 0.48)

        self.sucursal = ctk.CTkLabel(self, text = f"Sucursal bancaria: {datos[0][10]}", font = self.font)
        self.sucursal.place(relx = 0.05, rely = 0.53)
        
        self.cuenta = ctk.CTkLabel(self, text = f"Cuenta bancaria: {datos[0][11]}", font = self.font)
        self.cuenta.place(relx = 0.05, rely = 0.58)
        
        self.titular = ctk.CTkLabel(self, text = f"Titular de la cuenta: {datos[0][12]}", font = self.font)
        self.titular.place(relx = 0.05, rely = 0.63)
        
        self.telefono = ctk.CTkLabel(self, text = f"Teléfono del titular: {datos[0][13]}", font = self.font)
        self.telefono.place(relx = 0.05, rely = 0.68)

        self.autorizado = ctk.CTkLabel(self, text = f"Aut.firmar factura: {datos[0][14]}", font = self.font)
        self.autorizado.place(relx = 0.05, rely = 0.73)


        # servicios 
        self.frame_servicios = FrameServicios(self)

        self.servicios_scroll = ScrollFrame(self.frame_servicios)

        self.importe_label = ctk.CTkLabel(self.frame_servicios, text = f"Importe: 0.00 cup", font = ctk.CTkFont("Helvetica", 15, "bold"))
        self.importe_label.place(relx = 0.53, rely = 0.93)

        self.cantidad_label = ctk.CTkLabel(self.frame_servicios, text = f"Cantidad: 0", font = ctk.CTkFont("Helvetica", 15, "bold"))
        self.cantidad_label.place(relx = 0.1, rely = 0.93)

        self.servicios()
        
        # Añadir servicios
        self.servicios_menu = ctk.CTkOptionMenu(self.frame_servicios, values = [str(i) for i in range(11)], command = self.add_service)
        self.servicios_menu.place(relx = 0.82, rely = 0.05, relwidth = 0.13)
        
        self.servicios_label = ctk.CTkLabel(self.frame_servicios, text = "Servicios", font = ctk.CTkFont("Helvetica",20, "bold"))
        self.servicios_label.place(relx = 0.1, rely = 0.05)

        # Cancel button
        self.cancel_button = ctk.CTkButton(self, text = "Atrás", font = self.font, command = self.atras)
        self.cancel_button.place(relx = 0.43, rely = 0.9)
        
        # Pdf button
        self.pdf_panel = PanelPDFViewer(self, 1.0, 0.7, "PDF", f"{self.titulo}")

        self.ver_pdf = ctk.CTkButton(self, text = "Ver PDF", font = self.font, command = self.read_pdf)  
        self.ver_pdf.place(relx = 0.63, rely = 0.05, relwidth = 0.1)
        
        # Actualizar frame
        self.actualizar_frame = Actualizar(self, 1.0, 0.35)

        self.guardar_button = ctk.CTkButton(self.actualizar_frame, text = "Guardar", font = self.font, command = self.guardar)
        self.guardar_button.place(relx = 0.55, rely = 0.85, relheight = 0.1, relwidth = 0.2)

        self.actualizar = ctk.CTkButton(self, text = "Actualizar", font = self.font, command = self.actualizar_frame.animate)  
        self.actualizar.place(relx = 0.74, rely = 0.05, relwidth = 0.1)
    
    def add_service(self, choice):
        for child in self.servicios_scroll.winfo_children():
            if child.widgetName == "frame":
                child.destroy()

        i = 0 
        while i < int(choice):
            self.anadir = Frames(self.servicios_scroll, "anadir", f"{self.titulo}")
            i +=1

        self.servicios()

    def read_pdf(self):
        self.pdf_panel.animate()
        if os.path.isfile(f"./pdfs/{self.titulo}.pdf"):
            CTkPDFViewer(self.pdf_panel.frame, file = f"{self.titulo}")

    def servicios(self):
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
        
        instruccion_importe = f"SELECT sum(valor) FROM Servicios WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion_importe)
        importe = cursor.fetchall()
        
        instruccion_serv = f"SELECT * FROM Servicios WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion_serv)
        datos_serv = cursor.fetchall()
        
        instruccion_count = f"SELECT count(proveedor) FROM Servicios WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion_count)
        datos_count = cursor.fetchall()
        
        conn.commit()
        conn.close()
        
        self.frames = []
        i = 0
        while i < datos_count[0][0]:
            frames = DatosServicios(self.servicios_scroll,
                           proveedor = self.titulo,
                           nombre = datos_serv[i][1],
                           descripcion = datos_serv[i][2],
                           factura = datos_serv[i][3],
                           fecha = datos_serv[i][4],
                           pagado = datos_serv[i][5],
                           valor = datos_serv[i][-1])
            self.frames.append(frames)    
            i+=1
 
        if importe[0][0] == None:
            show_importe = "0.00"
        elif len(str(importe[0][0])) < 4:
            show_importe = importe[0][0]
        elif len(str(importe[0][0])) == 4:
            show_importe = str(importe[0][0])[0] + " " + str(importe[0][0])[1:] 
        elif len(str(importe[0][0])) == 5:
            show_importe = str(importe[0][0])[0:2] + " " + str(importe[0][0])[2:] 
        elif len(str(importe[0][0])) == 6:
            show_importe = str(importe[0][0])[0:3] + " " + str(importe[0][0])[3:] 
        elif len(str(importe[0][0])) == 7:
            show_importe = str(importe[0][0])[0] + " " + str(importe[0][0])[1:4] + " " + str(importe[0][0])[4:]
        else:    
            show_importe = str(importe[0][0])[0:2] + " " + str(importe[0][0])[2:5] + " " + str(importe[0][0])[5:]
       
    
        self.importe_label.configure(text = f"Importe: {show_importe} CUP")
        self.cantidad_label.configure(text = f"Cantidad: {datos_count[0][0]}")
    
    def atras(self):
        for child in self.master.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        
        self.master.master.create_frames()
        self.master.master.master.master.master.master.sort.set("Proveedor")
 

    def new_service(self):
        proveedor = self.titulo
        nombre_del_servicio = self.anadir.anadir_frame.nombre_servicio_entry.get()       
        descripcion = self.anadir.anadir_frame.desc_servicio_entry.get()       
        no_factura = self.anadir.anadir_frame.factura_entry.get()       
        fecha_servicio = f"{self.anadir.anadir_frame.fecha_serv_day.get()}/{self.anadir.anadir_frame.fecha_serv_mes.get()}/{self.anadir.anadir_frame.fecha_serv_year.get()}"       
        pagado = self.anadir.anadir_frame.pagado_entry.get()       
        valor = self.anadir.anadir_frame.valor_entry.get() if len(self.anadir.anadir_frame.valor_entry.get()) > 0 else 0       


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

        self.anadir.animate()
        for child in self.servicios_scroll.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        self.servicios()


    def guardar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
        
        for frame in self.actualizar_frame.frames:
            if frame.text == "Proveedor":
                prov = (frame.entry.get()[0]).upper() + frame.entry.get()[1:]
                instruccion = f"UPDATE Contratos SET proveedor='{prov}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                instruccion = f"UPDATE Servicios SET proveedor='{prov}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                if os.path.isfile(f"./pdfs/{self.titulo}.pdf"):
                    os.rename(f"./pdfs/{self.titulo}.pdf", f"./pdfs/{prov}.pdf")
                self.titulo = prov
                self.proveedor.configure(text = f"{prov}")
                
            elif frame.text == "Objeto":           
                instruccion = f"UPDATE Contratos SET objeto='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.objeto.configure(text = f"Objeto: {frame.entry.get()}")
            
            elif frame.text == "Fecha del contrato":           
                instruccion = f"UPDATE Contratos SET fecha_del_contrato='{frame.day.get()}/{frame.month.get()}/{frame.year.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.fecha.configure(text = f"Fecha del contrato: {frame.day.get()}/{frame.month.get()}/{frame.year.get()}")
            
            elif frame.text == "Fecha de vencimiento":           
                instruccion = f"UPDATE Contratos SET fecha_de_vencimiento ='{frame.day.get()}/{frame.month.get()}/{frame.year.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.fecha_vencimiento.configure(text = f"Fecha de vencimiento: {frame.day.get()}/{frame.month.get()}/{frame.year.get()}")

            elif frame.text == "Dirección":           
                instruccion = f"UPDATE Contratos SET direccion='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.direccion.configure(text = f"Dirección: {frame.entry.get()}")
            
            elif frame.text == "Código NIT":           
                instruccion = f"UPDATE Contratos SET codigo_nit='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.codigo_nit.configure(text = f"Código NIT: {frame.entry.get()}")

            elif frame.text == "Código REUP":           
                instruccion = f"UPDATE Contratos SET codigo_reup='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.codigo_reup.configure(text = f"Código REUP: {frame.entry.get()}")
            
            elif frame.text == "Código VERSAT":           
                instruccion = f"UPDATE Contratos SET codigo_versat='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.codigo_versat.configure(text = f"Código VERSAT: {frame.entry.get()}")

            elif frame.text == "Sucursal bancaria":           
                instruccion = f"UPDATE Contratos SET sucursal='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.sucursal.configure(text = f"Sucursal bancaria: {frame.entry.get()}")

            elif frame.text == "Cuenta bancaria":           
                instruccion = f"UPDATE Contratos SET cuenta='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.cuenta.configure(text = f"Cuenta bancaria: {frame.entry.get()}")

            elif frame.text == "Titular de la cuenta":           
                instruccion = f"UPDATE Contratos SET titular='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.titular.configure(text = f"Titular de la cuenta: {frame.entry.get()}")
            
            elif frame.text == "Teléfono del titular":           
                instruccion = f"UPDATE Contratos SET telefono='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.telefono.configure(text = f"Teléfono del titular: {frame.entry.get()}")

            elif frame.text == "Aut.firmar factura":           
                instruccion = f"UPDATE Contratos SET autorizado_por='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.autorizado.configure(text = f"Aut.firmar factura: {frame.entry.get()}")

        conn.commit()
        conn.close()

        self.actualizar_frame.animate()


class FrameServicios(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master)

        self.master = master

        self.place(relx = 0.55, rely = 0.15, relwidth = 0.4, relheight = 0.7)



class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master = master)

        self.master = master

        self.place(relx = 0.05, rely = 0.13, relwidth = 0.9, relheight = 0.8)



    
