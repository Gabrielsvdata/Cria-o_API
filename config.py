# armazenar as configurações do ambiente de desenvlvimento
from os import environ # Arquivo tem acesso as variaveis de ambiente
from dotenv import load_dotenv #Carregamento das variaveis de ambiente nesse arquivo

load_dotenv(".env")

class Config():
        SQLALCHEMY_DATABASE_URI = environ.get("URL_DATABASE_PROD") #puxa a variavel de ambiente e utiliza para a conexão
        SQLALCHEMY =_TACK_MODIFICATIONS = False #Otimiza as quetis no banco de dados

        # +++ Configurações de e-mail +++
        MAIL_SERVER   = environ.get("MAIL_SERVER", "smtp.gmail.com")
        MAIL_PORT     = int(environ.get("MAIL_PORT", 587))
        MAIL_USE_TLS  = environ.get("MAIL_USE_TLS", "true").lower() in ("true","1")
        MAIL_USE_SSL  = environ.get("MAIL_USE_SSL", "false").lower() in ("true", "1")
        MAIL_USERNAME = environ.get("MAIL_USERNAME")       # ex: no-reply@meuapp.com
        MAIL_PASSWORD = environ.get("MAIL_PASSWORD")       # senha ou token do SMTP
        MAIL_DEFAULT_SENDER = environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)

        # Remetente padrão (de onde os e-mails vão sair)
        MAIL_DEFAULT_SENDER = environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)