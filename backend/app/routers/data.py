
from flask import Blueprint, current_app
import pathlib
import json
import os

from urllib.parse import urljoin
from flask import  request, send_from_directory, jsonify

from app.utils.files_read import get_files
from app.utils import services

#models
from app.models.files import FilesModel


app_data = Blueprint('data', __name__)


@app_data.route('/resource/<path:filename>', methods=['POST', 'PUT', 'DELETE'])
def data(filename):
    path = pathlib.Path(filename)
    filename = urljoin(current_app.config['UPLOAD_FOLDER'], filename)


    if request.method == 'POST':
        if not os.path.isdir(filename):
            os.makedirs(filename, exist_ok=True)

        if 'upload_file' not in request.files:
            return jsonify({'msg': 'directory created'})

        file = request.files['upload_file']
        full_path = os.path.join(filename, file.filename)
        file.save(full_path)
        
        
        if request.form.get('modified_at'):
            atime = request.form.get('created_at')
            mtime = request.form.get('modified_at')
            os.utime(full_path, (atime, mtime))
        

        return jsonify({'msg': 'save uploaded file' })

    elif request.method == 'PUT':
        ''' moves uploaded file to the specified location. '''
        if os.path.exists(filename):
            new_path = request.args.get('new_path')
            pass

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


@app_data.route('/files')
def consult_files_db():
    code = request.args.get('code')
    
    if not code:
        return jsonify({'msg': 'Parameter "code" is required'}), 400

    try:
        files = FilesModel.find_by_code_and_status(code=code, exclude_status='deleted')
        return jsonify({'files': files}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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
            return send_from_directory(_path.parent, _path.name)
    except FileNotFoundError:
        abort(404)
    except Exception as e:
        app.logger.error(f"error in send file: {e}")
        abort(500)
    
    return filename