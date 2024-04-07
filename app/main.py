from fastapi import FastAPI, Request
from app.routers import contas_a_pagar_receber_router
from app.shared.exception_handler import notfound_exception_handler
from app.shared.exceptions import NotFound

app = FastAPI()

@app.get('/')
def hello_world():
    return 'Hello from FasAPI'

app.include_router(contas_a_pagar_receber_router.router)
app.add_exception_handler(NotFound, notfound_exception_handler)