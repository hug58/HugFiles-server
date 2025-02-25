
from flask import Blueprint, current_app
import pathlib
import json
import os

from urllib.parse import urljoin
from flask import  request, send_from_directory, jsonify

from app.utils.files_read import get_files
from app.utils import services

app_data = Blueprint('data', __name__)


@app_data.route('/<path:filename>', methods=['POST', 'PUT', 'DELETE'])
def data(filename):
    '''Handle files.'''
    
    path = pathlib.Path(filename)
    filename = urljoin(current_app.config['UPLOAD_FOLDER'], filename)


    # if request.method == 'GET':
    #     if os.path.isfile(filename):
    #         path = pathlib.Path(filename)
    #         print(f"FILENAME: {str(path.parent)} ::: {path.name}")
    #         return send_from_directory(path.parent, path.name)
    #     elif os.path.isdir(filename):
    #         return jsonify(get_files(filename, path.name))

    #     return jsonify({'msg': 'account does not exist'})

    if request.method == 'POST':
        if not os.path.isdir(filename):
            os.makedirs(filename, exist_ok=True)

        if 'upload_file' not in request.files:
            return jsonify({'msg': 'directory created'})

        file = request.files['upload_file']
        full_path = os.path.join(filename, file.filename)
        file.save(full_path)
        
        
        # if request.form.get('modified_at'):
        #     atime = request.form.get('created_at')
        #     mtime = request.form.get('modified_at')
        #     os.utime(full_path, (atime, mtime))
        

        return jsonify({'msg': 'save uploaded file' })

    elif request.method == 'PUT':
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
                    if request.get('modified_at'):
                        atime = int(request['created_at'])
                        mtime = int(request['modified_at'])
                        os.utime(full_path, (atime, mtime))
                    return jsonify({'msg': 'successfully updated file'})
            else:
                return jsonify({'msg': 'did not update uploaded file'})
        else:
            return {'File not found': filename}, 404

    elif request.method == 'DELETE':
        services.delete(filename)
        return jsonify({'msg': 'deleted file'})


@app_data.route('/consult', methods=['POST'])
def consult():
    '''
    DATA FILENAME FOR FILES AND DIRECTORY
    '''
    data_filename:dict = request.get_json()
    _path_filename:str = data_filename.get('filename')
    _path_filename:str = _path_filename.lstrip('/')
    code = data_filename.get('code')
    
     
    path = os.path.join(code, _path_filename )
    path = path.replace('\\', '/') if os.name != 'posix' else path
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], path)
    
    
    return jsonify(get_files(filename, code))



@app_data.route('/download', methods=['POST'])
def download():
    ''' DATA FILENAME FOR FILES AND DIRECTORY '''
    
    data_filename:dict = request.get_json()
    _path_filename:str = data_filename.get('filename')
    _path_filename:str = _path_filename.lstrip('/')
    
     
    path = os.path.join(data_filename.get('code'),_path_filename )
    path = path.replace('\\', '/') if os.name != 'posix' else path
    filename = os.path.join(current_app.config['UPLOAD_FOLDER'], path)

    filename = os.path.join(os.path.abspath('.'), filename)

    
    try:
        if os.path.isfile(filename):
            _path = pathlib.Path(filename)
            print(f"FILENAME: {str(_path.parent)} ::: {_path.name}")
            return send_from_directory(_path.parent, _path.name)
    except FileNotFoundError:
        abort(404)
        print("FILE")
    except Exception as e:
        # Manejar otros errores posibles
        print("PROBANDO")
        app.logger.error(f"Error al enviar el archivo: {e}")
        abort(500)
    
    return filename