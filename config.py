# armazenar as configurações do ambiente de desenvlvimento
from os import environ # Arquivo tem acesso as variaveis de ambiente
from dotenv import load_dotenv #Carregamento das variaveis de ambiente nesse arquivo

load_dotenv(".env")

class Config():
        # TESTE 21/05/2020
        # SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_DEV") #puxa a variavel de ambiente e utiliza para a conexão
        # SQLALCHEMY =_TACK_MODIFICATIONS = False #Otimiza as quetis no banco de dados


        # ORIGINAL
        SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_PROD") #puxa a variavel de ambiente e utiliza para a conexão
        SQLALCHEMY =_TACK_MODIFICATIONS = False #Otimiza as quetis no banco de dados
