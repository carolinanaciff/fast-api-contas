from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_listar_contas():
    response = client.get('/contas-a-pagar-e-receber/listar-contas')

    assert response.status_code == 200, f'erro no teste. status {response.status_code}'

    assert response.json() == [
        {'id': 1, 'descricao': 'Aluguel', 'valor': 1000.5, 'tipo': 'a pagar'}, 
        {'id': 2, 'descricao': 'Salario', 'valor': 5000.0, 'tipo': 'receber'}
    ]
 

def test_criar_conta():
    nova_conta = {
        'descricao': 'Curso de Python', 
        'valor': 333.90, 
        'tipo': 'pagar'
    }

    nova_conta_copy = nova_conta.copy()
    nova_conta_copy['id'] = 3

    response = client.post('/contas-a-pagar-e-receber/criar-conta', json=nova_conta)

    assert response.status_code == 201
    assert response.json() == nova_conta_copy