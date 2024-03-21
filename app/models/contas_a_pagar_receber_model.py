from sqlalchemy import Column, Integer, String, Float
from app.shared.database import Base


class ContaPagarReceberModel(Base):
    __tablename__ = 'contas_pagar_receber'

    id = Column(Integer, primary_key=True, autoincrement=True)
    descricao = Column(String(50))
    valor = Column(Float)
    tipo = Column(String(7))