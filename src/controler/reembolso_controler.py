from flasgger import swag_from
from flask import Blueprint, request, jsonify
from src.model import db
from src.model.reembolso_model import Reembolso
from src.model.comprovante_model import Comprovante
import os

bp_reembolso = Blueprint('reembolso', __name__, url_prefix='/reembolsos')

# Base para os arquivos YAML
DOCS_BASE = os.path.join(os.path.dirname(__file__), '..', '..', 'docs', 'reembolso')

@bp_reembolso.route('/', methods=['GET'])
@swag_from(os.path.join(DOCS_BASE, 'listar_reembolsos.yml'))
def listar_reembolsos():
    try:
        status = request.args.get('status')
        num_prestacao = request.args.get('num_prestacao', type=int)

        query = Reembolso.query
        if status:
            query = query.filter_by(status=status)
        if num_prestacao:
            query = query.filter_by(num_prestacao=num_prestacao)

        reembolsos = query.all()
        return jsonify([r.to_dict() for r in reembolsos]), 200
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@bp_reembolso.route('/<int:num_prestacao>', methods=['GET'])
def buscar_reembolso(num_prestacao):
    r = Reembolso.query.get(num_prestacao)
    if not r:
        return jsonify({'erro': 'Reembolso não encontrado.'}), 404
    return jsonify(r.to_dict()), 200

@bp_reembolso.route('/new', methods=['POST'])
@swag_from(os.path.join(DOCS_BASE, 'cadastrar_reembolso.yml'))
def criar_reembolso():
    try:
        d = request.get_json()
        comprovante_id = d.get('comprovante_id')
        if comprovante_id:
            comprovante = Comprovante.query.get(comprovante_id)
            if not comprovante:
                return jsonify({'erro': 'Comprovante não encontrado.'}), 400

        novo = Reembolso(
            colaborador=d['colaborador'],
            empresa=d['empresa'],
            descricao=d.get('descricao', ''),
            tipo_reembolso=d['tipo_reembolso'],
            centro_custo=d['centro_custo'],
            ordem_interna=d.get('ordem_interna'),
            divisao=d.get('divisao'),
            pep=d.get('pep'),
            moeda=d.get('moeda', 'BRL'),
            distancia_km=d.get('distancia_km'),
            valor_km=d.get('valor_km'),
            valor_faturado=d['valor_faturado'],
            despesa=d.get('despesa', 0),
            id_colaborador=d['id_colaborador'],
            comprovante_id=comprovante_id
        )
        db.session.add(novo)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso criado com sucesso!', 'reembolso': novo.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

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

@bp_reembolso.route('/<int:num_prestacao>/rejeitar', methods=['PATCH'])
def rejeitar_reembolso(num_prestacao):
    try:
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Reembolso não encontrado.'}), 404
        r.status = 'Rejeitado'
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso rejeitado com sucesso!', 'reembolso': r.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@bp_reembolso.route('/<int:num_prestacao>', methods=['PUT'])
@swag_from(os.path.join(DOCS_BASE, 'atualizar_reembolso.yml'))
def atualizar_reembolso(num_prestacao):
    try:
        dados = request.get_json()
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Reembolso não encontrado.'}), 404

        novo_comprovante_id = dados.get('comprovante_id')
        if novo_comprovante_id:
            comprovante = Comprovante.query.get(novo_comprovante_id)
            if not comprovante:
                return jsonify({'erro': 'Comprovante informado não existe.'}), 400
            r.comprovante_id = novo_comprovante_id

        for campo in (
            'colaborador', 'empresa', 'descricao', 'tipo_reembolso',
            'centro_custo', 'ordem_interna', 'divisao', 'pep',
            'moeda', 'distancia_km', 'valor_km', 'valor_faturado',
            'despesa', 'id_colaborador', 'status'
        ):
            if campo in dados:
                setattr(r, campo, dados[campo])

        db.session.commit()
        return jsonify({'mensagem': 'Reembolso atualizado com sucesso!', 'reembolso': r.to_dict()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 400

@bp_reembolso.route('/<int:num_prestacao>', methods=['DELETE'])
@swag_from(os.path.join(DOCS_BASE, 'remover_reembolso.yml'))
def remover_reembolso(num_prestacao):
    try:
        r = Reembolso.query.get(num_prestacao)
        if not r:
            return jsonify({'erro': 'Reembolso não encontrado.'}), 404
        db.session.delete(r)
        db.session.commit()
        return jsonify({'mensagem': 'Reembolso removido com sucesso!'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'erro': str(e)}), 500

@bp_reembolso.route('/<int:num_prestacao>/enviar-analise', methods=['PATCH'])
def enviar_para_analise(num_prestacao):
    r = Reembolso.query.get(num_prestacao)
    if not r:
        return jsonify({'erro': 'Reembolso não encontrado.'}), 404
    r.status = 'Em análise'
    db.session.commit()
    return jsonify({'mensagem': 'Enviado para análise!', 'reembolso': r.to_dict()}), 200
