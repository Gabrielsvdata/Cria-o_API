# src/routes/colaborador_routes.py

from flask import Blueprint, request, jsonify, make_response
from src.model.colaborador_model import Colaborador
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.model import db
from src.security.security import hash_senha, checar_senha
from flasgger import swag_from

bp_colaborador = Blueprint('colaborador', __name__, url_prefix='/colaborador')

@bp_colaborador.route('/todos-colaboradores', methods=['GET'])
@swag_from('../docs/colaborador/pegar_todos_colaboradores.yml')
def pegar_dados_todos_colaboradores():
    colaboradores = db.session.execute(db.select(Colaborador)).scalars().all()
    resultado = [col.all_data() for col in colaboradores]
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
    return jsonify({'mensagem': 'Colaborador cadastrado com sucesso'}), 201

@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['OPTIONS', 'PUT'])
@swag_from('../docs/colaborador/atualizar_controller.yml')
def atualizar_dados_do_colaborador(id_colaborador):
    if request.method == 'OPTIONS':
        return '', 200
    dados = request.get_json()
    colaborador = db.session.get(Colaborador, id_colaborador)
    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    # permite atualizar nome, email, cargo, salario e senha
    for campo in ('nome', 'email', 'cargo', 'salario', 'senha'):
        if campo in dados:
            if campo == 'senha':
                setattr(colaborador, campo, hash_senha(dados[campo]))
            else:
                setattr(colaborador, campo, dados[campo])

    db.session.commit()
    return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso'}), 200

@bp_colaborador.route('/remover/<int:id_colaborador>', methods=['OPTIONS', 'DELETE'])
@swag_from('../docs/colaborador/remover_controller.yml')
def remover_colaborador(id_colaborador):
    if request.method == 'OPTIONS':
        return '', 200
    colaborador = db.session.get(Colaborador, id_colaborador)
    if not colaborador:
        return jsonify({'mensagem': 'Colaborador não encontrado'}), 404

    db.session.delete(colaborador)
    db.session.commit()
    return jsonify({'mensagem': 'Colaborador removido com sucesso'}), 200

@bp_colaborador.route('/login', methods=['POST', 'OPTIONS'])
def login():
    # responde pré-voo CORS
    if request.method == 'OPTIONS':
        return '', 200

    try:
        dados = request.get_json() or {}
        email = dados.get('email')
        senha = dados.get('senha')
        if not email or not senha:
            return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400

        colaborador = db.session.execute(
            db.select(Colaborador).where(Colaborador.email == email)
        ).scalar()

        if not colaborador or not checar_senha(senha, colaborador.senha):
            return jsonify({'mensagem': 'Credenciais inválidas!'}), 401

        access_token = create_access_token(identity=colaborador.id)
        resp = make_response(jsonify(colaborador.to_public_dict()), 200)
        resp.set_cookie(
            'access_token', access_token,
            httponly=True,
            secure=True,    # em produção, só HTTPS
            samesite='Strict'
        )
        return resp

    except Exception as e:
        return jsonify({
            'mensagem': 'Erro ao realizar login',
            'erro': str(e)
        }), 500

#
@bp_colaborador.route('/me', methods=['GET'])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    colaborador = db.session.get(Colaborador, user_id)
    return jsonify(colaborador.to_public_dict()), 200

    
    # if request.method == 'OPTIONS':
    #     return '', 200
    
    # dados = request.get_json() 
    # try:
    #     email = dados.get('email')
    #     senha = dados.get('senha')
    #     if not email or not senha:
    #         return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400

    #     colaborador = db.session.execute(
    #         db.select(Colaborador).where(Colaborador.email == email)
    #     ).scalar()


    #     if email == colaborador.email and checar_senha(senha, colaborador.senha):
    #      return jsonify({'mensagem': 'Login realizado com sucesso!'}), 200
    #     else:
    #        return jsonify({'mensagem': 'Credenciais inválidas!'}), 400
        
    # except Exception as e:
    #     return jsonify({'mensagem': 'Erro ao realizar login', 'erro': str(e)}), 500


        # RASCUNHO DO CÓDIGO ANTIGO
        # if not colaborador or not checar_senha(senha, colaborador.senha):
        #     return jsonify({'mensagem': 'Usuário ou senha incorretos'}), 401

        # return jsonify({
        #     'mensagem': 'Login realizado com sucesso',
        #     'usuario':  colaborador.all_data()
        # }), 200
