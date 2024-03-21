from enum import Enum
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List
from sqlalchemy.orm import Session
from app.models.contas_a_pagar_receber_model import ContaPagarReceberModel
from app.shared.dependencies import get_db

router = APIRouter(prefix='/contas-a-pagar-e-receber')


class ContasPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: float 
    tipo: str

    class Config:
        orm_mode = True

class ContaPagarReceberEnum(str, Enum):
    PAGAR = 'PAGAR'
    RECEBER = 'RECEBER'

class ContasPagarReceberRequest(BaseModel):
    descricao: str = Field(min_length=3, max_length=50)
    valor: float = Field(gt=0)
    tipo: ContaPagarReceberEnum # PAGAR OU RECEBER


@router.get('/listar-contas', response_model=List[ContasPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)) -> List[ContasPagarReceberResponse]:
    return db.query(ContaPagarReceberModel).order_by(ContaPagarReceberModel.id.asc()).all()


@router.get('/listar-conta/{id_conta}', response_model=ContasPagarReceberResponse)
def listar_conta(
        id_conta: int,
        db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    
    conta_result : ContaPagarReceberModel = db.query(ContaPagarReceberModel).get(id_conta)
    if conta_result.descricao == None:
        raise HTTPException(status_code=404, detail="Conta não encontrada")
    
    return conta_result


@router.post('/criar-conta', response_model=ContasPagarReceberResponse, status_code=201)
def criar_conta(conta_request: ContasPagarReceberRequest, 
                db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    
    #ENVIANDO OS PARAMETROS ESCREVENDO UM POR UM
    #contas_pagar_receber = ContaPagarReceberModel(
    #    descricao=conta_request.descricao, 
    #    valor=conta_request.valor,
    #    tipo=conta_request.tipo
    #    )

    #ENVIANDO ABREVIADO COM **.VARIAVEL.MODEL_DUMP
    contas_pagar_receber = ContaPagarReceberModel(
        **conta_request.model_dump()
    )
    db.add(contas_pagar_receber)
    db.commit()
    db.refresh(contas_pagar_receber)

    return contas_pagar_receber


@router.put('/atualiza-conta/{id_conta}', response_model=ContasPagarReceberResponse, status_code=200)
def atualizar_conta(
        id_conta: int,
        conta_atualizar_request: ContasPagarReceberRequest, 
        db: Session = Depends(get_db)) -> ContasPagarReceberResponse:
    
    conta_atualizar : ContaPagarReceberModel = db.query(ContaPagarReceberModel).get(id_conta)

    conta_atualizar.descricao = conta_atualizar_request.descricao
    conta_atualizar.valor = conta_atualizar_request.valor
    conta_atualizar.tipo = conta_atualizar_request.tipo

    db.add(conta_atualizar)
    db.commit()
    db.refresh(conta_atualizar)

    return conta_atualizar