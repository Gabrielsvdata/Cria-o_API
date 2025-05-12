# src/controler/auth_controller.py

from flask import Blueprint, request, jsonify, url_for
from flask_mail import Message
from datetime import datetime
from src.extensions import mail, db
from src.model.password_reset_model import PasswordReset
from src.model.colaborador_model import Colaborador
from src.security.security import hash_senha

bp_auth = Blueprint('auth', __name__, url_prefix='/auth')


@bp_auth.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get('email')
    # Não vaza informação se o usuário existe ou não
    pr = PasswordReset.create(email)

    # Monta URL de reset
    reset_url = url_for('auth.reset_password_form', token=pr.token, _external=True)

    # Envia e-mail
    msg = Message(
        subject="Recuperação de Senha",
        recipients=[email],
    )
    msg.body = (
        f"Para redefinir sua senha, clique no link abaixo:\n\n"
        f"{reset_url}\n\n"
        "Se você não solicitou essa ação, pode ignorar este e-mail."
    )
    mail.send(msg)

    return jsonify({'mensagem': 'Se o e-mail existir, você receberá instruções.'}), 200


@bp_auth.route('/reset-password/<token>', methods=['GET'])
def reset_password_form(token):
    pr = PasswordReset.query.filter_by(token=token).first()
    if not pr or pr.expires_at < datetime.utcnow():
        return jsonify({'erro': 'Token inválido ou expirado.'}), 400

    return jsonify({'mensagem': 'Token válido, prossiga para redefinir a senha.'}), 200


@bp_auth.route('/reset-password', methods=['POST'])
def reset_password():
    data = request.get_json()
    token = data.get('token')
    new_pass = data.get('new_password')

    pr = PasswordReset.query.filter_by(token=token).first()
    if not pr or pr.expires_at < datetime.utcnow():
        return jsonify({'erro': 'Token inválido ou expirado.'}), 400

    user = Colaborador.query.filter_by(email=pr.email).first()
    if not user:
        return jsonify({'erro': 'Usuário não encontrado.'}), 404

    # Atualiza senha e remove o token
    user.senha = hash_senha(new_pass)
    db.session.delete(pr)
    db.session.commit()

    return jsonify({'mensagem': 'Senha redefinida com sucesso.'}), 200
