import customtkinter as ctk 
import sqlite3

class Message(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, text):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        self.advertencia_label = ctk.CTkLabel(self, 
                                              text = f"¿Deseas {text} ?", 
                                              anchor = "e",
                                              font = ctk.CTkFont("Helvetica", 20, "bold"))
        self.advertencia_label.place(relx = 0.1, rely = 0.4)

        # layout 
        self.place(relx = self.start_pos, rely = 0.25, relwidth = self.width, relheight = 0.4)

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
        else:
            self.animate_backwards()
            self.tkraise()


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = self.pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

class OnlyNumbers(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        self.advertencia_label = ctk.CTkLabel(self, 
                                              text = f"Sólo pueden ser números", 
                                              anchor = "e",
                                              font = ctk.CTkFont("Helvetica", 20, "bold"))
        self.advertencia_label.place(relx = 0.1, rely = 0.4)

        self.button = ctk.CTkButton(self, text = "OK", command = self.animate)
        self.button.place(relx = 0.4, rely = 0.8, relheight = 0.1, relwidth = 0.2)

        # layout 
        self.place(relx = self.start_pos, rely = 0.25, relwidth = self.width, relheight = 0.4)

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
        else:
            self.animate_backwards()
            self.tkraise()


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = self.pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True




class Confirmation(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, text):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = ctk.CTkFont("Helvetica", 23, "bold"))
        self.label.place(relx = 0.07, rely = 0.07)
        
        self.debes_label = ctk.CTkLabel(self, text = "Debes llenar/actualizar:", anchor = "w", font = self.font)
        self.debes_label.place(relx = 0.07, rely = 0.15)

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.place(relx = 0.07, rely = 0.22, relwidth = 0.85, relheight = 0.65)
        
        self.ok = ctk.CTkButton(self, text = "OK", font = self.font, command = self.button_ok, hover_color = "green")
        self.ok.place(relx = 0.4, rely = 0.9, relwidth = 0.2)

        # layout 
        self.place(relx = self.start_pos, rely = 0.2, relwidth = self.width, relheight = 0.6)
    
    def button_ok(self):
        for child in self.scroll.winfo_children():
            child.destroy()
        self.animate()

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
        else:
            self.animate_backwards()

    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = self.pos, rely = 0.2, relwidth = self.width, relheight = 0.6)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.2, relwidth = self.width, relheight = 0.6)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

class ConfirmationFrame(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master,
                         height = 50,
                         fg_color = "white")

        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, font = self.font)
        self.label.place(relx = 0.05, rely = 0.25)

        self.pack(fill = "x", expand = True, padx = 5, pady = 5)



class Actualizar(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, text):
        super().__init__(master = master,
                         border_width = 3) 
        
        self.text = text

        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        # font
        self.font = ctk.CTkFont("Helvetica", 15)
        self.frames = []
        
        self.values = ["Proveedor","Área", "Fecha del contrato", "Fecha de vencimiento", "Dirección", "Código NIT", "Código REUP", "Código VERSAT", "Banco", "Sucursal bancaria", "Cuenta bancaria", "Titular de la cuenta", "Teléfono del titular", "Autorizo de la CCD/JDN"]
        self.options_menu = ctk.CTkOptionMenu(self, font = self.font, values = self.values, command = self.options)
        self.options_menu.place(relx = 0.3, rely = 0.1, relwidth = 0.4)
        
        self.scroll_frames = ctk.CTkScrollableFrame(self)
        self.scroll_frames.place(relx = 0.05, rely = 0.2, relwidth = 0.9)
        
        self.cancel_button = ctk.CTkButton(self, text = "Cancelar",font = self.font, command = self.animate, hover_color= "red")
        self.cancel_button.place(relx = 0.25, rely = 0.85, relheight = 0.1, relwidth = 0.2)

        
        # layout 
        self.place(relx = self.start_pos, rely = 0.25, relwidth = 0.4, relheight = 0.5) 

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            for child in self.scroll_frames.winfo_children():
                if child.widgetName == "frame":
                    child.destroy()
            self.frames = []
            self.values = ["Proveedor","Área", "Fecha del contrato", "Fecha de vencimiento", "Dirección", "Código NIT", "Código REUP", "Código VERSAT", "Banco", "Sucursal bancaria", "Cuenta bancaria", "Titular de la cuenta", "Teléfono del titular", "Autorizo de la CCD/JDN"]
            self.options_menu.configure(values = self.values)
            self.options_menu.set(self.values[0])

        else:
            self.animate_backwards()
            if self.text == "datos":
                self.master.actualizar.configure(state = "normal")
                self.master.eliminar.configure(state = "normal")
                self.master.ver_pdf.configure(state = "normal")
                self.master.cancel_button.configure(state = "normal")
                for child in self.master.servicios_scroll.winfo_children():
                    child.destroy()
                self.master.servicios()
                self.master.servicios_menu.set("0")

    def options(self, choice):
        self.values = [i for i in self.values if i != choice]
        if choice == "Fecha del contrato" or choice == "Fecha de vencimiento" or choice == "Fecha del acuerdo":
            frame = UpdateFechaLabel(self.scroll_frames, text = choice)
            self.frames.append(frame)
        elif choice == "Área":
            frame = UpdateArea(self.scroll_frames, text = choice)
            self.frames.append(frame)
        elif choice == "Autorizo de la CCD/JDN":
            frame = UpdateAutorizadoLabel(self.scroll_frames, text = choice)
            self.frames.append(frame)
        else:
            frame = UpdateLabel(self.scroll_frames, text = choice)
            self.frames.append(frame)
        self.options_menu.configure(values = self.values)


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.08 
            self.place(relx = self.pos, rely = 0.25, relwidth = 0.4, relheight = 0.5)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.08 
            self.place(relx = self.pos, rely = 0.25, relwidth = 0.4, relheight = 0.5)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

class UpdateArea(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         fg_color = "white",
                         height = 100)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.05)
        
        self.connect_database()

        self.entry = ctk.CTkOptionMenu(self, font = self.font, values = self.options)

        if self.master.master.master.master.text == "datos":
            self.entry.set(self.master.master.master.master.master.datos[0][2])
        elif self.master.master.master.master.text == "recuperar":
            self.entry.set(self.master.master.master.master.master.datos[0][1])
        self.entry.place(relx = 0.04, rely = 0.3, relwidth = 0.91)
        
        self.button = ctk.CTkButton(self, font = self.font, text = "cancelar",command = self.cancel, hover_color = "red")
        self.button.place(relx = 0.375, rely = 0.65, relwidth = 0.25)

        self.pack(fill = "x", expand = True, pady = 0.5, padx = 0.5)

    def cancel(self):
        self.master.master.master.master.frames = [i for i in self.master.master.master.master.frames if i != self]
        self.master.master.master.master.values.append(self.text)
        self.destroy()

    def connect_database(self):
        conn = sqlite3.connect("contratos.db")
        cursor = conn.cursor()

        instruccion = f"SELECT * FROM Area_que_Tramita"
        cursor.execute(instruccion)
        datos = cursor.fetchall()
        
        self.options = []
        for i in datos:
            self.options.append(i[0])

        conn.commit()
        conn.close()


class UpdateLabel(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         fg_color = "white",
                         height = 100)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.05)
        
        self.entry = ctk.CTkEntry(self, font = self.font)
        self.entry.place(relx = 0.04, rely = 0.3, relwidth = 0.91)
        
        self.button = ctk.CTkButton(self, font = self.font, text = "cancelar",command = self.cancel, hover_color = "red")
        self.button.place(relx = 0.375, rely = 0.65, relwidth = 0.25)

        self.pack(fill = "x", expand = True, pady = 0.5, padx = 0.5)

    def cancel(self):
        self.master.master.master.master.frames = [i for i in self.master.master.master.master.frames if i != self]
        self.master.master.master.master.values.append(self.text)
        self.destroy()

class UpdateAutorizadoLabel(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         fg_color = "white",
                         height = 200)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.05)
        
        self.acuerdo_label = ctk.CTkLabel(self, text = "Acuerdo", anchor = "w", font = self.font)
        self.acuerdo_label.place(relx = 0.05, rely = 0.24)

        self.acuerdo_entry = ctk.CTkEntry(self, font = self.font)
        self.acuerdo_entry.place(relx = 0.26, rely = 0.24, relwidth = 0.7)
        
        self.monto_label = ctk.CTkLabel(self, text = "Monto", anchor = "w", font = self.font)
        self.monto_label.place(relx = 0.05, rely = 0.43)

        self.monto_entry = ctk.CTkEntry(self, font = self.font)
        self.monto_entry.place(relx = 0.26, rely = 0.43, relwidth = 0.7)

        self.fecha_label = ctk.CTkLabel(self, text = "Fecha", anchor = "w", font = self.font)
        self.fecha_label.place(relx = 0.05, rely = 0.62)
        
        self.day = ctk.CTkOptionMenu(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.day.place(relx = 0.26, rely = 0.62)
        
        self.month = ctk.CTkOptionMenu(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.month.place(relx = 0.40, rely = 0.62)

        self.year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2031)], width = 70)
        self.year.place(relx = 0.68, rely = 0.62)    

        self.button = ctk.CTkButton(self, font = self.font, text = "cancelar", command= self.cancel, hover_color = "red")
        self.button.place(relx = 0.375, rely = 0.8, relwidth = 0.25)

        self.pack(fill = "x", expand = True, pady = 0.5, padx = 0.5)
        
    def cancel(self):
        self.master.master.master.master.frames = [i for i in self.master.master.master.master.frames if i != self]
        self.master.master.master.master.values.append(self.text)
        self.destroy()


class UpdateFechaLabel(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         fg_color = "white",
                         height = 100)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.05)
        
        self.day = ctk.CTkOptionMenu(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.day.place(relx = 0.05, rely = 0.3)
        
        self.month = ctk.CTkOptionMenu(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.month.place(relx = 0.19, rely = 0.3)

        self.year = ctk.CTkOptionMenu(self, values = [str(i) for i in range(2020, 2031)], width = 70)
        self.year.place(relx = 0.47, rely = 0.3)    

        self.button = ctk.CTkButton(self, font = self.font, text = "cancelar",command = self.cancel, hover_color= "red")
        self.button.place(relx = 0.375, rely = 0.65, relwidth = 0.25)

        self.pack(fill = "x", expand = True, pady = 0.5, padx = 0.5)

    def cancel(self):
        self.master.master.master.master.frames = [i for i in self.master.master.master.master.frames if i != self]
        self.destroy()

class Junta(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, monto, text):
        super().__init__(master = master,
                         border_width = 3) 
        self.master = master 
        self.text = text

        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True

        if len(str(monto)) < 7:
            self.show_monto = monto 
        elif len(str(monto)) == 7:
            self.show_monto = str(monto)[0] + " " + str(monto)[1:4] + " " + str(monto)[4:] 
        else:
            self.show_monto = str(monto)[0:2] + " " + str(monto)[2:5] + " " + str(monto)[5:] 


        self.atras_button = ctk.CTkButton(self, text = "OK", command = self.atras)
        self.atras_button.place(relx = 0.4, rely = 0.85, relheight = 0.1, relwidth = 0.2)
        
        self.advertencia_label = ctk.CTkLabel(self, 
                                              text = f"Excede el monto autorizado", 
                                              anchor = "e",
                                              font = ctk.CTkFont("Helvetica", 20, "bold"))
        self.advertencia_label.place(relx = 0.05, rely = 0.4, relheight = 0.1)
        
        self.monto_label = ctk.CTkLabel(self, 
                                              text = f"de {self.show_monto} cup", 
                                              anchor = "e",
                                              font = ctk.CTkFont("Helvetica", 20, "bold"))
        self.monto_label.place(relx = 0.05, rely = 0.5, relheight = 0.1)

        # layout 
        self.place(relx = self.start_pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
    
    def atras(self):
        i = 0
        if self.text == "contracts":
            while i < len(self.master.service.frames):
                self.master.service.frames[i].valor_entry.configure(state = "normal")    
                i +=1
        elif self.text == "anadir":
            for child in self.master.servicios_scroll.winfo_children():
                if child.text == "anadir":
                    child.valor_entry.configure(state = "normal")
        else:
            for child in self.master.servicios_scroll.winfo_children():
                child.valor_entry.configure(state = "normal")

        self.animate()

    def disabled_frames(self):
        if self.text == "contracts":
            i = 0
            while i < len(self.master.service.frames):
                self.master.service.frames[i].valor_entry.configure(state = "disabled")
                i +=1
        
        elif self.text == "anadir":
            for child in self.master.servicios_scroll.winfo_children():
                if child.text == "anadir":
                    child.valor_entry.configure(state = "disabled")

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.disabled_frames()
        else:
            self.animate_backwards()


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = self.pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7
            self.place(relx = self.pos, rely = 0.25, relwidth = self.width, relheight = 0.4)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True


class EliminarServicio(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, text):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        self.width = abs(start_pos - end_pos)
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True

        self.deseas_label = ctk.CTkLabel(self, 
                                              text = f"¿Deseas eliminar?", 
                                              anchor = "e",
                                              font = ctk.CTkFont("Helvetica", 15, "bold"))
        self.deseas_label.place(relx = 0.1, rely = 0.1)

        # layout 
        self.place(relx = self.start_pos, rely = 0.2, relwidth = 0.6, relheight = 0.5)

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
        else:
            self.animate_backwards()


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.8 
            self.place(relx = self.pos, rely = 0.2, relwidth = 0.6, relheight = 0.5)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.8
            self.place(relx = self.pos, rely = 0.2, relwidth = 0.6, relheight = 0.5)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True

