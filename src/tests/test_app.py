#PARA QUE A BIBLIOTECA ENCONTRAR O ARQUIVO DE TESTE O NOME DESSE ARQUIVO TEM QUE COMEÇAR COM TESTE

import pytest # TRAZ A BIBLIOTECA DE TESTES 
import time #manipular o tempo 
from src.model.colaborador_model import Colaborador
from src.app import create_app

@pytest.fixture # IDENTIDICAR FUNÇÕES DE CONFIGURAÇÕES PARA O TESTE 
def app():
    app = create_app()
    yield app

@pytest.fixture
def client(app):
    return app.test_cliente(app)

def test_desempenho_requisicao_get(client):
    
    comeco = time.time()# PEGAR A HORA ATUAL E TRANSFORMAR EM SEGUNDOS 100

    for _ in range(100):
            resposta = client.get('colaborador/todos/colaboradores')

    fim = time.time() - comeco
    assert fim < 0.2

