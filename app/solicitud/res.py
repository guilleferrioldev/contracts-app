import os
from pylatex import Document, Section, Subsection, Command, TextBlock
from pylatex.utils import NoEscape
from pylatex.package import Package


latex_document = 'solicitud.tex'
with open(latex_document) as file:
    tex = file.readlines()

tex.remove(tex[31])
tex.insert(30, r"\put(21,-62.96002){\fontsize{14.04}{1}\usefont{T1}{cmr}{m}{n}\selectfont\color{color_29791}Transferencia Bancaria  Cuba  Nominativo  Si  Cheque Certificado Vamos}")

doc = Document('basic', font_size=None)

doc.preamble.append(NoEscape("".join(tex)))

doc.generate_tex()
doc.generate_pdf(clean_tex=False)

os.system("rm basic.aux")
os.system("rm basic.log")
os.system("rm basic.tex")
os.system("rm basic.fls")
os.system("rm basic.fdb_latexmk")
os.system("firefox basic.pdf")

