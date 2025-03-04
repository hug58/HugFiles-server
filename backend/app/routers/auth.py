
from flask import Blueprint, current_app

from urllib.parse import urljoin
from flask import  request, send_from_directory, jsonify
from app.utils.files_read import get_files
from app.utils import services


#models
from app.models.account import Accounts


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

@app_auth.route('/account', methods=['POST'])
def account():
    data = request.json
    if not data or 'username' not in data:
        return jsonify({"error": "Username and global_hash are required"}), 400
    
    user = Accounts.find_by_username(data['username']) 
    if user:
        print(f"Account created: {user.to_dict}")
        return user.to_dict()

    code, path = services.workspace(data['username'])
    account = Accounts(username=data['username'],code=code)
    account.save()
    
    return jsonify({"_id": str(account._id), 'code': code, 'path': path}), 201

