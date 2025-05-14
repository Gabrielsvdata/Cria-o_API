
from src.model import db
from sqlalchemy.schema import Column
<<<<<<< HEAD
from sqlalchemy.types import Integer, String, DECIMAL, TIMESTAMP, DATETIME
=======
from sqlalchemy.types import Integer, String, DECIMAL, TIMESTAMP
>>>>>>> main
from sqlalchemy import func
from sqlalchemy import ForeignKey
class Reembolso(db.Model):
    __tablename__ = 'reembolso'

    # id = Column(Integer, primary_key=True, autoincrement=True)
    colaborador = Column(String(150), nullable=False)
    empresa = Column(String(50), nullable=False)
    num_prestacao = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(255))
<<<<<<< HEAD
    data = Column(DATETIME,  nullable=False)
=======
    data = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
>>>>>>> main
    tipo_reembolso = Column(String(35), nullable=False)
    centro_custo = Column(String(50), nullable=False)
    ordem_interna = Column(String(50))
    divisao = Column(String(50))
    pep = Column(String(50))
    moeda = Column(String(20), nullable=False)
    distancia_km = Column(String(50))
    valor_km = Column(String(50))
    valor_faturado = Column(DECIMAL(10, 2), nullable=False)
    despesa = Column(DECIMAL(10, 2))
    id_colaborador = Column(Integer, ForeignKey('colaborador.id'))
    status = Column(String(25), default='Em análise')
<<<<<<< HEAD
            # <— nova coluna

=======
>>>>>>> main

    def __init__(self,
                 colaborador,
                 empresa,
<<<<<<< HEAD
                 data,
=======
>>>>>>> main
                 descricao='',
                 tipo_reembolso=None,
                 centro_custo=None,
                 ordem_interna=None,
                 divisao=None,
                 pep=None,
                 moeda='BRL',
                 distancia_km=None,
                 valor_km=None,
                 valor_faturado=0,
                 despesa=0,
                 id_colaborador=None,
                 status='Em análise'):
        self.colaborador     = colaborador
        self.empresa         = empresa
<<<<<<< HEAD
        self.data            = data
=======
>>>>>>> main
        self.descricao       = descricao
        self.tipo_reembolso  = tipo_reembolso
        self.centro_custo    = centro_custo
        self.ordem_interna   = ordem_interna
        self.divisao         = divisao
        self.pep             = pep
        self.moeda           = moeda
<<<<<<< HEAD
        self.distancia_km     = distancia_km
=======
        self.distanca_km     = distancia_km
>>>>>>> main
        self.valor_km        = valor_km
        self.valor_faturado  = valor_faturado
        self.despesa         = despesa
        self.id_colaborador  = id_colaborador
        self.status          = status

 # ---------------------------- MÉTODO to_dict ----------------------------
    def to_dict(self):
        """
        Converte o objeto Reembolso em um dicionário JSON.
        """
        return {
            "num_prestacao": self.num_prestacao,
            "colaborador": self.colaborador,
            "empresa": self.empresa,
            "descricao": self.descricao,
            "data": str(self.data),  # Convertendo data para string
            "tipo_reembolso": self.tipo_reembolso,
            "centro_custo": self.centro_custo,
            "ordem_interna": self.ordem_interna,
            "divisao": self.divisao,
            "pep": self.pep,
            "moeda": self.moeda,
<<<<<<< HEAD
            "distancia_km": self.distancia_km,
=======
            "distanca_km": self.distanca_km,
>>>>>>> main
            "valor_km": self.valor_km,
            "valor_faturado": float(self.valor_faturado),  # Garantindo que seja float
            "despesa": float(self.despesa) if self.despesa else None,
            "id_colaborador": self.id_colaborador,
            "status": self.status
<<<<<<< HEAD
        }
=======
        }
>>>>>>> main
