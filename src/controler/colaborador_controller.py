
from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from
# request -> captura os dados na requisição.Pega o conteudo da requisição
# jsonify -> Trabalha com as respostas e converte em json


bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/todos-colaboradores')
def pegar_dados_todos_colaboradores():
    # busca todos os Colaborador e transforma em dict
    colaboradores = db.session.execute(
        db.select(Colaborador)
    ).scalars().all()
    resultado = [col.to_dict() for col in colaboradores]
    return jsonify(resultado), 200

@bp_colaborador.route('/cadastrar', methods=['OPTIONS', 'POST'])
@swag_from('../docs/colaborador/cadastrar_controller.yml')
def cadastrar_novo_colaborador():
    if request.method == 'OPTIONS':
        return '', 200
    dados = request.get_json()
    novo = Colaborador(
        nome   = dados['nome'],
        email  = dados['email'],
        senha  = hash_senha(dados['senha']),
        cargo  = dados.get('cargo'),
        salario= dados.get('salario')
    )
    db.session.add(novo)
    db.session.commit()
    return jsonify({'mensagem': 'Dado cadastrado com sucesso'}), 201

@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['PUT'])
def atualizar_dados_do_colaborador(id_colaborador):
    dados = request.get_json()
    colaborador = db.session.get(Colaborador, id_colaborador)
    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    # atualiza apenas os campos que vierem no JSON
    for campo in ('nome', 'cargo', 'email', 'salario'):
        if campo in dados:
            setattr(colaborador, campo, dados[campo])

    db.session.commit()
    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200

@bp_colaborador.route('/login', methods=['OPTIONS', 'POST'])
def login():
    if request.method == 'OPTIONS':
        return '', 200
    dados = request.get_json()
    email = dados.get('email')
    senha  = dados.get('senha')

    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400

    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar_one_or_none()

    if not colaborador or not checar_senha(senha, colaborador.senha):
        return jsonify({'mensagem': 'Usuário ou senha incorretos'}), 401

    return jsonify({
        'mensagem': 'Login realizado com sucesso',
        'usuario':  colaborador.to_dict()
    }), 200