from src.model import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey

class Comprovante(db.Model):
    __tablename__ = "comprovantes"

    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String(120), nullable=False)
    texto_extraido = Column(Text, nullable=False)
    data_criacao = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamento com reembolso
    reembolso_id = Column(Integer, ForeignKey('reembolso.num_prestacao'), nullable=False)

    def __init__(self, nome_arquivo, texto_extraido, reembolso_id):
        self.nome_arquivo = nome_arquivo
        self.texto_extraido = texto_extraido
        self.reembolso_id = reembolso_id

    def to_dict(self):
        return {
            "id": self.id,
            "nome_arquivo": self.nome_arquivo,
            "texto_extraido": self.texto_extraido,
            "data_criacao": self.data_criacao.strftime("%Y-%m-%d %H:%M:%S"),
            "reembolso_id": self.reembolso_id
        }
