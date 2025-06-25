# backend/routes/file_ops.py
import os
import uuid
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from backend.extension import db
from backend.model import File, User
from datetime import datetime

file_ops_bp = Blueprint('file_ops', __name__)
ALLOWED_EXTENSIONS = {'pptx', 'docx', 'xlsx'}

def is_allowed(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@file_ops_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_file():
    identity = get_jwt_identity()
    user = User.query.get(identity['id'])

    if user.role != 'ops':
        return jsonify({"message": "Only Ops users can upload files"}), 403

    if 'file' not in request.files:
        return jsonify({"message": "No file provided"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"message": "Empty filename"}), 400

    if file and is_allowed(file.filename):
        original_filename = secure_filename(file.filename)
        ext = original_filename.rsplit('.', 1)[1].lower()
        new_id = str(uuid.uuid4())
        new_filename = f"{new_id}.{ext}"
        upload_path = os.path.join('backend', 'uploads', new_filename)
        file.save(upload_path)

        new_file = File(
            id=new_id,
            filename=new_filename,
            original_filename=original_filename,
            uploader_id=user.id,
            file_type=ext,
            upload_time=datetime.utcnow()
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({"message": "File uploaded successfully", "file_id": new_id}), 201

    return jsonify({"message": "Invalid file type"}), 400