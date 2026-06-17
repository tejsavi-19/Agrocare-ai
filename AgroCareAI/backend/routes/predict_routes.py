import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from database import db
from models.scan import Scan
from models.user import User # Import User for stats/context if needed
from ai_engine import ai_engine
import uuid
from datetime import datetime

predict_bp = Blueprint('predict', __name__)


ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@predict_bp.route('/predict', methods=['POST'])
@jwt_required()
def predict():
    # The initial try-except block for JWT identity and prints are removed as per instruction.
    # jwt_required() decorator handles authentication, and get_jwt_identity() is called later
    # when needed for database operations.

    if 'image' not in request.files:
        return jsonify({'error': 'No image part'}), 400
        
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
        
    if file and allowed_file(file.filename):
        # Create uploads directory if it doesn't exist (should be handled in config but double check)
        if not os.path.exists(current_app.config['UPLOAD_FOLDER']):
            os.makedirs(current_app.config['UPLOAD_FOLDER'])

        filename = secure_filename(file.filename)
        # Rename file to avoid collisions
        unique_filename = f"{uuid.uuid4()}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(file_path)
        
        # Predict using AI Engine
        result = ai_engine.predict(file_path)
        
        if result:
            user_id = int(get_jwt_identity())
            
            # Save to database
            new_scan = Scan(
                user_id=user_id,
                image_path=unique_filename, # Store relative path or just filename
                prediction=result['prediction'],
                confidence=result['confidence'],
                risk_level=result['risk_level'],
                advice=result['advice']
            )
            
            try:
                db.session.add(new_scan)
                db.session.commit()
                
                response_data = result
                response_data['scan_id'] = new_scan.id
                return jsonify(response_data), 200
            except Exception as e:
                db.session.rollback()
                return jsonify({'error': f"Database error: {str(e)}"}), 500
        else:
             return jsonify({'error': 'Prediction failed'}), 500
            
    return jsonify({'error': 'File type not allowed'}), 400

@predict_bp.route('/history', methods=['GET'])
@jwt_required()
def history():
    user_id = int(get_jwt_identity())
    scans = Scan.query.filter_by(user_id=user_id).order_by(Scan.timestamp.desc()).all()
    return jsonify([scan.to_dict() for scan in scans]), 200

@predict_bp.route('/history/<int:scan_id>/report', methods=['GET'])
@jwt_required()
def history_report(scan_id):
    user_id = int(get_jwt_identity())
    scan = Scan.query.filter_by(id=scan_id, user_id=user_id).first()
    
    if not scan:
        return jsonify({'error': 'Scan not found'}), 404
        
    file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], scan.image_path)
    
    if not os.path.exists(file_path):
        return jsonify({'error': 'Original image not found'}), 404
        
    # Re-run prediction to generate the full knowledge base report
    result = ai_engine.predict(file_path)
    
    if result:
        result['scan_id'] = scan.id
        result['timestamp'] = scan.timestamp.isoformat()
        return jsonify(result), 200
    else:
        return jsonify({'error': 'Failed to generate report'}), 500

@predict_bp.route('/stats', methods=['GET'])
@jwt_required()
def stats():
    user_id = int(get_jwt_identity())
    user_scans = Scan.query.filter_by(user_id=user_id).all()
    
    total_scans = len(user_scans)
    healthy_count = sum(1 for s in user_scans if s.prediction == 'Healthy')
    diseased_count = sum(1 for s in user_scans if s.prediction == 'Diseased')
    
    # Calculate disease distribution
    disease_map = {}
    for scan in user_scans:
        if scan.prediction == 'Diseased' and scan.disease_type:
            disease_map[scan.disease_type] = disease_map.get(scan.disease_type, 0) + 1
    
    diseases_list = [{'name': name, 'count': count} for name, count in disease_map.items()]
    # Sort by count descending
    diseases_list.sort(key=lambda x: x['count'], reverse=True)

    return jsonify({
        'total_scans': total_scans,
        'predictions': {
            'Healthy': healthy_count,
            'Diseased': diseased_count
        },
        'diseases': diseases_list
    }), 200

from flask import send_from_directory
@predict_bp.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)
