from flasgger import swag_from
from flask import Blueprint, request, jsonify, make_response
from src.model import db
from src.model.reembolso_model import Reembolso  # seu model já atualizado

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolsos')

# ——————————————————————————————————————————————————————————————
# 1) Listar (GET /reembolsos?status=...)
@bp_reembolso.route('/', methods=['GET'])
@swag_from('../docs/reembolso/listar_reembolsos.yml')
def listar_reembolsos():
    status = request.args.get('status')
    try:
        query = Reembolso.query
        if status:
            query = query.filter_by(status=status)
        reembolsos = query.all()
        return jsonify([r.to_dict() for r in reembolsos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500
# ——————————————————————————————————————————————————————————————
# 2) Criar novo (OPTIONS + POST /reembolsos/new)
@bp_reembolso.route('/new', methods=['OPTIONS', 'POST'])
@swag_from('../docs/reembolso/cadastrar_reembolso.yml')
def criar_reembolso():
    # responde ao preflight CORS
    if request.method == 'OPTIONS':
        return make_response('', 200)

    try:
        d = request.get_json()
        novo = Reembolso(
            colaborador    = d['colaborador'],
            empresa        = d['empresa'],
            data           = d['data'],
            descricao      = d.get('descricao', ''),
            tipo_reembolso = d['tipo_reembolso'],
            centro_custo   = d['centro_custo'],
            ordem_interna  = d.get('ordem_interna'),
            divisao        = d.get('divisao'),
            pep            = d.get('pep'),
            moeda          = d['moeda'],
            distancia_km   = d.get('distancia_km'),
            valor_km       = d.get('valor_km'),
            valor_faturado = d['valor_faturado'],
            despesa        = d.get('despesa', 0),
            id_colaborador = d['id_colaborador']
        )
        db.session.add(novo)
        db.session.commit()

        return jsonify({
            'mensagem': 'Reembolso criado com sucesso!',
            'reembolso': novo.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

# ——————————————————————————————————————————————————————————————
# 3) Buscar um (GET /reembolsos/<num_prestacao>)
@bp_reembolso.route('/<int:num_prestacao>', methods=['GET'])
def buscar_reembolso(num_prestacao):
    r = Reembolso.query.get(num_prestacao)
    if not r:
        return jsonify({'erro': 'Reembolso não encontrado.'}), 404
    return jsonify(r.to_dict()), 200

# ——————————————————————————————————————————————————————————————
# 4) Atualizar parcial (PATCH /reembolsos/<num_prestacao>)
@bp_reembolso.route('/<int:num_prestacao>', methods=['PATCH'])
def atualizar_reembolso(num_prestacao):
    r = Reembolso.query.get(num_prestacao)
    if not r:
        return jsonify({'erro': 'Reembolso não encontrado.'}), 404

    dados = request.get_json()
    # atualiza somente os campos enviados
    for campo in (
        'colaborador', 'empresa', 'data', 'descricao',
        'tipo_reembolso', 'centro_custo', 'ordem_interna',
        'divisao', 'pep', 'moeda',
        'distancia_km', 'valor_km', 'valor_faturado',
        'despesa', 'status'
    ):
        if campo in dados:
            setattr(r, campo, dados[campo])

    db.session.commit()
    return jsonify({
        'mensagem': 'Reembolso atualizado com sucesso!',
        'reembolso': r.to_dict()
    }), 200

# ——————————————————————————————————————————————————————————————
# 5) Deletar (DELETE /reembolsos/<num_prestacao>)
@bp_reembolso.route('/<int:num_prestacao>', methods=['OPTIONS', 'DELETE'])
def deletar_reembolso(num_prestacao):
    if request.method == 'OPTIONS':
        # responde ao preflight CORS
        return make_response('', 200)
    r = Reembolso.query.get(num_prestacao)
    if not r:
        return jsonify({'erro': 'Reembolso não encontrado.'}), 404

    db.session.delete(r)
    db.session.commit()
    return jsonify({'mensagem': 'Reembolso deletado com sucesso!'}), 200

# Aprovar
@bp_reembolso.route('/<int:num_prestacao>/aprovar', methods=['PATCH','OPTIONS'])
def aprovar_reembolso(num_prestacao):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    try:
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Não encontrado.'}), 404
        r.status = 'Aprovado'
        db.session.commit()
        return jsonify({'mensagem': 'Aprovado com sucesso!', 'reembolso': r.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500


# Rejeitar
@bp_reembolso.route('/<int:num_prestacao>/rejeitar', methods=['PATCH','OPTIONS'])
def rejeitar_reembolso(num_prestacao):
    if request.method == 'OPTIONS':
        return make_response('', 200)
    try:
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Não encontrado.'}), 404
        r.status = 'Rejeitado'
        db.session.commit()
        return jsonify({'mensagem': 'Rejeitado com sucesso!', 'reembolso': r.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500