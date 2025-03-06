
from flask import Blueprint, current_app
import pathlib
import json
import os

from urllib.parse import urljoin
from flask import  request, send_from_directory, jsonify

from app.utils.files_read import get_files
from app.utils import services

delta_app = Blueprint('delta', __name__)
DATA_DIR = current_app.config['UPLOAD_FOLDER']


@delta_app.route('/signature', methods=['GET'])
def get_signature():
    filename = request.args.get('filename')
    code = request.args.get('code')
    filepath = os.path.join(DATA_DIR, code, filename)

    if not os.path.exists(filepath):
        return jsonify({'msg': 'no such file'})

    with open(filepath, 'rb') as f:
        file_data = f.read()

    signature = rdiff.signature(file_data)
    return signature


@delta_app.route('/apply', methods=['POST'])
def apply_delta():
    code = request.args.get('code')
    filename = request.args.get('filename')
    

    filepath = os.path.join(DATA_DIR, code, filename)

    if not os.path.exists(filepath) and os.path.isfile(filepath):
        return jsonify({'msg': 'File does not exist'}), 404

    delta = request.data
    with open(filepath, "rb") as f:
        base_data = f.read()

    # Aplicar el delta para reconstruir el archivo nuevo
    new_data = rdiff.patch(base_data, delta)

    # Guardar el archivo actualizado
    with open(filepath, "wb") as f:
        f.write(new_data)

    return jsonify({'msg':'file modified successfully'})