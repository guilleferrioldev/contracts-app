import customtkinter as ctk 

class Dashboard(ctk.CTkFrame):
    def __init__(self, master, row, column, columnspan, padx, pady, sticky):
        super().__init__(master = master)

        self.grid(row = row, column = column, columnspan = columnspan,padx = padx, pady = pady, sticky = sticky)

