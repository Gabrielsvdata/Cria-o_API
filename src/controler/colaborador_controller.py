from flask import Blueprint, request, jsonify, current_app
from src.model.colaborador_model import Colaborador
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

from flask import Blueprint, request, jsonify
from src.model.colaborador_model import Colaborador
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
def cadastrar_novo_colaborador():
    if request.method == 'OPTIONS':
        return '', 200 # Idealmente, use Flask-CORS para lidar com OPTIONS

    dados = request.get_json()
    if not dados:
        return jsonify({'mensagem': 'Payload da requisição está vazio ou não é JSON válido.'}), 400

    nome = dados.get('nome')
    email = dados.get('email')
    senha = dados.get('senha')
    # cargo e salario são opcionais pelo uso de .get() na criação do objeto Colaborador

    if not nome or not email or not senha:
        return jsonify({'mensagem': 'Nome, email e senha são obrigatórios.'}), 400

    try:
        novo = Colaborador(
            nome=nome,
            email=email,
            senha=hash_senha(senha), # função de hash
            cargo=dados.get('cargo'),
            salario=dados.get('salario')
        )
        db.session.add(novo)
        db.session.commit()
        
        # Retorno atual (só mensagem):
        return jsonify({'mensagem': 'Colaborador cadastrado com sucesso'}), 201

    except Exception as e:
        db.session.rollback() # Desfaz a transação em caso de erro
        current_app.logger.error(f"Erro ao cadastrar colaborador: {str(e)}", exc_info=True) # Loga o erro
        return jsonify({'mensagem': 'Erro interno ao cadastrar. Tente novamente mais tarde.'}), 500

@bp_colaborador.route('/atualizar/<int:id_colaborador>', methods=['OPTIONS', 'PUT'])
@swag_from('../docs/colaborador/atualizar_controller.yml')
def atualizar_dados_do_colaborador(id_colaborador):
    # Se for uma requisição OPTIONS (CORS preflight), só retorno OK.
    if request.method == 'OPTIONS':
        return '', 200
    
    dados = request.get_json()
    if not dados:
        # Se não vieram dados no corpo do JSON, é um erro.
        return jsonify({'mensagem': 'Payload da requisição está vazio ou não é JSON válido.'}), 400

    # Busco o colaborador pelo ID (crachá) que veio na URL.
    colaborador = db.session.get(Colaborador, id_colaborador)
    if not colaborador:
        # Se não encontrei, aviso que o colaborador não existe.
        return jsonify({'mensagem': 'Colaborador não encontrado (crachá inválido).'}), 404

    # Verificação Adicional para o fluxo de "Alterar Senha":
    # Se 'email' E 'senha' estão presentes nos dados recebidos,
    # entendo que é uma tentativa de alterar a senha com verificação.
    email_para_verificacao = dados.get('email')
    nova_senha = dados.get('senha')

    if email_para_verificacao and nova_senha: # Entra aqui se for o fluxo de alterar senha
        if email_para_verificacao.lower() != colaborador.email.lower(): # Comparo os emails (ignorando maiúsculas/minúsculas)
            # Se o email fornecido no corpo não bate com o email do colaborador (do crachá)...
            current_app.logger.warning(
                f"Tentativa de alteração de senha falhou para id {id_colaborador}: "
                f"Email fornecido '{email_para_verificacao}' não corresponde ao email do BD '{colaborador.email}'."
            )
            return jsonify({'mensagem': 'O email fornecido não corresponde ao crachá informado.'}), 400 # Ou 403 Forbidden
        
        # Se o email bateu, prossigo para atualizar a senha.
        # A senha será hasheada pela lógica abaixo no loop.
        # Os outros campos (nome, cargo, etc.) não serão alterados A MENOS que também sejam enviados
        # no JSON 'dados' pelo frontend, o que não é o caso para este fluxo específico de alterar senha.
        # Se APENAS email e senha forem enviados, APENAS a senha será atualizada (após o email ser verificado).
    
    # Lógica original de atualização (permite atualizar outros campos também, se enviados)
    # Para o nosso fluxo de alterar senha, 'dados' conterá principalmente 'email' e 'senha'.
    try:
        campos_permitidos_para_atualizacao = {}
        if email_para_verificacao and nova_senha:
            # No fluxo de alterar senha, só quero realmente atualizar a senha.
            # O 'email' foi apenas para verificação.
            campos_permitidos_para_atualizacao['senha'] = nova_senha
        else:
            # Se não for o fluxo de alterar senha, permite atualizar outros campos normalmente.
            # Isso mantém a funcionalidade original de atualização de perfil, se você a usar em outro lugar.
            for campo_chave in ('nome', 'email', 'cargo', 'salario', 'senha'):
                if campo_chave in dados:
                    campos_permitidos_para_atualizacao[campo_chave] = dados[campo_chave]
        
        if not campos_permitidos_para_atualizacao:
            return jsonify({'mensagem': 'Nenhum dado válido fornecido para atualização.'}), 400

        for campo, valor in campos_permitidos_para_atualizacao.items():
            if campo == 'senha':
                # Se o campo é 'senha', uso minha função hash_senha.
                setattr(colaborador, campo, hash_senha(valor))
                current_app.logger.info(f"Senha atualizada para o colaborador id {id_colaborador}.")
            elif campo == 'email' and (email_para_verificacao and nova_senha):
                # No fluxo específico de alteração de senha, não altero o email,
                # ele foi só para verificação. Se quisesse permitir, removeria esta condição.
                pass # Não atualiza o email neste fluxo específico.
            else:
                # Para outros campos, atualizo diretamente.
                setattr(colaborador, campo, valor)
        
        db.session.commit() # Salvo as alterações no banco.
        return jsonify({'mensagem': 'Dados do colaborador atualizados com sucesso!'}), 200 # Mensagem genérica de sucesso.
                                                                                        # Para o caso de senha: "Senha alterada com sucesso!"

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"Erro ao atualizar dados do colaborador id {id_colaborador}: {str(e)}", exc_info=True)
        return jsonify({'mensagem': 'Erro interno ao atualizar dados.'}), 500


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

@bp_colaborador.route('/login', methods=['POST'])
def login():
    
    dados_requisicao = request.get_json()
    
    email = dados_requisicao.get('email')
    senha = dados_requisicao.get('senha')
    
    if not email or not senha:
        return jsonify({'mensagem': 'Todos os dados precisam ser preenchidos'}), 400
    
    # Verifica se o colaborador existe
    colaborador = db.session.execute(
        db.select(Colaborador).where(Colaborador.email == email)
    ).scalar()

    # Se o colaborador não existir, retorna erro 404
    if not colaborador:
        return jsonify({'mensagem': 'Usuario não encontrado'}), 404
    
    # Converte o colaborador para dicionário
    # Isso é necessário para que o método to_dict funcione corretamente
    colaborador = colaborador.to_dict()

    # Verifica se o email e a senha estão corretos
    if email == colaborador.get('email') and checar_senha(senha, colaborador.get('senha')):
        # ALTERAÇÃO AQUI: Preparar e retornar os dados do usuário
      
        # contém as chaves 'id', 'nome' e 'cargo'.
        dados_do_usuario_para_retorno = {
            'id': colaborador.get('id'),
            'nome': colaborador.get('nome'),
            'cargo': colaborador.get('cargo')
        }
        return jsonify({
            'mensagem': 'Login realizado com sucesso', 
            'usuario': dados_do_usuario_para_retorno  # Adicionando os dados do usuário
        }), 200
    else:
        return jsonify({'mensagem': 'Credenciais invalidas'}), 400
    