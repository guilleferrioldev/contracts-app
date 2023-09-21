import customtkinter as ctk 
from datos_contratos import Datos
from message import Message
import sqlite3


class Contracts(ctk.CTkScrollableFrame):
    def __init__(self, master, row, column, columnspan, padx, pady, sticky):
        super().__init__(master = master)
        
        self.create_frames()        

        self.grid(row = row, column = column, columnspan = columnspan,padx = padx, pady = pady, sticky = sticky)


    def create_frames(self):        
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
               
        instruccion = "SELECT proveedor, fecha_del_contrato, fecha_de_vencimiento, objeto, autorizado_por,(SELECT sum(valor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS valor, (SELECT count(proveedor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS count FROM Contratos ORDER BY proveedor"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()
        
        i = 0 
        while i < len(datos):
            ContractsFrames(self, 
                        proveedor = datos[i][0],
                        servicio = datos[i][-1],
                        objeto = datos[i][3],
                        autorizado = datos[i][4],
                        importe = datos[i][5],
                        fecha = datos[i][1],
                        vencimiento = datos[i][2])
            i +=1

                
    def readOrdered(self, searching, field):
        if field == "Proveedor":
            field = "proveedor"
        elif field == "Fecha contrato":
            field = "fecha_del_contrato"
        elif field == "Fecha vencimiento":
            field = "fecha_de_vencimiento"
        elif field == "Objeto":
            field = "objeto"
        elif field == "Importe total":
            field = "valor"
        elif field == "Servicios":
            field = "count"
        elif field == "Aut.firm factura":
            field = "autorizado_por"

        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
        
        instruccion = f"SELECT proveedor, fecha_del_contrato, fecha_de_vencimiento, objeto, autorizado_por, (SELECT sum(valor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS valor, (SELECT count(proveedor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS count FROM Contratos WHERE proveedor like '%{searching}%' ORDER BY {field}"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()
        
        i = 0 
        while i < len(datos):
            ContractsFrames(self, 
                        proveedor = datos[i][0],
                        servicio = datos[i][-1],
                        objeto = datos[i][3],
                        autorizado = datos[i][4],
                        importe = datos[i][5],
                        fecha = datos[i][1],
                        vencimiento = datos[i][2])
            i +=1

                   
class ContractsFrames(ctk.CTkFrame):
    def __init__(self, master, proveedor, servicio, objeto, autorizado, importe, fecha, vencimiento):
        super().__init__(master = master,
                         height = 200,
                         fg_color = "white")
        
        self.master = master
        self.proveedor = ContractsProveedor(self, text = proveedor)
        self.service = ContractsService(self, text = f"Servicios {servicio}")
        self.objeto = ContractsObjeto(self, text = objeto)
        self.autorizado = ContractsAutorizado(self, text = f"Aut.firmar factura: {autorizado}")
        self.importe = ContractsImporte(self, importe = importe)
        self.fecha = ContractsFecha(self, text = f"Desde {fecha}")
        self.vencimiento = ContractsVencimiento(self, text = f"Hasta {vencimiento}")


        # events
        self.bind("<Button>", lambda event: self.evento())
        self.proveedor.bind("<Button>", lambda event: self.evento())
        self.service.bind("<Button>", lambda event: self.evento())
        self.objeto.bind("<Button>", lambda event: self.evento())
        self.autorizado.bind("<Button>", lambda event: self.evento())
        self.importe.bind("<Button>", lambda event: self.evento())
        self.fecha.bind("<Button>", lambda event: self.evento())
        self.vencimiento.bind("<Button>", lambda event: self.evento())

        self.pack(expand = True, fill = "x", padx = 5, pady = 5)
    
    def evento(self):
        self.datos = Datos(self, self.proveedor.text) 
        
        # Deletre button
        self.font = ctk.CTkFont("Helvetica", 15)
        self.deletemessage = Message(self.datos, 1.0,0.7,"Eliminar")
        
        self.aceptar = ctk.CTkButton(self.deletemessage, text = "Si", font = self.font, command = self.eliminar)
        self.aceptar.place(relx = 0.7, rely = 0.8, relwidth = 0.2)
        
        self.denegar = ctk.CTkButton(self.deletemessage, text = "No", font = self.font, command = self.deletemessage.animate)
        self.denegar.place(relx = 0.4, rely = 0.8, relwidth = 0.2)

        self.eliminar = ctk.CTkButton(self.datos, text = "Eliminar", font = self.font, command = self.deletemessage.animate)  
        self.eliminar.place(relx = 0.85, rely = 0.05, relwidth = 0.1)

    def eliminar(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
        instruccion = f"Select * FROM Contratos WHERE proveedor = '{self.datos.titulo}'"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        
        
        data_insert_query = ''' INSERT INTO Recuperar_Contratos 
                    (proveedor,
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
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        '''

        
        data_insert = []
        i = 0 
        while i < len(datos[0]):
            if i != 0 and i != 2 and i != 3:
                data_insert.append(datos[0][i])
            else: 
                data_insert.append("")
            i += 1
        
        data_insert_tuple = tuple(data_insert[1:])
        
        cursor.execute(data_insert_query, data_insert_tuple)
    
        instruccion = f"Delete FROM Contratos WHERE proveedor = '{self.datos.titulo}'"
        cursor.execute(instruccion)
        
        instruccion = f"DELETE FROM Servicios WHERE proveedor = '{self.datos.titulo}'"
        cursor.execute(instruccion)

        instruccion = f"DELETE FROM Autorizo_Junta WHERE proveedor = '{self.datos.titulo}'"
        cursor.execute(instruccion)

        conn.commit()
        conn.close()

        for child in self.master.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        self.master.create_frames()
        
        self.datos.destroy()



class ContractsProveedor(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 30, "bold"),
                         anchor = "w")
        
        self.text = text
        self.place(relx = 0.03, rely = 0.2,relwidth = 0.85, relheight= 0.4)


class ContractsObjeto(ctk.CTkLabel):
    def __init__(self, master, text):
        if len(text) >= 94:
            self.text = text[0:92] + "..."
        else:
            self.text = text
        
        super().__init__(master = master, 
                         text = self.text, 
                         font = ctk.CTkFont("Helvetica", 15),
                         anchor = "w")

        self.place(relx = 0.03, rely = 0.55, relwidth = 0.6, relheight= 0.2)
    

class ContractsAutorizado(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 15),
                         anchor = "w")

        self.text = text
        self.place(relx = 0.03, rely = 0.7, relwidth = 0.6, relheight= 0.2)


class ContractsService(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 15))
        
        self.text = text
        self.place(relx = 0.75, rely = 0.15, relwidth = 0.2, relheight= 0.1)


class ContractsImporte(ctk.CTkLabel):
    def __init__(self, master, importe):
        self.show_importe = ""
        
        if type(importe) == float:
            importe = int(importe)
        elif importe == None:
            importe = 0
            
        if len(str(importe)) < 4:
            self.show_importe = importe
        elif len(str(importe)) == 4:
            self.show_importe = str(importe)[0] + " " + str(importe)[1:] 
        elif len(str(importe)) == 5:
            self.show_importe = str(importe)[0:2] + " " + str(importe)[2:] 
        elif len(str(importe)) == 6:
            self.show_importe = str(importe)[0:3] + " " + str(importe)[3:] 
        elif len(str(importe)) == 7:
            self.show_importe = str(importe)[0] + " " + str(importe)[1:4] + " " + str(importe)[4:]
        else:
            self.show_importe = str(importe)[0:2] + " " + str(importe)[2:5] + " " + str(importe)[5:]

       


        if importe < 500000:
            self.show_color = "green"
        elif importe >= 500000 and importe < 800000:
            self.show_color = "orange"
        else:
            self.show_color = "red"


        super().__init__(master = master, 
                         text = self.show_importe, 
                         text_color = self.show_color,
                         font = ctk.CTkFont("Helvetica", 25, "bold"),)
        
        self.place(relx = 0.75, rely = 0.3, relwidth = 0.2, relheight= 0.2)


class ContractsFecha(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 15)) 
        self.text = text
        self.place(relx = 0.75, rely = 0.57, relwidth = 0.2, relheight= 0.1)


class ContractsVencimiento(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 15))
        
        self.text = text
        self.place(relx = 0.75, rely = 0.70, relwidth = 0.2, relheight= 0.1)










