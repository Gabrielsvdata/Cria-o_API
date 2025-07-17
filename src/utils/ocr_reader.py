import pytesseract
import os
from PIL import Image

# Caminho para o executável do Tesseract (versão em português do Windows)
pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'

# Caminho para a pasta tessdata
os.environ['TESSDATA_PREFIX'] = r'C:\Arquivos de Programas\Tesseract-OCR'

def extrair_texto_imagem(caminho_imagem):
    try:
        imagem = Image.open(caminho_imagem)
        texto = pytesseract.image_to_string(imagem, lang='por')
        return texto
    except Exception as e:
        return f"Erro ao processar OCR: {e}"
