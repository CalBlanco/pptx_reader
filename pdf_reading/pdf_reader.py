from pypdf import PdfReader
import os

def get_text_from_pdf(pdf_file:str):
    file_name = os.path.basename(pdf_file)

    reader = PdfReader(pdf_file)

    text_data = []
    for i, page in enumerate(reader.pages):
        text_data.append((file_name, i+1,  page.extract_text()))
    
    return text_data