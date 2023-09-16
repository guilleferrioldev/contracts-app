import customtkinter as ctk

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

        self.scroll = ctk.CTkScrollableFrame(self)
        self.scroll.place(relx = 0.05, rely = 0.2, relwidth = 0.9, relheight = 0.6)
        
        self.search = ctk.CTkEntry(self, placeholder_text = "Buscar", font = self.font)
        self.search.place(relx = 0.51, rely = 0.1, relwidth = 0.3)

        Frames(self.scroll, "Tamara Ravelo")
        Frames(self.scroll, "Guillermo Ferriol")
        Frames(self.scroll, "Maykel Masó")

        self.new_object = ctk.CTkButton(self, text = "+", font = self.font)
        self.new_object.place(relx = 0.9, rely = 0.1, relwidth = 0.05)
        
        self.delete_object = ctk.CTkButton(self, text = "/", font = self.font)
        self.delete_object.place(relx = 0.83, rely = 0.1, relwidth = 0.05)

        self.cancel_button = ctk.CTkButton(self, text = "Cancelar", font = self.font, command = self.animate)
        self.cancel_button.place(relx = 0.25, rely = 0.85)
        
        self.guardar_button = ctk.CTkButton(self, text = "Guardar", font = self.font)
        self.guardar_button.place(relx = 0.55, rely = 0.85)

        # layout 
        self.place(relx = self.start_pos, rely = 0.1, relwidth = 0.7, relheight = 0.8)

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

class Frames(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master = master, 
                         height = 50,
                         fg_color = "white")

        self.check = ctk.CTkCheckBox(self, text = text, font = ctk.CTkFont("Helvetica", 15))
        self.check.place(relx = 0.05, rely = 0.3)

        self.pack(expand = True, fill = "x", pady = 5 , padx = 5)








