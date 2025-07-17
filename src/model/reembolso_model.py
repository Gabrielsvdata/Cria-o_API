from src.model import db
from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, func, ForeignKey

class Reembolso(db.Model):
    __tablename__ = 'reembolso'

    num_prestacao   = Column(Integer, primary_key=True, autoincrement=True)
    colaborador     = Column(String(150), nullable=False)
    empresa         = Column(String(50), nullable=False)
    descricao       = Column(String(255))
    data            = Column(TIMESTAMP, server_default=func.current_timestamp(), nullable=False)
    tipo_reembolso  = Column(String(35), nullable=False)
    centro_custo    = Column(String(50), nullable=False)
    ordem_interna   = Column(String(50))
    divisao         = Column(String(50))
    pep             = Column(String(50))
    moeda           = Column(String(20), nullable=False, default='BRL')
    distancia_km    = Column(String(50))
    valor_km        = Column(String(50))
    valor_faturado  = Column(DECIMAL(10, 2), nullable=False)
    despesa         = Column(DECIMAL(10, 2))
    id_colaborador  = Column(Integer, ForeignKey('colaborador.id'))
    status          = Column(String(25), default='Em análise')

    # ✅ Relacionamento com comprovante
    comprovante_id = Column(Integer, ForeignKey('comprovantes.id'))

    def __init__(self,
                 colaborador,
                 empresa,
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
                 status='Em análise',
                 comprovante_id=None):
        self.colaborador     = colaborador
        self.empresa         = empresa
        self.descricao       = descricao
        self.tipo_reembolso  = tipo_reembolso
        self.centro_custo    = centro_custo
        self.ordem_interna   = ordem_interna
        self.divisao         = divisao
        self.pep             = pep
        self.moeda           = moeda
        self.distancia_km    = distancia_km
        self.valor_km        = valor_km
        self.valor_faturado  = valor_faturado
        self.despesa         = despesa
        self.id_colaborador  = id_colaborador
        self.status          = status
        self.comprovante_id  = comprovante_id  # ✅ Atribuição do comprovante

    def to_dict(self):
        return {
            "num_prestacao":   self.num_prestacao,
            "colaborador":     self.colaborador,
            "empresa":         self.empresa,
            "descricao":       self.descricao,
            "data":            str(self.data),
            "tipo_reembolso":  self.tipo_reembolso,
            "centro_custo":    self.centro_custo,
            "ordem_interna":   self.ordem_interna,
            "divisao":         self.divisao,
            "pep":             self.pep,
            "moeda":           self.moeda,
            "distancia_km":    self.distancia_km,
            "valor_km":        self.valor_km,
            "valor_faturado":  float(self.valor_faturado),
            "despesa":         float(self.despesa) if self.despesa is not None else None,
            "id_colaborador":  self.id_colaborador,
            "status":          self.status,
            "comprovante_id":  self.comprovante_id  # ✅ Retorno para o front
        }
