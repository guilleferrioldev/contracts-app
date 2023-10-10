import customtkinter as ctk 
from message import Message, Actualizar, UpdateLabel
from datos_servicios import DatosServicios
from service import Frames
from pdf import PanelPDFViewer, CTkPDFViewer
from objeto import Object
import sqlite3
import os

class Datos(ctk.CTkToplevel):
    def __init__(self, master, title, parent = "contracts"):
        super().__init__(master = master)
        
        self.master = master
        
        self.title(title)
        self.transient(master)
        self.width = self.master.master.master.master.master.master.winfo_width()
        self.height = self.master.master.master.master.master.master.winfo_height()
        self.x = self.master.master.master.master.master.master.winfo_x()
        self.y = self.master.master.master.master.master.master.winfo_y()
        self.geometry(f"{self.width}x{self.height}+{self.x}+{self.y}")
        self.resizable(True, True)
        self.font = ctk.CTkFont("Helvetica", 15)
        self.titulo = title
        self.parent = parent
        self.font = ctk.CTkFont("Helvetica", 15)

        
        # database
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
               
        instruccion = f"SELECT * FROM Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        self.datos = cursor.fetchall()

        instruccion = f"SELECT * FROM Autorizo_Junta WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        self.datos_junta = cursor.fetchall()

        conn.commit()
        conn.close()

        # widgets
        self.proveedor = ctk.CTkLabel(self, text = title, font = ctk.CTkFont("Helvetica", 25, "bold"), anchor = "w")
        self.proveedor.place(relx = 0.03, rely = 0.05, relwidth =0.55, relheight = 0.043)
        
        self.area = ctk.CTkLabel(self, text = f"Área: {self.datos[0][2]}", font = self.font)
        self.area.place(relx = 0.03, rely = 0.10)
        
        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.place(relx = 0.03, rely = 0.15, relheight = 0.72, relwidth = 0.51)

        self.frame_objeto = ctk.CTkFrame(self.scroll, height = 300, fg_color = "white")
        self.frame_objeto.pack(fill = "x", expand = True, padx = 5, pady = 5)

        self.objeto = ctk.CTkLabel(self.frame_objeto, text = "Objetos", font = self.font)
        self.objeto.place(relx = 0.05, rely = 0.04) 

        #self.objeto_show_frame = Object(self, 1.0, 0.7, "Objeto")
        #self.objeto_button = ctk.CTkButton(self.frame_objeto, text = "+", font = self.font, command = self.objeto_show_frame.animate)
        #self.objeto_button.place(relx = 0.85, rely = 0.04, relwidth = 0.1, relheight = 0.08)

        self.objeto_scroll = ctk.CTkScrollableFrame(self.frame_objeto)
        self.objeto_scroll.place(relx = 0.05, rely = 0.15, relwidth = 0.9, relheight =  0.75)
        
        self.create_objects()
        
        self.frame_datos = ctk.CTkFrame(self.scroll, height = 500, fg_color = "white")
        self.frame_datos.pack(fill = "x", expand = True, padx = 5, pady = 5)
        
        self.fecha = ctk.CTkLabel(self.frame_datos, text = f"Fecha del contrato: {self.datos[0][3]}", font = self.font)
        self.fecha.place(relx = 0.05, rely = 0.03)

        self.fecha_vencimiento = ctk.CTkLabel(self.frame_datos, text = f"Fecha de vencimiento: {self.datos[0][4]}", font = self.font)
        self.fecha_vencimiento.place(relx = 0.05, rely = 0.09)

        self.direccion = ctk.CTkLabel(self.frame_datos, text = f"Dirección: {self.datos[0][6]}", font = self.font)
        self.direccion.place(relx = 0.05, rely = 0.15)

        self.codigo_nit = ctk.CTkLabel(self.frame_datos, text = f"Código NIT: {self.datos[0][7]}", font = self.font)
        self.codigo_nit.place(relx = 0.05, rely = 0.21)
        
        self.codigo_reup = ctk.CTkLabel(self.frame_datos, text = f"Código REUP: {self.datos[0][8]}", font = self.font)
        self.codigo_reup.place(relx = 0.05, rely = 0.27)

        self.codigo_versat = ctk.CTkLabel(self.frame_datos, text = f"Código VERSAT: {self.datos[0][9]}", font = self.font)
        self.codigo_versat.place(relx = 0.05, rely = 0.33)

        self.banco = ctk.CTkLabel(self.frame_datos, text = f"Banco: {self.datos[0][10]}", font = self.font)
        self.banco.place(relx = 0.05, rely = 0.39)

        self.sucursal = ctk.CTkLabel(self.frame_datos, text = f"Sucursal bancaria: {self.datos[0][11]}", font = self.font)
        self.sucursal.place(relx = 0.05, rely = 0.45)
        
        self.cuenta = ctk.CTkLabel(self.frame_datos, text = f"Cuenta bancaria: {self.datos[0][12]}", font = self.font)
        self.cuenta.place(relx = 0.05, rely = 0.51)
        
        self.titular = ctk.CTkLabel(self.frame_datos, text = f"Titular de la cuenta: {self.datos[0][13]}", font = self.font)
        self.titular.place(relx = 0.05, rely = 0.57)
        
        self.telefono = ctk.CTkLabel(self.frame_datos, text = f"Teléfono del titular: {self.datos[0][14]}", font = self.font)
        self.telefono.place(relx = 0.05, rely = 0.63)
        
        self.autorizo_junta = ctk.CTkLabel(self.frame_datos, text = f"Autorizo de la CCD/JDN: No", font = self.font)
        self.autorizo_junta.place(relx = 0.05, rely = 0.72)
        
        self.acuerdo = ctk.CTkLabel(self.frame_datos, text = f"Acuerdo: -", font = self.font)
        self.acuerdo.place(relx = 0.05, rely = 0.78)
        
        self.monto = ctk.CTkLabel(self.frame_datos, text = f"Monto acordado: -", font = self.font)
        self.monto.place(relx = 0.05, rely = 0.84)
        
        self.fecha_junta= ctk.CTkLabel(self.frame_datos, text = f"Fecha del acuerdo: -", font = self.font)
        self.fecha_junta.place(relx = 0.05, rely = 0.9)

        self.junta()        

        self.frame_autorizado = ctk.CTkFrame(self.scroll, height = 300, fg_color = "white")
        self.frame_autorizado.pack(fill = "x", expand = True, padx = 5, pady = 5)

        self.autorizado = ctk.CTkLabel(self.frame_autorizado, text = "Aut.firmar factura", font = self.font)
        self.autorizado.place(relx = 0.05, rely = 0.04)

        #self.autorizado_show_frame = Object(self, 1.0, 0.7, "Aut.firmar factura", "datos")
        #self.autorizado_button = ctk.CTkButton(self.frame_autorizado, text = "+", font = self.font, command = self.autorizado_show_frame.animate)
        #self.autorizado_button.place(relx = 0.85, rely = 0.04, relwidth = 0.1, relheight = 0.08)

        self.autorizado_scroll = ctk.CTkScrollableFrame(self.frame_autorizado)
        self.autorizado_scroll.place(relx = 0.05, rely = 0.15, relwidth = 0.9, relheight =  0.75)
        
        self.create_autorizados()

        # servicios 
        self.frame_servicios = FrameServicios(self)

        self.servicios_scroll = ScrollFrame(self.frame_servicios)

        self.importe_label = ctk.CTkLabel(self.frame_servicios, text = f"Importe: 0.00 cup", font = ctk.CTkFont("Helvetica", 15, "bold"))
        self.importe_label.place(relx = 0.56, rely = 0.93)

        self.cantidad_label = ctk.CTkLabel(self.frame_servicios, text = f"Cantidad: 0", font = ctk.CTkFont("Helvetica", 15, "bold"))
        self.cantidad_label.place(relx = 0.1, rely = 0.93)

        self.servicios()
        
        # Añadir servicios
        self.servicios_menu = ctk.CTkOptionMenu(self.frame_servicios, values = [str(i) for i in range(11)], command = self.add_service)
        self.servicios_menu.place(relx = 0.82, rely = 0.05, relwidth = 0.13)
        
        self.servicios_label = ctk.CTkLabel(self.frame_servicios, text = "Servicios", font = ctk.CTkFont("Helvetica",20, "bold"))
        self.servicios_label.place(relx = 0.1, rely = 0.05)

        # Cancel button
        self.cancel_button = ctk.CTkButton(self, text = "Atrás", font = self.font, command = self.atras, hover_color = "red")
        self.cancel_button.place(relx = 0.43, rely = 0.9)
        
        # Pdf button
        self.pdfmessage = Message(self, 1.0,0.7,"Insertar PDF")
        
        self.aceptar_pdf = ctk.CTkButton(self.pdfmessage, text = "Si", font = self.font,command = self.pdf_animate, hover_color = "green")
        self.aceptar_pdf.place(relx = 0.7, rely = 0.8, relwidth = 0.2)
        
        self.denegar_pdf = ctk.CTkButton(self.pdfmessage, text = "No", font = self.font, command = self.cancel_pdf_animate, hover_color= "red")
        self.denegar_pdf.place(relx = 0.4, rely = 0.8, relwidth = 0.2)

        self.pdf_panel = PanelPDFViewer(self, 1.0, 0.7, "PDF", f"{self.titulo}")

        self.ver_pdf = ctk.CTkButton(self, text = "Ver PDF", font = self.font, command = self.read_pdf)  
        self.ver_pdf.place(relx = 0.63, rely = 0.05, relwidth = 0.1)
        
        # Actualizar frame
        self.actualizar_frame = Actualizar(self, 1.0, 0.35, "datos")

        self.guardar_button = ctk.CTkButton(self.actualizar_frame, text = "Guardar", font = self.font, command = self.guardar, hover_color = "green")
        self.guardar_button.place(relx = 0.55, rely = 0.85, relheight = 0.1, relwidth = 0.2)

        self.actualizar = ctk.CTkButton(self, text = "Actualizar", font = self.font, command = self.actualizar_animate, hover_color = "orange")  
        self.actualizar.place(relx = 0.74, rely = 0.05, relwidth = 0.1)
    
        # Delete message
        self.deletemessage = Message(self, 1.0,0.7,"Eliminar")
        
        self.aceptar = ctk.CTkButton(self.deletemessage, text = "Si", font = self.font, command = self.eliminar, hover_color = "red")
        self.aceptar.place(relx = 0.7, rely = 0.8, relwidth = 0.2)
        
        self.denegar = ctk.CTkButton(self.deletemessage, text = "No", font = self.font, command = self.delete_enable, hover_color= "green")
        self.denegar.place(relx = 0.4, rely = 0.8, relwidth = 0.2)


        self.eliminar = ctk.CTkButton(self, text = "Eliminar", font = self.font, command = self.delete_disable, hover_color = "red")  
        self.eliminar.place(relx = 0.85, rely = 0.05, relwidth = 0.1)

    def create_objects(self):
        splitting = self.datos[0][5].split(",")
        data = [i.strip() for i in splitting]
        if data != [""]:
            for i in data:
                self.object_in = FrameObjetos(self.objeto_scroll, i)

    def create_autorizados(self):
        splitting = self.datos[0][15].split(",")
        data = [i.strip() for i in splitting]
        if data != [""]:
            for i in data:
                self.autorizado_in = FrameObjetos(self.autorizado_scroll, i)

    def disabled(self):
        self.eliminar.configure(state = "disabled")
        self.actualizar.configure(state = "disabled")
        self.ver_pdf.configure(state = "disabled")
        self.cancel_button.configure(state = "disabled")
    
    def enabled(self):
        self.eliminar.configure(state = "normal")
        self.actualizar.configure(state = "normal")
        self.ver_pdf.configure(state = "normal")
        self.cancel_button.configure(state = "normal")

    def delete_disable(self):
        self.deletemessage.animate()
        self.disabled()
    
    def delete_enable(self):
        self.deletemessage.animate()
        self.enabled()

    def actualizar_animate(self):
        self.actualizar_frame.animate()
        self.disabled()
    
    def cancel_pdf_animate(self):
        self.pdfmessage.animate()
        self.enabled()

    def pdf_animate(self):
        self.pdfmessage.animate()
        self.pdf_panel.copy_pdf()

    def junta(self):
        if self.datos_junta != []:
            importe = self.datos_junta[0][2]
            if len(str(importe)) < 4:
                monto = importe
            elif len(str(importe)) == 4:
                monto = str(importe)[0] + " " + str(importe)[1:] 
            elif len(str(importe)) == 5:
                monto = str(importe)[0:2] + " " + str(importe)[2:] 
            elif len(str(importe)) == 6:
                monto = str(importe)[0:3] + " " + str(importe)[3:] 
            elif len(str(importe)) == 7:
                monto = str(importe)[0] + " " + str(importe)[1:4] + " " + str(importe)[4:]
            else:    
                monto = str(importe)[0:2] + " " + str(importe)[2:5] + " " + str(importe)[5:]

            self.autorizo_junta.configure(text = "Autorizo de la CCD/JDN: Si")
            self.acuerdo.configure(text = f"Acuerdo: {self.datos_junta[0][1]}")
            self.monto.configure(text = f"Monto acordado: {monto} CUP")
            self.fecha_junta.configure(text = f"Fecha del acuerdo {self.datos_junta[0][3]}")

    def eliminar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
        instruccion = f"Select * FROM Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        
        
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

        data_insert_tuple = []
        i = 1 
        while i < len(datos[0]):
            if i != 3 and i != 4:
                data_insert_tuple.append(datos[0][i])
            else:
                data_insert_tuple.append("")
            i += 1
        
        cursor.execute(data_insert_query, data_insert_tuple)
    
        instruccion = f"Delete FROM Contratos WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)
        
        instruccion = f"DELETE FROM Servicios WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)

        instruccion = f"DELETE FROM Autorizo_Junta WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion)

        conn.commit()
        conn.close()
        
        # Move pdf to other dir
        if os.path.isfile(f"./pdfs/{self.titulo}.pdf"):
            os.remove(f"./pdfs/{self.titulo}.pdf")
        
        if self.parent == "contracts":
            for child in self.master.master.winfo_children():
                if child.widgetName == "frame":
                    child.destroy()
        
            self.master.master.create_frames()
        else:
            self.master.master.master.master.master.master.insert_frames()
            self.master.master.master.master.master.master.master.master.switch_frame("Calendario")   
        self.destroy()

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
        self.cancel_button.configure(state = "disabled")
        self.eliminar.configure(state = "disabled")
        self.actualizar.configure(state = "disabled")
        self.ver_pdf.configure(state = "disabled")
 
        if os.path.isfile(f"./pdfs/{self.titulo}.pdf"):
            self.pdf_panel.animate()
            pdf = CTkPDFViewer(self.pdf_panel.frame, file = f"{self.titulo}")
        else:
            self.pdfmessage.animate()


    def servicios(self):
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
        
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

        self.cantidad_label.configure(text = f"Cantidad: {datos_count[0][0]}")
        self.suma()
    
    def suma(self):
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
        
        instruccion_importe = f"SELECT sum(valor) FROM Servicios WHERE proveedor = '{self.titulo}'"
        cursor.execute(instruccion_importe)
        importe = cursor.fetchall()
        
        conn.commit()
        conn.close()
        
        valores = []
        for child in self.servicios_scroll.winfo_children():
            if child.text == "anadir":
                valores.append(child.valor_entry.get())

        value = sum([int(i) for i in valores if i != ""])
        
        if importe[0][0] != None:
            importe = importe[0][0] + value
        else:
            importe = 0
        
            
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
        
                    
        self.importe_label.configure(text = f"Importe: {show_importe} CUP")

    
    def atras(self):
        for child in self.master.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()

        if self.parent == "contracts":
            self.master.master.create_frames()
            self.master.master.master.master.master.master.sort.set("Proveedor")
        else:
            self.master.master.master.master.master.master.insert_frames()
            self.master.master.master.master.master.master.master.master.switch_frame("Calendario")   


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
            
            elif frame.text == "Área":           
                instruccion = f"UPDATE Contratos SET area='{frame.entry.get()}' WHERE  proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                self.area.configure(text = f"Área: {frame.entry.get()}")

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
            
            elif frame.text == "Autorizo de la CCD/JDN":
                self.autorizo_junta.configure(text = f"Autorizo de la CCD/JDN: Si")
                
                acuerdo = frame.acuerdo_entry.get()
                monto = frame.monto_entry.get()
                fecha_junta = f"{frame.day.get()}/{frame.month.get()}/{frame.year.get()}"

                instruccion = f"SELECT * FROM Autorizo_Junta WHERE proveedor='{self.titulo}'"
                cursor.execute(instruccion)
                datos = cursor.fetchall()
                
                if datos == []:
                    data_insert_query_junta = ''' INSERT INTO Autorizo_Junta 
                            (proveedor,
                            acuerdo_junta,
                            monto_junta,
                            fecha_de_autorizo)
                            VALUES (?,?,?,?)
                            '''

                    data_insert_tuple_junta = (self.titulo,
                            acuerdo,
                            monto,
                            fecha_junta)


                    cursor.execute(data_insert_query_junta, data_insert_tuple_junta)
                
                else:
                    instruccion = f"UPDATE Autorizo_Junta SET acuerdo_junta='{acuerdo}' WHERE  proveedor='{self.titulo}'"
                    cursor.execute(instruccion)
                    
                    instruccion = f"UPDATE Autorizo_Junta SET monto_junta='{monto}' WHERE  proveedor='{self.titulo}'"
                    cursor.execute(instruccion)
                    
                    instruccion = f"UPDATE Autorizo_Junta SET fecha_de_autorizo='{fecha_junta}' WHERE  proveedor='{self.titulo}'"
                    cursor.execute(instruccion)


                self.acuerdo.configure(text = f"Acuerdo: {frame.acuerdo_entry.get()}") 
                self.monto.configure(text = f"Monto acordado: {frame.monto_entry.get()} CUP")
                self.fecha_junta.configure(text = f"Fecha del acuerdo: {frame.day.get()}/{frame.month.get()}/{frame.year.get()}")

        conn.commit()
        conn.close()
        
        self.actualizar_frame.animate()


class FrameServicios(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master)

        self.master = master

        self.place(relx = 0.55, rely = 0.15, relwidth = 0.4, relheight = 0.72)



class ScrollFrame(ctk.CTkScrollableFrame):
    def __init__(self, master):
        super().__init__(master = master)

        self.master = master

        self.place(relx = 0.05, rely = 0.13, relwidth = 0.9, relheight = 0.8)

class FrameObjetos(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master,
                         height = 50, 
                         fg_color = "white")
        
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)
        
        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.03, rely = 0.3, relheight =0.4, relwidth = 0.92)
        
        self.pack(expand = True, fill = "x", padx = 5, pady = 5)

        




















    
