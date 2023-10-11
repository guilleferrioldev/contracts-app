import customtkinter as ctk 
from tkinter import filedialog
from tkinter import scrolledtext
from service import Service, Frames
from message import Message, Junta, Confirmation, ConfirmationFrame
from recorver import Recorver
from objeto import Object
import sqlite3
import sys
from pathlib import Path
import shutil
import datetime

class NewButton(ctk.CTkButton):
    def __init__(self, master, text, width,row, column, padx, pady, sticky, command):
        super().__init__(master = master,
                         text = text, 
                         width = width,
                         command = command)
        
        self.grid(row = row, column = column, padx = padx, pady = pady, sticky = sticky)


class SlidePanel(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos):
        super().__init__(master = master)

        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)
        

        # animation logic
        self.pos = self.end_pos
        self.in_start_pos = False

        # font
        font = ctk.CTkFont(family = "Helvetica", size = 15)
        
        # Nombre del proveedor
        self.proveedor_label = ctk.CTkLabel(self, text = "Nombre del proveedor", font = font)
        self.proveedor_label.place(relx = 0.05, rely =0.05,  relheight = 0.043)

        self.proveedor_entry = ctk.CTkEntry(self, font = font)
        self.proveedor_entry.place(relx = 0.2, rely =0.05, relwidth = 0.28,relheight = 0.043)
        
        # Área que tramita
        self.area_label = ctk.CTkLabel(self, text = "Área que tramita", font = font)
        self.area_label.place(relx = 0.05, rely = 0.10,  relheight = 0.043)
        
        self.area_frame = Object(self, 1.0, 0.7, "Área que tramita")
        self.area_button = ctk.CTkButton(self,text = "Área que tramita", command = self.area_frame.animate)
        self.area_button.place(relx = 0.2, rely = 0.10, relwidth = 0.28, relheight = 0.043)

        # Fecha del contrato
        self.fecha_label = ctk.CTkLabel(self, text = "Fecha del contrato", font = font)
        self.fecha_label.place(relx = 0.05, rely = 0.15,relheight = 0.043)

        self.fecha_day = ctk.CTkOptionMenu(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.fecha_day.place(relx = 0.2, rely = 0.15, relwidth = 0.07, relheight = 0.043)
        
        self.fecha_mes = ctk.CTkOptionMenu(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.fecha_mes.place(relx = 0.275, rely = 0.15,relwidth = 0.13, relheight = 0.043)

        
        self.fecha_year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2024)], width = 70)
        self.fecha_year.place(relx = 0.41, rely = 0.15,relwidth = 0.07, relheight = 0.043)

        # Fecha de vencimiento
        self.fecha_venc_label = ctk.CTkLabel(self, text = "Fecha de vencimiento", font = font)
        self.fecha_venc_label.place(relx = 0.05, rely = 0.20, relheight = 0.043)

        self.fecha_venc_day = ctk.CTkOptionMenu(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.fecha_venc_day.place(relx = 0.2, rely = 0.20,relwidth = 0.07, relheight = 0.043)
        
        self.fecha_venc_mes = ctk.CTkOptionMenu(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.fecha_venc_mes.place(relx = 0.275, rely = 0.20,relwidth = 0.13, relheight = 0.043)
        
        self.fecha_venc_year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2030)], width = 70)
        self.fecha_venc_year.place(relx = 0.41, rely = 0.20, relwidth = 0.07,  relheight = 0.043)

        # Objeto 
        self.objeto_label = ctk.CTkLabel(self, text =  "Objeto", font = font)
        self.objeto_label.place(relx = 0.05, rely = 0.25, relheight = 0.043)

        self.objeto_frame = Object(self, 1.0, 0.7, "Objeto")
        self.objeto_button = ctk.CTkButton(self,text = "Objeto",width = 300,  command = self.objeto_frame. animate)
        self.objeto_button.place(relx = 0.2, rely = 0.25, relwidth = 0.28, relheight = 0.043)

               
        # Direccion 
        self.direccion_label = ctk.CTkLabel(self, text = "Dirección", font = font)
        self.direccion_label.place(relx = 0.05, rely = 0.30, relheight = 0.043)

        self.direccion_entry = ctk.CTkEntry(self, width = 300, font = font)
        self.direccion_entry.place(relx = 0.2, rely = 0.30, relwidth = 0.28, relheight = 0.043)

        # Codigos
        self.nit_code_label = ctk.CTkLabel(self, text = "Código NIT", font = font)
        self.nit_code_label.place(relx = 0.05, rely = 0.35, relheight = 0.043)

        self.nit_code_entry = ctk.CTkEntry(self, font = font)
        self.nit_code_entry.place(relx = 0.2, rely = 0.35, relwidth = 0.28, relheight = 0.043)

        self.reup_code_label = ctk.CTkLabel(self, text = "Código REUP", font = font)
        self.reup_code_label.place(relx = 0.05, rely = 0.40, relheight = 0.043)

        self.reup_code_entry = ctk.CTkEntry(self, font = font)
        self.reup_code_entry.place(relx = 0.2, rely = 0.40, relwidth = 0.28,relheight = 0.043)
        
        self.versat_code_label = ctk.CTkLabel(self, text = "Código VERSAT", font = font)
        self.versat_code_label.place(relx = 0.05, rely = 0.45, relheight = 0.043)

        self.versat_code_entry = ctk.CTkEntry(self, font = font)
        self.versat_code_entry.place(relx = 0.2, rely = 0.45, relwidth = 0.28,relheight = 0.043)

        # Banco
        self.banco_label = ctk.CTkLabel(self, text = "Banco/Sucursal", font = font)
        self.banco_label.place(relx = 0.05, rely = 0.50, relheight = 0.043)

        self.banco_menu = ctk.CTkOptionMenu(self, values = ["Metropolitano","BPA", "BANDEC"])
        self.banco_menu.place(relx = 0.2, rely = 0.50, relwidth = 0.135, relheight = 0.043)
        
        self.sucursal_entry = ctk.CTkEntry(self, font = font)
        self.sucursal_entry.place(relx = 0.34, rely = 0.50, relwidth = 0.14, relheight = 0.043)

        self.cuenta_label = ctk.CTkLabel(self, text = "Cuenta bancaria", font = font)
        self.cuenta_label.place(relx = 0.05, rely = 0.55,  relheight = 0.043)

        self.cuenta_entry = ctk.CTkEntry(self, font = font)
        self.cuenta_entry.place(relx = 0.2, rely = 0.55, relwidth = 0.28, relheight = 0.043)
        
        self.titular_cuenta_label = ctk.CTkLabel(self, text = "Titular de la cuenta", font = font)
        self.titular_cuenta_label.place(relx = 0.05, rely = 0.60,  relheight = 0.043)

        self.titular_cuenta_entry = ctk.CTkEntry(self, font = font)
        self.titular_cuenta_entry.place(relx = 0.2, rely = 0.60, relwidth = 0.28, relheight = 0.043)
        
        self.telefono_label = ctk.CTkLabel(self, text = "Teléfono", font = font)
        self.telefono_label.place(relx = 0.05, rely = 0.65, relheight = 0.043)

        self.telefono_entry = ctk.CTkEntry(self, font = font)
        self.telefono_entry.place(relx = 0.2, rely = 0.65, relwidth = 0.28, relheight = 0.043)

        # autorizado
        self.autorizado_label = ctk.CTkLabel(self, text = "Aut.firmar factura", font = font)
        self.autorizado_label.place(relx = 0.05, rely = 0.70,  relheight = 0.043)
        
        self.autorizado_frame = Object(self, 1.0, 0.7, "Aut. firmar factura")
        self.autorizado_button = ctk.CTkButton(self,text = "Autorizado a firmar factura", command = self.autorizado_frame.animate)
        self.autorizado_button.place(relx = 0.2, rely = 0.70, relwidth = 0.28, relheight = 0.043)

        # junta
        self.junta_label = ctk.CTkLabel(self, text = "Autorizo de la CCD/JDN", font = font)
        self.junta_label.place(relx = 0.05, rely = 0.75,  relheight = 0.043)
        
        self.junta_var = ctk.StringVar(value = "off")
        self.junta_button = ctk.CTkCheckBox(self, text = "", command = self.enable,variable = self.junta_var, onvalue="on", offvalue="off") 
        self.junta_button.place(relx = 0.20, rely = 0.75, relheight = 0.043)
        
        self.acuerdo_label = ctk.CTkLabel(self, text = "(Acuerdo)", font = font)
        self.acuerdo_label.place(relx = 0.27, rely = 0.75, relheight = 0.043)
        
        self.acuerdo_junta_entry = ctk.CTkEntry(self, font = font, state = "disabled")
        self.acuerdo_junta_entry.place(relx = 0.34, rely = 0.75, relwidth = 0.14, relheight = 0.043)
        
        self.monto_label = ctk.CTkLabel(self, text = "Monto autorizado", font = font)
        self.monto_label.place(relx = 0.05, rely = 0.80, relheight = 0.043)
        
        self.monto_junta_entry = ctk.CTkEntry(self, font = font, state = "disabled")
        self.monto_junta_entry.place(relx = 0.2, rely = 0.80, relwidth = 0.28, relheight = 0.043)

        self.fecha_junta_label = ctk.CTkLabel(self, text = "Fecha de autorizo", font = font)
        self.fecha_junta_label.place(relx = 0.05, rely = 0.85, relheight = 0.043)

        self.fecha_junta_day = ctk.CTkOptionMenu(self, values = [str(i) for i in range(1, 32)], width = 55, state = "disabled")
        self.fecha_junta_day.place(relx = 0.2, rely = 0.85, relwidth = 0.07, relheight = 0.043)
        
        self.fecha_junta_mes = ctk.CTkOptionMenu(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110,
                                    state = "disabled")
        self.fecha_junta_mes.place(relx = 0.275, rely = 0.85,relwidth= 0.13, relheight = 0.043)

        
        self.fecha_junta_year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2024)], width = 70, state = "disabled")
        self.fecha_junta_year.place(relx = 0.41, rely = 0.85,relwidth = 0.07, relheight = 0.043)
        

        # servicios
        self.service = Service(self, relx = 0.55, rely = 0.05, relwidth = 0.4, relheight = 0.79)

        self.add_pdf = ctk.CTkButton(self, text = "Añadir PDF", command = self.copy_pdf)
        self.add_pdf.place(relx = 0.85, rely = 0.85, relwidth = 0.1, relheight = 0.043)

        self.menu = ctk.CTkOptionMenu(self.service, values = [str(i) for i in range(11)], command = self.validate_menu)
        self.menu.place(relx = 0.82, rely = 0.05,relwidth = 0.12, relheight = 0.05)
        
        self.path_adding_pdf = 0

        # Confirmation Message 
        self.confirmation = Confirmation(self, 1.0, 0.7, "Para Guardar")

        #Message box
        self.cancelmessage = Message(self, 1.0,0.7,"Cancelar")
        
        self.aceptar = ctk.CTkButton(self.cancelmessage, text = "Si", font = font, command = self.cancel, hover_color = "red")
        self.aceptar.place(relx = 0.7, rely = 0.8, relwidth = 0.2, relheight = 0.1)
        
        self.denegar = ctk.CTkButton(self.cancelmessage, text = "No", font = font, command = self.cancelmessage.animate, hover_color = "green")
        self.denegar.place(relx = 0.4, rely = 0.8, relwidth = 0.2, relheight = 0.1)
        
        self.savemessage = Message(self, 1.0,0.7,"Guardar") 

        self.aceptar = ctk.CTkButton(self.savemessage, text = "Si",font = font,command = self.insert_database, hover_color = "green")
        self.aceptar.place(relx = 0.7, rely = 0.8, relwidth = 0.2)
        
        self.denegar = ctk.CTkButton(self.savemessage, text = "No",font = font, command = self.savemessage.animate, hover_color = "red")
        self.denegar.place(relx = 0.4, rely = 0.8, relwidth = 0.2)

        # Setting buttons
        self.cancel_button = ctk.CTkButton(self, text = "Cancelar", font = font, command = self.cancelmessage.animate, hover_color = "red")
        self.cancel_button.place(relx = 0.25, rely = 0.94, relwidth = 0.11, relheight = 0.043)

        self.recuperar_button = ctk.CTkButton(self, text = "Recuperar",font = font,hover_color = "orange", command = lambda : Recorver(self, 1.0,0.7).animate())
        self.recuperar_button.place(relx = 0.59, rely = 0.94,relwidth = 0.11, relheight = 0.043)

        # layout 
        self.place(relx = self.end_pos, rely = 0.01, relwidth = self.width, relheight = 0.98)
        
    def copy_pdf(self):
        filename = filedialog.askopenfilename(title = "Copiar pdf", initialdir = "~")
        if filename:
            self.path = Path(filename)
            self.path_adding_pdf = 1


    def cancel(self):
        self.cancelmessage.animate()
        self.animate()

    def validate_menu(self, choice):
        validate = 0
        for child in self.objeto_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    validate = 1 

        if validate:
            self.options(choice)
        else:
            self.objeto_frame.animate()
            self.menu.set("0")

    def options(self, choice):
        self.service.frames = []
        self.service.importe_label.configure(text = f"Importe: 0.00 CUP")
        
        for child in self.service.scroll_frame.winfo_children():
            if child.widgetName == "frame":
                child.destroy()

        for number in range(int(choice)):
            frames = Frames(self.service.scroll_frame, "contracts")
            self.service.frames.append(frames)
        
    def suma(self):
        i = 0
        importe = 0
        values = [] 
        while i < len(self.service.frames):
            values.append(self.service.frames[i].valor_entry.get())
            i+=1
        
        for val in values:
            if val != "":
                importe += int(val)
        
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
       
        if self.junta_button.get() == "off":
            if importe < 1000000:
                self.service.importe_label.configure(text = f"Importe: {show_importe} CUP")
            else:
                self.junta_message = Junta(self, 1.0, 0.7, 1000000).animate()
        else:
            if importe < int(self.monto_junta_entry.get()):
                self.service.importe_label.configure(text = f"Importe: {show_importe} CUP")
            else:
                self.junta_message = Junta(self, 1.0, 0.7, self.monto_junta_entry.get()).animate()


    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
            self.proveedor_entry.delete(0, "end")
            self.direccion_entry.delete(0, "end")
            self.nit_code_entry.delete(0, "end")
            self.reup_code_entry.delete(0, "end")
            self.versat_code_entry.delete(0, "end")
            self.sucursal_entry.delete(0, "end")
            self.cuenta_entry.delete(0, "end")
            self.titular_cuenta_entry.delete(0, "end")
            self.telefono_entry.delete(0, "end") 
            self.master.master.sort_var.set("Proveedor")
            self.master.master.buscar()
            for child in self.area_frame.scroll.winfo_children():
                if child.widgetName == "frame":
                    if child.text != "insert":
                        child.check_var.set("off")
                    else:
                        child.destroy()
            for child in self.objeto_frame.scroll.winfo_children():
                if child.widgetName == "frame":
                    if child.text != "insert":
                        child.check_var.set("off")
                    else:
                        child.destroy()
            for child in self.autorizado_frame.scroll.winfo_children():
                if child.widgetName == "frame":
                    if child.text != "insert":
                        child.check_var.set("off")
                    else:
                        child.destroy()
        else:
            self.animate_backwards()
            self.tkraise()
            self.menu.set("0")
            for child in self.service.scroll_frame.winfo_children():
                if child.widgetName == "frame":
                    child.destroy()
            self.service.frames.clear()
            self.junta_var.set("off")        
            self.acuerdo_junta_entry.delete(0, "end")
            self.monto_junta_entry.delete(0,"end")
            self.banco_menu.set("Metropolitano")
            self.fecha_day.set(1) 
            self.fecha_mes.set("Enero") 
            self.fecha_year.set(2020) 
            self.fecha_venc_day.set(1) 
            self.fecha_venc_mes.set("Enero") 
            self.fecha_venc_year.set(2020) 
            self.fecha_junta_day.set(1) 
            self.fecha_junta_mes.set("Enero") 
            self.fecha_junta_year.set(2020) 
            self.acuerdo_junta_entry.configure(state = "disabled")
            self.monto_junta_entry.configure(state = "disabled")
            self.fecha_junta_day.configure(state = "disabled") 
            self.fecha_junta_mes.configure(state = "disabled") 
            self.fecha_junta_year.configure(state = "disabled") 
            self.service.importe_label.configure(text = "Importe: 0.00 CUP") 


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.08 
            self.place(relx = self.pos, rely = 0.01, relwidth = self.width, relheight = 0.98)
            self.after(1, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.08 
            self.place(relx = 0.01, rely = 0.01, relwidth = self.width, relheight = 0.98)
            self.after(1, self.animate_backwards)
         else:
            self.in_start_pos = True

    def enable(self):
        if self.junta_var.get() == "on":
            self.monto_junta_entry.configure(state = "normal") 
            self.acuerdo_junta_entry.configure(state = "normal")
            self.fecha_junta_day.configure(state = "normal") 
            self.fecha_junta_mes.configure(state = "normal") 
            self.fecha_junta_year.configure(state = "normal")
        else:
            self.acuerdo_junta_entry.delete(0, "end")
            self.monto_junta_entry.delete(0,"end")
            self.monto_junta_entry.configure(state = "disabled")
            self.acuerdo_junta_entry.configure(state = "disabled")
            self.fecha_junta_day.configure(state = "disabled") 
            self.fecha_junta_mes.configure(state = "disabled") 
            self.fecha_junta_year.configure(state = "disabled") 
    
    def confirmar(self):
        if self.proveedor_entry.get() == "":
            ConfirmationFrame(self.confirmation.scroll, text = "Proveedor")
        
        area = 0
        for child in self.area_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    area = 1
        
        if area == 0:
            ConfirmationFrame(self.confirmation.scroll, text = "Área que tramita")

        objeto = 0
        for child in self.objeto_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    objeto = 1
        
        if objeto == 0:
            ConfirmationFrame(self.confirmation.scroll, text = "Objetos")

        autorizado = 0
        for child in self.autorizado_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    autorizado = 1

        if autorizado == 0:
            ConfirmationFrame(self.confirmation.scroll, text = "Aut.firmar factura")        

        fecha_de_vencimiento = self.convert(f"{self.fecha_venc_day.get()}/{self.fecha_venc_mes.get()}/{self.fecha_venc_year.get()}")

        if fecha_de_vencimiento.date() < datetime.datetime.now().date():
            fecha = 0
            ConfirmationFrame(self.confirmation.scroll, text = "Fecha de Vencimiento")    
        else:
            fecha = 1 

        if all([self.proveedor_entry.get(), area, objeto, autorizado, fecha]):
            self.savemessage.animate()
        else:
            self.confirmation.animate()
    
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
        
        format = '%d/%b/%Y'
        datetime_str = datetime.datetime.strptime(res, format)
 
        return datetime_str



    def insert_database(self):
        # Contract data
        proveedor = (self.proveedor_entry.get()[0]).upper() + self.proveedor_entry.get()[1:] if len(self.proveedor_entry.get())>0 else ""
        fecha_del_contrato = f"{self.fecha_day.get()}/{self.fecha_mes.get()}/{self.fecha_year.get()}"
        fecha_de_vencimiento = f"{self.fecha_venc_day.get()}/{self.fecha_venc_mes.get()}/{self.fecha_venc_year.get()}"
        objeto = ""
        for child in self.objeto_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    objeto += f"{child.text} ,"
        objeto = objeto[:-2]
        area = ""
        for child in self.area_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    area += f"{child.text} ,"
        area = area[:-2]
        direccion = self.direccion_entry.get()
        codigo_nit = self.nit_code_entry.get()
        codigo_reup = self.reup_code_entry.get()
        codigo_versat = self.versat_code_entry.get()
        banco = self.banco_menu.get()
        sucursal = self.sucursal_entry.get()
        titular = self.titular_cuenta_entry.get()
        cuenta = self.cuenta_entry.get()
        telefono = self.telefono_entry.get()
        autorizado_por = ""
        for child in self.autorizado_frame.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.check_var.get() == "on":
                    autorizado_por += f"{child.text} ,"
        autorizado_por = autorizado_por[:-2]
        autorizo_junta = "si" if self.junta_button.get() == "on" else "no"
        acuerdo_junta = self.acuerdo_junta_entry.get() if autorizo_junta == "si" else ""
        monto_junta = self.monto_junta_entry.get() if autorizo_junta == "si" else 0 
        fecha_de_autorizo = f"{self.fecha_junta_day.get()}/{self.fecha_junta_mes.get()}/{self.fecha_junta_year.get()}" if autorizo_junta == "si" else ""

        # Contracts table
        conn  = sqlite3.connect("contratos.db")
         
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

        data_insert_tuple = (proveedor, area, fecha_del_contrato, fecha_de_vencimiento,
                             objeto, direccion, codigo_nit, codigo_reup, 
                             codigo_versat, banco, sucursal,
                             cuenta,titular, telefono, autorizado_por)
        
        cursor = conn.cursor()
        cursor.execute(data_insert_query, data_insert_tuple)

        # Junta table           
        data_insert_query_junta = ''' INSERT INTO Autorizo_Junta 
                            (proveedor,
                            acuerdo_junta,
                            monto_junta,
                            fecha_de_autorizo)
                            VALUES (?,?,?,?)
        '''

        data_insert_tuple_junta = (proveedor,
                            acuerdo_junta,
                            monto_junta,
                            fecha_de_autorizo)
        
        if self.junta_button.get() == "on":    
            cursor.execute(data_insert_query_junta, data_insert_tuple_junta)
    
        i = 0
        while i < int(self.menu.get()):
            proveedor = (self.proveedor_entry.get()[0]).upper() + self.proveedor_entry.get()[1:] if len(self.proveedor_entry.get()) > 0 else ""
            nombre_del_servicio = self.service.frames[i].nombre_servicio_entry.get() if self.menu.get() != "0" else "" 
            descripcion = self.service.frames[i].desc_servicio_entry.get() if self.menu.get() != "0" else "" 
            no_factura = self.service.frames[i].factura_entry.get() if self.menu.get() != "0" else "" 
            fecha_servicio = f"{self.service.frames[i].fecha_serv_day.get()}/{self.service.frames[i].fecha_serv_mes.get()}/{self.service.frames[i].fecha_serv_year.get()}" if self.menu.get() != "0" else "" 
            pagado = self.service.frames[i].pagado_entry.get() if self.menu.get() != "0" else "" 
            valor = self.service.frames[i].valor_entry.get() if self.menu.get() != "0" else 0.0 
            i += 1
                
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

        if self.path_adding_pdf:
            shutil.copy(self.path, f"./pdfs/{proveedor}.pdf")
        
    
        self.savemessage.animate()
        self.master.master.buscar()
        self.animate()
        
