from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db
from routes.auth_routes import auth_bp
from routes.predict_routes import predict_bp
from create_db_script import create_database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database exists
    create_database()

    # Extensions
    CORS(app)
    db.init_app(app)
    jwt = JWTManager(app)

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        print(f"DEBUG: Invalid Token Error: {error}")
        return jsonify({'error': 'Invalid token', 'message': error}), 422

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        print(f"DEBUG: Missing Token Error: {error}")
        return jsonify({'error': 'Missing token', 'message': error}), 401

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        print(f"DEBUG: Expired Token Error: {jwt_payload}")
        return jsonify({'error': 'Token expired', 'message': 'Please login again'}), 401

    # Blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(predict_bp, url_prefix='/api')

    # Create Database Tables
    with app.app_context():
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
