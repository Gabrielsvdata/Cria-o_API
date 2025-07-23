from flask import Blueprint, request, jsonify
from src.utils.ocr_reader import extrair_texto_imagem
from src.model.comprovante_model import Comprovante
from src.model import db
import os, uuid

# Blueprint com prefixo padrão
ocr_bp = Blueprint("ocr_bp", __name__, url_prefix='/ocr')


# -------------------------------
# CREATE - Upload e extração OCR
# -------------------------------
@ocr_bp.route("/", methods=["POST"])
def ocr():
    if "file" not in request.files:
        return jsonify({"erro": "Arquivo não encontrado"}), 400

    file = request.files["file"]
    if file.filename.strip() == "":
        return jsonify({"erro": "Nome do arquivo vazio"}), 400

    os.makedirs("temp", exist_ok=True)
    extensao = os.path.splitext(file.filename)[1]
    nome_arquivo = f"{uuid.uuid4().hex}{extensao}"
    caminho_temporario = os.path.join("temp", nome_arquivo)

    try:
        # Salva o arquivo temporariamente
        file.save(caminho_temporario)

        # Extrai texto da imagem
        texto = extrair_texto_imagem(caminho_temporario)

        # Salva no banco de dados
        comprovante = Comprovante(nome_arquivo=nome_arquivo, texto_extraido=texto)
        db.session.add(comprovante)
        db.session.commit()

        return jsonify({
            "mensagem": "Texto extraído e salvo com sucesso.",
            "id_comprovante": comprovante.id,
            "nome_arquivo": nome_arquivo,
            "texto_extraido": texto
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": f"Erro ao processar imagem: {str(e)}"}), 500

    finally:
        if os.path.exists(caminho_temporario):
            os.remove(caminho_temporario)


# -------------------------------
# READ - Listar comprovantes
# -------------------------------
@ocr_bp.route("/", methods=["GET"])
def listar_ocr():
    comprovantes = Comprovante.query.order_by(Comprovante.data_criacao.desc()).all()
    resultados = [
        {
            "id": c.id,
            "nome_arquivo": c.nome_arquivo,
            "texto_extraido": c.texto_extraido,
            "data_criacao": c.data_criacao.isoformat()
        }
        for c in comprovantes
    ]
    return jsonify(resultados), 200


# -------------------------------
# READ - Obter um comprovante
# -------------------------------
@ocr_bp.route("/<int:id>", methods=["GET"])
def obter_ocr(id):
    comprovante = Comprovante.query.get(id)
    if not comprovante:
        return jsonify({"erro": "Comprovante não encontrado"}), 404

    return jsonify({
        "id": comprovante.id,
        "nome_arquivo": comprovante.nome_arquivo,
        "texto_extraido": comprovante.texto_extraido,
        "data_criacao": comprovante.data_criacao.isoformat()
    }), 200
