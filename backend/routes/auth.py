from flask import Blueprint, request, jsonify, current_app
from backend.model import User
from backend.extension import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from itsdangerous import URLSafeTimedSerializer
import uuid

auth_bp = Blueprint('auth', __name__)

# SignUp
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    if not email or not password or not role:
        return jsonify({'message': 'Missing data'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'message': 'User already exists'}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        id=str(uuid.uuid4()),
        email=email,
        password=hashed_password,
        role=role,
        is_verified=False
    )
    db.session.add(new_user)
    db.session.commit()

    if role == 'client':
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        token = s.dumps(email, salt='email-confirm')
        verification_url = f"http://localhost:5000/api/auth/verify/{token}"

        return jsonify({
            'message': 'Client created successfully. Verify your email using the URL.',
            'verification_url': verification_url
        }), 201

    return jsonify({'message': 'Ops user created successfully'}), 201


# Email Verification
@auth_bp.route('/verify/<token>', methods=['GET'])
def verify_email(token):
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
        # Token valid for 1 hour
    except Exception as e:
        return jsonify({'message': 'Invalid or expired token'}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404

    user.is_verified = True
    db.session.commit()
    return jsonify({'message': 'Email verified successfully!'}), 200


# Login
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({'message': 'Invalid credentials'}), 401

    if user.role == 'client' and not user.is_verified:
        return jsonify({'message': 'Email not verified'}), 403

    access_token = create_access_token(identity={'id': user.id, 'role': user.role})
    return jsonify({'token': access_token, 'role': user.role}), 200
