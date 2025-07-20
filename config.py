# config.py

from os import environ
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv(".env")

class Config():
    # Ambiente de desenvolvimento
    SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_DEV")  # Usa a URL do banco de dados do .env
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Desativa o rastreamento de modificações (melhor performance)

    # Ambiente de produção (comentado)
    # SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_PROD")
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
