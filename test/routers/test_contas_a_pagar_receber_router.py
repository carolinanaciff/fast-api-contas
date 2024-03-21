from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from app.main import app
from decouple import config
from sqlalchemy.orm import sessionmaker
from app.shared.database import Base
from app.shared.dependencies import get_db

client = TestClient(app)

SQLALCHEMY_DATABASE_URL = config('DB_TEST_URL')
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={}
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    except Exception as ex:
        raise Exception(ex)
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


def test_listar_contas():
    # Dropando bases anteriores e criando nova base de testes
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # criando registros antes de testar o get
    client.post('/contas-a-pagar-e-receber/criar-conta', 
        json={'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'})
    client.post('/contas-a-pagar-e-receber/criar-conta', 
        json={'descricao': 'Salario', 'valor': 5000.0, 'tipo': 'RECEBER'})

    response = client.get('/contas-a-pagar-e-receber/listar-contas')

    assert response.status_code == 200, f'erro no teste. status {response.status_code}'

    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'PAGAR'}, 
        {'id': 2, 'descricao': 'Salario', 'valor': 5000.0, 'tipo': 'RECEBER'}
    ]
 

def test_criar_conta():
    # Dropando bases anteriores e criando nova base de testes
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    nova_conta = {
        'descricao': 'Curso de Python', 
        'valor': 333.90, 
        'tipo': 'PAGAR'
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy['id'] = 1

    response = client.post('/contas-a-pagar-e-receber/criar-conta', json=nova_conta)

    assert response.status_code == 201
    assert response.json() == nova_conta_copy


def test_deve_retornar_erro_exceder_descricao():
    response = client.post('/contas-a-pagar-e-receber/criar-conta', json={
        'descricao': 'Taxa de Manutenção de Equipamentos de Tecnologia de Informação e Comunicação',
        'valor': 300,
        'tipo': 'PAGAR'
    })
    assert response.status_code == 422

def test_deve_retornar_erro_valor():
    response = client.post('/contas-a-pagar-e-receber/criar-conta', json={
        'descricao': 'Taxa de Manutenção',
        'valor': -1,
        'tipo': 'PAGAR'
    })
    assert response.status_code == 422

def test_deve_retornar_erro_pagar_receber():
    response = client.post('/contas-a-pagar-e-receber/criar-conta', json={
        'descricao': 'Taxa de Manutenção',
        'valor': 300,
        'tipo': 'A PAGAR'
    })
    assert response.status_code == 422