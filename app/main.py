from fastapi import FastAPI
from app.routers import contas_a_pagar_receber_router
#from app.shared.database import engine, Base
#from app.models.contas_a_pagar_receber_model import ContaPagarReceberModel

#Base.metadata.drop_all(bind=engine)
#Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get('/')
def hello_world():
    return 'Hello from FasAPI'

app.include_router(contas_a_pagar_receber_router.router)

