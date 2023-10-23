import customtkinter as ctk 
from datos_contratos import Datos
from message import Message
import sqlite3
import os
import datetime


class Contracts(ctk.CTkScrollableFrame):
    def __init__(self, master, row, column, columnspan, padx, pady, sticky):
        super().__init__(master = master)
        
        self.create_frames()        

        self.grid(row = row, column = column, columnspan = columnspan,padx = padx, pady = pady, sticky = sticky)


    def create_frames(self):        
        conn = sqlite3.connect("contratos.db") 
        cursor = conn.cursor()
               
        instruccion = "SELECT proveedor,area, fecha_del_contrato, fecha_de_vencimiento, objeto, autorizado_por,(SELECT sum(valor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS valor, (SELECT count(proveedor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS count FROM Contratos ORDER BY proveedor"
        cursor.execute(instruccion)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()
        
        i = 0 
        while i < len(datos):
            ContractsFrames(self, 
                        proveedor = datos[i][0],
                        area = datos[i][1],
                        servicio = datos[i][-1],
                        objeto = datos[i][4],
                        autorizado = datos[i][5],
                        importe = datos[i][-2],
                        fecha = datos[i][2],
                        vencimiento = datos[i][3])
            i +=1
                
    def readOrdered(self, searching, field):
        if field == "Proveedor":
            field = "proveedor"
        elif field == "Área":
            field = "area"
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
        
        if field != "fecha_del_contrato" and field != "fecha_de_vencimiento":
            instruccion = f"SELECT proveedor, area, fecha_del_contrato, fecha_de_vencimiento, objeto, autorizado_por, (SELECT sum(valor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS valor, (SELECT count(proveedor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS count FROM Contratos WHERE proveedor like '%{searching}%' ORDER BY {field}"
            cursor.execute(instruccion)
            datos = cursor.fetchall()

        elif field == "fecha_del_contrato":
            instruccion = f"SELECT proveedor, area, fecha_del_contrato, fecha_de_vencimiento, objeto, autorizado_por, (SELECT sum(valor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS valor, (SELECT count(proveedor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS count FROM Contratos WHERE proveedor like '%{searching}%'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
            
            reserva = []
            i = 0 
            while i < len(datos):
                reserva.append(list(datos[i]))
                i += 1
                        
            i = 0 
            while i < len(reserva):
                reserva[i][2] = self.convert(reserva[i][2])
                i += 1

            datos = sorted(reserva, key=lambda x: datetime.datetime.strptime(x[2],'%d/%b/%Y'))
            
            i = 0 
            while i < len(datos):
                datos[i][2] = self.unconvert(datos[i][2])
                i += 1
        
        elif field == "fecha_de_vencimiento":
            instruccion = f"SELECT proveedor, area, fecha_del_contrato, fecha_de_vencimiento, objeto, autorizado_por, (SELECT sum(valor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS valor, (SELECT count(proveedor) FROM Servicios WHERE Servicios.proveedor=Contratos.proveedor) AS count FROM Contratos WHERE proveedor like '%{searching}%'"
            cursor.execute(instruccion)
            datos = cursor.fetchall()
            
            reserva = []
            i = 0 
            while i < len(datos):
                reserva.append(list(datos[i]))
                i += 1
                        
            i = 0 
            while i < len(reserva):
                reserva[i][3] = self.convert(reserva[i][3])
                i += 1

            datos = sorted(reserva, key=lambda x: datetime.datetime.strptime(x[3],'%d/%b/%Y'))
            
            i = 0 
            while i < len(datos):
                datos[i][3] = self.unconvert(datos[i][3])
                i += 1

        conn.commit()
        conn.close()
    
        i = 0 
        while i < len(datos):
            ContractsFrames(self, 
                        proveedor = datos[i][0],
                        area = datos[i][1],
                        servicio = datos[i][-1],
                        objeto = datos[i][4],
                        autorizado = datos[i][5],
                        importe = datos[i][-2],
                        fecha = datos[i][2],
                        vencimiento = datos[i][3])
            i +=1
    
    def convert(self, date_time):
        date = date_time.split("/")
        
        if date[1] == "Enero":
            month = "Jan"
        elif date[1] == "Febrero":
            month = "Feb"
        elif date[1] == "Marzo":
            month = "Mar"
        elif date[1] == "Abril":
            month = "Apr"
        elif date[1] == "Mayo":
            month = "May"
        elif date[1] == "Junio":
            month = "Jun"
        elif date[1] == "Julio":
            month = "Jul"
        elif date[1] == "Agosto":
            month = "Aug"
        elif date[1] == "Septiembre":
            month = "Sep"
        elif date[1] == "Octubre":
            month = "Oct"
        elif date[1] == "Noviembre":
            month = "Nov"
        elif date[1] == "Diciembre":
            month = "Dec"
        
        date[1] =  month 
        res = "/".join(date)
        
        return res
    
    def unconvert(self, date_time):
        date = date_time.split("/")
        
        if date[1] == "Jan":
            month = "Enero"
        elif date[1] == "Feb":
            month = "Febrero"
        elif date[1] == "Mar":
            month = "Marzo"
        elif date[1] == "Apr":
            month = "Abril"
        elif date[1] == "May":
            month = "Mayo"
        elif date[1] == "Jun":
            month = "Junio"
        elif date[1] == "Jul":
            month = "Julio"
        elif date[1] == "Aug":
            month = "Agosto"
        elif date[1] == "Sep":
            month = "Septiembre"
        elif date[1] == "Oct":
            month = "Octubre"
        elif date[1] == "Nov":
            month = "Noviembre"
        elif date[1] == "Dec":
            month = "Diciembre"
        
        date[1] =  month 
        res = "/".join(date)
        
        return res


                   
class ContractsFrames(ctk.CTkFrame):
    def __init__(self, master, proveedor, area, servicio, objeto, autorizado, importe, fecha, vencimiento):
        super().__init__(master = master,
                         height = 200,
                         fg_color = "white")

        self.master = master
        self.proveedor = ContractsProveedor(self, text = proveedor)
        self.area = ContractsArea(self, text = f"Área: {area}")
        self.service = ContractsService(self, text = f"Servicios {servicio}")
        self.objeto = ContractsObjeto(self, text = f"Objetos: {objeto}")
        self.autorizado = ContractsAutorizado(self, text = f"Aut.firmar factura: {autorizado}")
        self.importe = ContractsImporte(self, importe = importe)
        self.fecha = ContractsFecha(self, text = f"Desde {fecha}")
        self.vencimiento = ContractsVencimiento(self, text = f"Hasta {vencimiento}")


        # events
        self.bind("<Button>", lambda event: self.evento())
        self.proveedor.bind("<Button>", lambda event: self.evento())
        self.area.bind("<Button>", lambda event: self.evento())
        self.service.bind("<Button>", lambda event: self.evento())
        self.objeto.bind("<Button>", lambda event: self.evento())
        self.autorizado.bind("<Button>", lambda event: self.evento())
        self.importe.bind("<Button>", lambda event: self.evento())
        self.fecha.bind("<Button>", lambda event: self.evento())
        self.vencimiento.bind("<Button>", lambda event: self.evento())

        self.pack(expand = True, fill = "x", padx = 5, pady = 5)
    
    def evento(self):
        self.datos = Datos(self, self.proveedor.text) 

class ContractsProveedor(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 30, "bold"),
                         anchor = "w")
        
        self.text = text
        self.place(relx = 0.03, rely = 0.1,relwidth = 0.7, relheight= 0.4)


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

        self.place(relx = 0.03, rely = 0.45, relwidth = 0.7, relheight= 0.15)


class ContractsArea(ctk.CTkLabel):
    def __init__(self, master, text):        
        super().__init__(master = master,
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 15),
                         anchor = "w")
        
        self.text = text
        self.place(relx = 0.03, rely = 0.72, relwidth = 0.7, relheight= 0.15)
  

class ContractsAutorizado(ctk.CTkLabel):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         text = text, 
                         font = ctk.CTkFont("Helvetica", 15),
                         anchor = "w")

        self.text = text
        self.place(relx = 0.03, rely = 0.58, relwidth = 0.7, relheight= 0.15)


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










