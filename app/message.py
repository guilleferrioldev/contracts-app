import customtkinter as ctk 
from service import Frames


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



class Actualizar(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos):
        super().__init__(master = master,
                         border_width = 3) 
        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        # font
        self.font = ctk.CTkFont("Helvetica", 15)
        self.frames = []

        self.values = ["Proveedor", "Objeto", "Fecha del contrato", "Fecha de vencimiento", "Dirección", "Código NIT", "Código REUP", "Código VERSAT", "Banco", "Sucursal bancaria", "Cuenta bancaria", "Titular de la cuenta", "Teléfono del titular", "Aut.firmar factura"]
        self.options_menu = ctk.CTkOptionMenu(self, font = self.font, values = self.values, command = self.options)
        self.options_menu.place(relx = 0.3, rely = 0.1, relwidth = 0.4)
        
        self.scroll_frames = ctk.CTkScrollableFrame(self)
        self.scroll_frames.place(relx = 0.05, rely = 0.2, relwidth = 0.9)
        
        self.cancel_button = ctk.CTkButton(self, text = "Cancelar", font = self.font, command = self.animate)
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
            self.values = ["Proveedor", "Objeto", "Fecha del contrato", "Fecha de vencimiento", "Dirección", "Código NIT", "Código REUP", "Código VERSAT", "Banco", "Sucursal bancaria", "Cuenta bancaria", "Titular de la cuenta", "Teléfono del titular", "Aut.firmar factura"]
            self.options_menu.configure(values = self.values)
            self.options_menu.set(self.values[0])

        else:
            self.animate_backwards()
            

    def options(self, choice):
        self.values = [i for i in self.values if i != choice]
        if choice == "Fecha del contrato" or choice == "Fecha de vencimiento":
            frame = UpdateFechaLabel(self.scroll_frames, text = choice)
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

class UpdateLabel(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"],
                         height = 70)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.05)
        
        self.entry = ctk.CTkEntry(self, font = self.font)
        self.entry.place(relx = 0.04, rely = 0.4, relwidth = 0.91)

        self.pack(fill = "x", expand = True, pady = 0.5, padx = 0.5)


class UpdateFechaLabel(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         fg_color = ctk.ThemeManager.theme["CTkButton"]["fg_color"],
                         height = 70)
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, anchor = "w", font = self.font)
        self.label.place(relx = 0.05, rely = 0.05)
        
        self.day = ctk.CTkComboBox(self, values = [str(i) for i in range(1, 32)], width = 55)
        self.day.place(relx = 0.05, rely = 0.4)
        
        self.month = ctk.CTkComboBox(self, 
                                    values = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
                                    width = 110)
        self.month.place(relx = 0.19, rely = 0.4)

        self.year = ctk.CTkComboBox(self, values = [str(i) for i in range(2020, 2024)], width = 70)
        self.year.place(relx = 0.47, rely = 0.4)

        self.pack(fill = "x", expand = True, pady = 0.5, padx = 0.5)



class Junta(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, monto):
        super().__init__(master = master,
                         border_width = 3) 
        self.master = master 

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


        self.atras_button = ctk.CTkButton(self, text = "OK", command = self.animate)
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

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            i = 0
            while i < len(self.master.service.frames):
                self.master.service.frames[i].valor_entry.configure(state = "disabled")
                i +=1
        else:
            self.animate_backwards()
            i = 0
            while i < len(self.master.service.frames):
                self.master.service.frames[i].valor_entry.configure(state = "normal")
                i +=1


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




class Anadir(ctk.CTkFrame):
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
        
        self.label = ctk.CTkLabel(self, text = text, font = ctk.CTkFont("Helvetica", 20, "bold"))
        self.label.place(relx = 0.05, rely = 0.05, relwidth = 0.6)

        self.anadir_frame = Frames(self, "anadir")

        
        # layout 
        self.place(relx = self.start_pos, rely = 0.3, relwidth = 0.4, relheight = 0.5)

    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
        else:
            self.animate_backwards()
            self.anadir_frame.desc_servicio_entry.delete(0,"end")      
            self.anadir_frame.factura_entry.delete(0,"end")       
            self.anadir_frame.fecha_serv_day.set(1) 
            self.anadir_frame.fecha_serv_mes.set("Enero")
            self.anadir_frame.fecha_serv_year.set(2020)   
            self.anadir_frame.pagado_entry.delete(0,"end")       
            self.anadir_frame.valor_entry.delete(0,"end") 


    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.7 
            self.place(relx = self.pos, rely = 0.3, relwidth = 0.4, relheight = 0.5)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.7 
            self.place(relx = self.pos, rely = 0.3, relwidth = 0.4, relheight = 0.5)
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

