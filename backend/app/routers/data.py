
from flask import Blueprint, current_app
import pathlib
import json
import os

from urllib.parse import urljoin
from flask import  request, send_from_directory, jsonify

from app.utils.files_read import get_files
from app.utils import services

app_data = Blueprint('data', __name__)


@app_data.route('/<path:filename>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def data(filename):
    """ Handle files. """
    path = pathlib.Path(filename)
    filename = urljoin(current_app.config['UPLOAD_FOLDER'], filename)


    if request.method == 'GET':
        if os.path.isfile(filename):
            path = pathlib.Path(filename)
            return send_from_directory(path.parent, path.name)
        elif os.path.isdir(filename):
            return jsonify(get_files(filename, path.name))
        
        return jsonify({"msg": "account does not exist"})
    
    elif request.method == 'POST':
        if not os.path.isdir(filename):
            os.makedirs(filename, exist_ok=True)

        if 'upload_file' not in request.files:
            return jsonify({'msg': 'directory created'})

        file = request.files['upload_file']
        full_path = os.path.join(filename, file.filename)
        file.save(full_path)


        return jsonify({'msg': 'save uploaded file' })
                        # , 'id': result.inserted_id})
         
    elif request.method == 'PUT':
        """
        TODO: ADD NOTIFICATIONS
        """
        if os.path.exists(path):
            if os.path.isfile(path):
                if request.json:
                    data_json = json.loads(request.get_json())
                    if data_json and 'name' in data_json:
                        new_file = str(path.parent).replace('\\', '/') + data_json['name']
                        os.rename(path, new_file)
                        return jsonify({'msg': 'save uploaded file'})
                else:
                    request.files['upload_file'].save(filename)
                    modified_at = round(os.path.getmtime(filename))
                    os.utime(filename, (modified_at, modified_at))
                    return jsonify({'msg': 'successfully updated file'})
            else:
                return jsonify({'msg': 'did not update uploaded file'})
        else:
            return {'File not found': filename}, 404
    
    elif request.method == 'DELETE':
        services.delete(filename)
        return jsonify({'msg': 'deleted file'})