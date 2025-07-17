import pytesseract
from PIL import Image
import os

# Caminho para o executável do Tesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Arquivos de Programas\Tesseract-OCR\tesseract.exe'

# Define a variável de ambiente para a pasta tessdata
os.environ['TESSDATA_PREFIX'] = r'C:\\Tesseract-OCR'

# Abre a imagem
img = Image.open("comprovante.jpg")

# Extrai o texto com idioma inglês
texto = pytesseract.image_to_string(img, lang='por')

# Exibe o resultado
print("Texto extraído:")
print("-" * 40)
print(texto)
