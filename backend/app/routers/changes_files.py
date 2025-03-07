
import pathlib
import json
import os
from datetime import datetime

from flask import  request, jsonify
from flask import Blueprint, current_app

#models
from app.models.files_change import FileLog


app_log = Blueprint('logs', __name__)


@app_log.route('/files', methods=["GET"])
def get_logs():
    code = request.args.get("code") 
    last_sync_time = request.args.get("last_sync_time") 

    if not code:
        return jsonify({'msg': 'code is required'}), 400

    if last_sync_time:
        try:
            last_sync_time = datetime.fromisoformat(last_sync_time)
        except ValueError:
            return jsonify({'msg': 'Format date invalid. Use ISO format (YYYY-MM-DDTHH:MM:SS)'}), 400

    try:
        if last_sync_time:
            logs = FileLog.find_last_changes_by_code(code, last_sync_time)
        else:
            logs = FileLog.find_by_code(code)

        logs_dict = [log.to_dict() for log in logs]
        return jsonify(logs_dict), 200

    except Exception as e:
        return jsonify({'msg': str(e)}), 500