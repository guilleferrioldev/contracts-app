import os
import sqlite3
from pylatex import Document, Section, Subsection, Command, TextBlock
from pylatex.utils import NoEscape
from pylatex.package import Package
import customtkinter as ctk

class ButtonPdf(ctk.CTkButton):
    def __init__(self, master):
        super().__init__(master = master)


def database():
    conn = sqlite3.connect(os.path.join("..", "contratos.db"))
    cursor = conn.cursor()

    instruccion = "SELECT * FROM Servicios"
    cursor.execute(instruccion)
    datos = cursor.fetchall()

    conn.commit()
    conn.close()

    print(datos)


def generate_PDF():
    latex_document = 'solicitud.tex'
    with open(latex_document) as file:
        tex = file.readlines()

    tex.remove(tex[31])
    tex.insert(30, r"\put(21,-62.96002){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}Transferencia Bancaria  Cuba  Nominativo  Si  Cheque Certificado Vamos}")

    doc = Document('temporal', font_size=None)

    doc.preamble.append(NoEscape("".join(tex)))

    doc.generate_tex()
    doc.generate_pdf(clean_tex=False)

def execute():
    generate_PDF()
    os.system("rm temporal.aux")
    os.system("rm temporal.log")
    os.system("rm temporal.tex")
    os.system("rm temporal.fls")
    os.system("rm temporal.fdb_latexmk")
    os.system("firefox temporal.pdf")

if __name__ == "__main__":
    database()
    execute()

