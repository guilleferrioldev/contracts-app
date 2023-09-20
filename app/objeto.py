import customtkinter as ctk
from message import Message
import sqlite3

class Object(ctk.CTkFrame):
    def __init__(self, master, start_pos, end_pos, text):
        super().__init__(master = master, 
                         border_width = 3)

        # general attributtes 
        self.start_pos = start_pos + 0.01
        self.end_pos = end_pos 
        
        # animation logic
        self.pos = self.start_pos
        self.in_start_pos = True
        
        self.text = text 

        self.font = ctk.CTkFont("Helvetica", 15)

        self.label = ctk.CTkLabel(self, text = self.text, font = ctk.CTkFont("Helvetica", 25, "bold"))
        self.label.place(relx = 0.05, rely = 0.08)

        self.scroll = Scroll(self, self.text)
        
        self.search = ctk.CTkEntry(self, placeholder_text = "Buscar", font = self.font)
        self.search.place(relx = 0.49, rely = 0.1, relwidth = 0.37)
        self.search.bind("<KeyRelease>", lambda event : self.searching())

        self.new_object = ctk.CTkOptionMenu(self, values = [str(i) for i in range(9)], font = self.font, command = self.insert)
        self.new_object.place(relx = 0.88, rely = 0.1, relwidth = 0.07)
        
        self.create_frames()

        self.cancel_button = ctk.CTkButton(self, text = "Cancelar", font = self.font, command = self.cancel)
        self.cancel_button.place(relx = 0.25, rely = 0.85)
        
        self.guardar_button = ctk.CTkButton(self, text = "Guardar", font = self.font, command = self.animate)
        self.guardar_button.place(relx = 0.55, rely = 0.85)

        # layout 
        self.place(relx = self.start_pos, rely = 0.1, relwidth = 0.7, relheight = 0.8)

    def cancel(self):
        for child in self.scroll.winfo_children():
            if child.widgetName == "frame":
                if child.text != "insert":
                    child.check_var.set("off")
                else:
                    child.destroy()

                self.new_object.set("0")
        
        self.animate()
            
    def searching(self):
        for child in self.scroll.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        
        if self.text == "Aut. firmar factura":
            tabla = "Autorizado_Firmar_Factura"
            row = "autorizado_por"
        else:
            tabla = "Objetos"
            row = "objeto"

        conn  = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
            
        instruction = f"Select * FROM {tabla} WHERE {row} like '%{self.search.get()}%' ORDER BY {row}"
        cursor.execute(instruction)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()

        i = 0 
        while i < len(datos):
            Frames(self.scroll, datos[i][0])
            i += 1



    def animate(self):
        if self.in_start_pos:
            self.animate_fordward()
            self.tkraise()
        else:
            self.animate_backwards()
            self.tkraise()

    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.87 
            self.place(relx = self.pos, rely = 0.1, relwidth = 0.7, relheight = 0.8)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.87 
            self.place(relx = self.pos, rely = 0.1, relwidth = 0.7, relheight = 0.8)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True
    
    def create_frames(self):
        if self.text == "Aut. firmar factura":
            tabla = "Autorizado_Firmar_Factura"
            order = "autorizado_por"
        else:
            tabla = "Objetos"
            order = "objeto"

        conn  = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
            
        instruction = f"Select * FROM {tabla} ORDER BY {order}"
        cursor.execute(instruction)
        datos = cursor.fetchall()

        conn.commit()
        conn.close()

        i = 0 
        while i < len(datos):
            Frames(self.scroll, datos[i][0])
            i += 1
        

    def insert(self, choice):
        for child in self.scroll.winfo_children():
            if child.widgetName == "frame":
                child.destroy()
        
        i = 0
        while i < int(choice):
            FramesInsert(self.scroll)
            i += 1
        
        self.create_frames()
        
        

class Scroll(ctk.CTkScrollableFrame):
    def __init__(self, master, text):
        super().__init__(master = master)
        self.master = master
        self.text = text
        self.place(relx = 0.05, rely = 0.2, relwidth = 0.9, relheight = 0.6)


class Frames(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         height = 50,
                         fg_color = "white")
        
        self.text = text
        self.font = ctk.CTkFont("Helvetica", 15)
        
        self.check_var = ctk.StringVar(value = "off")
        self.check = ctk.CTkCheckBox(self, text = self.text, font = self.font,variable = self.check_var, onvalue = "on", offvalue = "off")
        self.check.place(relx = 0.05, rely = 0.25)
        
        self.message = Message(self.master.master, 1.0, 0.7 , "Eliminar")
        
        self.message_cancel = ctk.CTkButton(self.message, text = "Cancel", command = self.message.animate)
        self.message_cancel.place(relx = 0.2, rely = 0.8, relwidth = 0.25)
        
        self.message_ok = ctk.CTkButton(self.message, text = "Aceptar", command = self.delete)
        self.message_ok.place(relx = 0.6, rely = 0.8, relwidth = 0.25)

        self.delete_button = ctk.CTkButton(self, text = "ELiminar", command = self.message.animate)
        self.delete_button.place(relx = 0.87, rely = 0.25, relwidth = 0.1)

        self.pack(expand = True, fill = "x", pady = 5 , padx = 5)

    def delete(self):
        if self.master.master.text == "Aut. firmar factura":
            tabla = "Autorizado_Firmar_Factura"
            row = "autorizado_por"
        else:
            tabla = "Objetos"
            row = "objeto"

        conn  = sqlite3.connect("contratos.db")
        cursor = conn.cursor()
            
        instruction = f"DELETE FROM {tabla} WHERE {row} = '{self.text}'" 
        cursor.execute(instruction)

        conn.commit()
        conn.close()
        
        self.destroy()
        self.message.animate()

class FramesInsert(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master = master, 
                         height = 50,
                         fg_color = "white")
        
        self.master = master
        self.text = "insert"

        self.font = ctk.CTkFont("Helvetica", 15)

        self.entry = ctk.CTkEntry(self, font = self.font)
        self.entry.place(relx = 0.03, rely = 0.25, relwidth = 0.8)
        
        self.button = ctk.CTkButton(self, text = "Insertar", font = self.font, command = self.insert)
        self.button.place(relx = 0.84, rely = 0.25, relwidth = 0.15)

        self.pack(expand = True, fill = "x", pady = 5 , padx = 5)

    def insert(self):
        if self.master.master.text == "Aut. firmar factura":
            conn  = sqlite3.connect("contratos.db")
            cursor = conn.cursor()

            data_insert_query = f'''INSERT INTO Autorizado_Firmar_Factura
                (autorizado_por,
                marcado) VALUES (?,?)
            '''

            data_insert_tuple = (
                self.entry.get(),
                0
                )

            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()
            
            Frames(self.master.master.scroll, self.entry.get())
            self.destroy()
        
        else:
            conn  = sqlite3.connect("contratos.db")
            cursor = conn.cursor()

            data_insert_query = f'''INSERT INTO Objetos
                (objeto,
                marcado) VALUES (?,?)
            '''

            data_insert_tuple = (
                self.entry.get(),
                0
                )

            cursor.execute(data_insert_query, data_insert_tuple)
            conn.commit()
            conn.close()
            
            Frames(self.master.master.scroll, self.entry.get())
            self.destroy()






