import customtkinter as ctk
from PIL import Image
import fitz
from threading import Thread
import math
import io
import os

class CTkPDFViewer(ctk.CTkScrollableFrame):

    def __init__(self,
                 master: any,
                 file: str,
                 page_width: int = 600,
                 page_height: int = 700,
                 page_separation_height: int = 2,
                 **kwargs):
        
        super().__init__(master, **kwargs)

        self.page_width = page_width
        self.page_height = page_height
        self.separation = page_separation_height
        self.pdf_images = []
        self.labels = []
        self.file = file

        self.percentage_view = 0
        self.percentage_load = ctk.StringVar()
        
        self.loading_message = ctk.CTkLabel(self, textvariable=self.percentage_load, justify="center")
        self.loading_message.pack(pady=10)

        self.loading_bar = ctk.CTkProgressBar(self, width=100)
        self.loading_bar.set(0)
        self.loading_bar.pack(side="top", fill="x", padx=10)

        self.after(250, self.start_process)
        
        self.pack(expand = True, fill = "both", padx = 10, pady = 10)

    def start_process(self):
        Thread(target=self.add_pages).start()
        
    def add_pages(self):
        """ add images and labels """
        self.percentage_bar = 0
        open_pdf = fitz.open(self.file)
        
        for page in open_pdf:
            page_data = page.get_pixmap()
            pix = fitz.Pixmap(page_data, 0) if page_data.alpha else page_data
            img = Image.open(io.BytesIO(pix.tobytes('ppm')))
            label_img = ctk.CTkImage(img, size=(self.page_width, self.page_height))
            self.pdf_images.append(label_img)
                
            self.percentage_bar = self.percentage_bar + 1
            percentage_view = (float(self.percentage_bar) / float(len(open_pdf)) * float(100))
            self.loading_bar.set(percentage_view)
            self.percentage_load.set(f"Loading {os.path.basename(self.file)} \n{int(math.floor(percentage_view))}%")
            
        self.loading_bar.pack_forget()
        self.loading_message.pack_forget()
        open_pdf.close()
        
        for i in self.pdf_images:
            label = ctk.CTkLabel(self, image=i, text="")
            label.pack(pady=(0, self.separation))
            self.labels.append(label)
        
    def configure(self, **kwargs):
        """ configurable options """
        
        if "file" in kwargs:
            self.file = kwargs.pop("file")
            self.pdf_images = []
            for i in self.labels:
                i.destroy()
            self.labels = []
            self.after(250, self.start_pack)
            
        if "page_width" in kwargs:
            self.page_width = kwargs.pop("page_width")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
                
        if "page_height" in kwargs:
            self.page_height = kwargs.pop("page_height")
            for i in self.pdf_images:
                i.configure(size=(self.page_width, self.page_height))
            
        if "page_separation_height" in kwargs:
            self.separation = kwargs.pop("page_separation_height")
            for i in self.labels:
                i.pack_forget()
                i.pack(pady=(0,self.separation))
        
        super().configure(**kwargs)


class PanelPDFViewer(ctk.CTkFrame):
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
        
        self.label = ctk.CTkLabel(self, text = f"{self.text}", font = ctk.CTkFont("Helvetica", 20, "bold"), anchor = "w")
        self.label.place(relx = 0.05, rely = 0.035, relwidth = 0.3, relheight = 0.04)

        self.frame = ctk.CTkFrame(self)
        self.frame.place(relx = 0.02, rely = 0.1, relwidth = 0.96, relheight = 0.8)
       
        self.pdf = CTkPDFViewer(self.frame, file = "my_file.pdf")

        self.printer = ctk.CTkButton(self, text = "Imprimir")
        self.printer.place(relx = 0.7, rely = 0.035, relwidth = 0.2, relheight = 0.04)

        self.atras_button = ctk.CTkButton(self, text = "Atrás", command = self.animate)
        self.atras_button.place(relx = 0.4, rely = 0.93, relwidth = 0.2, relheight = 0.04)

        # layout 
        self.place(relx = self.start_pos, rely = 0.05, relwidth = 0.5, relheight = 0.9)

    def animate(self):
        if self.in_start_pos:
            self.tkraise()
            self.animate_fordward()
        else:
            self.tkraise()
            self.animate_backwards()

    def animate_fordward(self):
        if self.pos > self.end_pos:
            self.pos -= 0.27 
            self.place(relx = self.pos, rely = 0.05, relwidth = 0.5, relheight = 0.9)
            self.after(10, self.animate_fordward)
        else:
            self.in_start_pos = False 

    def animate_backwards(self):
         if self.pos < self.start_pos:
            self.pos += 0.27 
            self.place(relx = self.pos, rely = 0.05, relwidth = 0.5, relheight = 0.9)
            self.after(10, self.animate_backwards)
         else:
            self.in_start_pos = True




#root = customtkinter.CTk()
#root.geometry("700x600")
#pdf_frame = CTkPDFViewer(root, file="my_file.pdf")
#pdf_frame.pack(fill="both", expand=True, padx=10, pady=10)
#root.mainloop()