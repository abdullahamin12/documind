from .base import Docparse
import fitz
class PyMuPDFParser(Docparse):
    def parse(self, path):
        doc=fitz.open(path)
        text=""
        for page in doc:
            text+=page.get_text()
            text+="\n"
        doc.close()
        return text 


