Parser OCR Tabela DE-PARA Barueri
Descrição

Script em Python para extrair a coluna "Novo Código" de uma tabela DE-PARA em PDF da Prefeitura de Barueri.
Utiliza pdfplumber para extração direta, com fallback OCR (pdf2image + pytesseract) se o PDF não tiver texto incorporado.

Gera um XML formatado contendo todos os códigos extraídos com suas linhas originais para referência.
Pré-requisitos

    Python 3.8+

    Bibliotecas Python:

        pdfplumber

        pdf2image

        pytesseract

        pillow

    Ferramentas externas instaladas:

        Poppler (para pdf2image)

        Tesseract OCR (para pytesseract)

Instalação

bash
pip install pdfplumber pdf2image pytesseract pillow
# Instale Poppler e Tesseract no sistema operacional

Uso

    Coloque o arquivo PDF ANEXO_III_Lista_DE-PARA.pdf na pasta do script.

    Configure variáveis de ambiente POPPLER_PATH e TESSERACT_CMD se necessário.

    Execute:

bash
python ocr.py

    O script gera o arquivo BARUERI_NOVO_CODIGO_FORMATADO.xml com a lista de "Novo Código".

Saída esperada

    XML formatado com elemento raiz <lista_de_para_barueri>

    Meta informação (nome do PDF, total de códigos, uso de OCR)

    Lista de <item> com <codigo> e <linha_original>

Exemplo de uso

xml
<lista_de_para_barueri>
  <meta>
    <pdf>ANEXO_III_Lista_DE-PARA.pdf</pdf>
    <total_codigos>906</total_codigos>
    <used_ocr>false</used_ocr>
  </meta>
  <novo_codigos>
    <item>
      <codigo>01.01.01.110</codigo>
      <linha_original>010101115 ANALISTA DE SISTEMAS 01.01.01.110 Anlise...</linha_original>
    </item>
    ...
  </novo_codigos>
</lista_de_para_barueri>

Contato

Desenvolvido por Leonardo Assis - uso interno para integração fiscal municipal.
