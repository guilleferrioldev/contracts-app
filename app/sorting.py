import customtkinter as ctk 
#from CTkScrollableDropdown import *

class Sort(ctk.CTkOptionMenu):
    def __init__(self, master, width,values, row, column, pady, sticky,variable, command):
        super().__init__(master= master,
                         width = width,
                         values = values,
                         variable = variable,
                         command = command,
                         state = "normal")

        self.set(values[0])
        self.grid(row = row, column = column, pady = pady, sticky = sticky)

