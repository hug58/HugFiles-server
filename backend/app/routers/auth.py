
from flask import Blueprint, current_app

from urllib.parse import urljoin
from flask import  request, send_from_directory, jsonify
from app.utils.files_read import get_files
from app.utils import services


app_auth = Blueprint('auth', __name__)

@app_auth.route('/', methods=['POST'])
def token():
    """ Get path with token """
    data_token = request.json
    if not isinstance(data_token, dict):
        return jsonify({'msg': 'json invalid'})
    if not data_token['email']:
        return jsonify({'msg': 'email empty'})

    code, path = services.workspace(data_token['email'])
    return jsonify({'path': path, 'code': code})