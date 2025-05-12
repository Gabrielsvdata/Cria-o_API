from flasgger import swag_from
from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso  # seu model já atualizado

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolsos')

# Listar todos
@bp_reembolso.route('/', methods=['GET'])
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def listar_reembolsos():
    try:
        reembolsos = Reembolso.query.all()
        return jsonify([r.to_dict() for r in reembolsos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@bp_reembolso.route('/<int:num_prestacao>', methods=['GET'])
def buscar_reembolso(num_prestacao):
    reembolso = Reembolso.query.get(num_prestacao)
    if not reembolso:
        return jsonify({'erro': 'Reembolso não encontrado.'}), 404
    return jsonify(reembolso.to_dict()), 200

# Criar novo (não enviamos num_prestacao, o SQLAlchemy gera pra gente)
@bp_reembolso.route('/new', methods=['POST'])
@swag_from('../docs/reembolso/cadastrar_reembolso.yml')
def criar_reembolso():
    try:
        d = request.get_json()
        novo = Reembolso(
        colaborador    = d['colaborador'],
        empresa        = d['empresa'],
        descricao      = d.get('descricao',''),
        tipo_reembolso = d['tipo_reembolso'],
        centro_custo   = d['centro_custo'],
        ordem_interna  = d.get('ordem_interna'),
        divisao        = d.get('divisao'),
        pep            = d.get('pep'),
        moeda          = d['moeda'],
        distancia_km   = d.get('distancia_km'),
        valor_km       = d.get('valor_km'),
        valor_faturado = d['valor_faturado'],
        despesa        = d.get('despesa',0),
        id_colaborador = d['id_colaborador']
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso criado com sucesso!', 'reembolso': novo.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

# Aprovar pelo num_prestacao (PK)
@bp_reembolso.route('/<int:num_prestacao>/aprovar', methods=['PATCH'])
def aprovar_reembolso(num_prestacao):
    try:
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Reembolso não encontrado.'}), 404
        r.status = 'Aprovado'
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso aprovado com sucesso!', 'reembolso': r.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

# Rejeitar pelo num_prestacao
@bp_reembolso.route('/<int:num_prestacao>/rejeitar', methods=['PATCH'])
def rejeitar_reembolso(num_prestacao):
    try:
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Reembolso não encontrado.'}), 404
        r.status = 'Rejeitado'
        db.session.commit()
        return jsonify({'mensagem': 'Seu pedido de reembolso foi rejeitado.', 'reembolso': r.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500
