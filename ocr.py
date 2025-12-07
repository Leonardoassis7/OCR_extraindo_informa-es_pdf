import os
import re
import pdfplumber
import xml.etree.ElementTree as ET
from pdf2image import convert_from_path
import pytesseract
from PIL import Image
from xml.dom import minidom  

pdf_path = "ANEXO_III_Lista_DE-PARA.pdf"

def pretty_xml(root):
    """ Formata XML com indentação """
    rough_string = ET.tostring(root, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    pretty_xml = reparsed.toprettyxml(indent="  ")
   
    lines = pretty_xml.split('\n')
    clean_lines = [line for line in lines if line.strip()]
    return '\n'.join(clean_lines)

def extract_text_pages_with_pdfplumber(pdf_path):
    pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
    except Exception:
        return []
    return pages

def ocr_pdf_to_pages(pdf_path, dpi=300):
    poppler_path = os.environ.get("POPPLER_PATH")
    tesseract_cmd = os.environ.get("TESSERACT_CMD")
    if tesseract_cmd:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    images = convert_from_path(pdf_path, dpi=dpi, poppler_path=poppler_path)
    return [pytesseract.image_to_string(img, lang='por') for img in images]

def extract_todos_novo_codigo(full_text):
    linhas = full_text.split('\n')
    novo_codigos = []
    
    print(" Analisando todas as linhas da tabela DE-PARA ")
    
    for i, linha in enumerate(linhas):
        linha_limpa = linha.strip()
        if not linha_limpa:
            continue
        
        match = re.match(r'^\d{9}\s+.+?\s+([0-9]{2}\.[0-9]{2}\.[0-9]{2}\.[0-9]{3})', linha_limpa)
        if match:
            novo_codigo = match.group(1)
            novo_codigos.append({
                "novo_codigo": novo_codigo,
                "linha_completa": linha_limpa[:100] + "..." if len(linha_limpa) > 100 else linha_limpa
            })
            if len(novo_codigos) <= 5: 
                print(f"[{len(novo_codigos)}] {novo_codigo}")
    
    print(f"\n Total de 'Novo Código' extraídos: {len(novo_codigos)}")
    return novo_codigos

def main(pdf_path):
    page_texts = extract_text_pages_with_pdfplumber(pdf_path)
    used_ocr = False
    if not page_texts or not any(p.strip() for p in page_texts):
        print(" Usando OCR...")
        page_texts = ocr_pdf_to_pages(pdf_path)
        used_ocr = True
    
    full_text = "\n".join(page_texts)
    novo_codigos = extract_todos_novo_codigo(full_text)
    
    root = ET.Element("lista_de_para_barueri")
    meta = ET.SubElement(root, "meta")
    ET.SubElement(meta, "pdf").text = os.path.basename(pdf_path)
    ET.SubElement(meta, "total_codigos").text = str(len(novo_codigos))
    ET.SubElement(meta, "used_ocr").text = str(used_ocr).lower()
    
    lista = ET.SubElement(root, "novo_codigos")
    for item in novo_codigos:
        codigo = ET.SubElement(lista, "item")
        ET.SubElement(codigo, "codigo").text = item["novo_codigo"]
        ET.SubElement(codigo, "linha_original").text = item["linha_completa"]
    
    out_name = "BARUERI_NOVO_CODIGO_FORMATADO.xml"
    xml_formatado = pretty_xml(root)
    
    with open(out_name, 'w', encoding='utf-8') as f:
        f.write(xml_formatado)
    
    print(f"\  SALVO FORMATADO: {out_name}")
    print("\ Preview (primeiros 500 chars):")
    print(xml_formatado[:500] + "...")

if __name__ == "__main__":
    if not os.path.exists(pdf_path):
        print(f" PDF não encontrado: {pdf_path}")
    else:
        main(pdf_path)
