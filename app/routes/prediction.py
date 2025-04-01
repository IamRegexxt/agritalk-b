from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.s3_service import S3Service
from app.models.prediction import Prediction
from app import db
import magic
from app.services.recommendation_service import RecommendationService
#from app.utils.constants import CROP_TYPES
from io import BytesIO

prediction_bp = Blueprint('prediction', __name__)
s3_service = S3Service()
recommendation_service = RecommendationService()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@prediction_bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file provided'}), 400

    file = request.files['image']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(file.filename):
        return jsonify({'error': 'File type not allowed'}), 400

    # Create in-memory file buffer
    file_buffer = BytesIO()
    file.save(file_buffer)  # Save FileStorage to BytesIO
    file_buffer.seek(0)

    # Check file size
    file_size = len(file_buffer.getvalue())
    if file_size > MAX_FILE_SIZE:
        return jsonify({'error': 'File size exceeds limit'}), 400

    # Check MIME type
    header = file_buffer.read(2048)
    file_buffer.seek(0)

    try:
        file_type = magic.from_buffer(header, mime=True)
    except UnicodeDecodeError:
        return jsonify({'error': 'Invalid file encoding'}), 400

    if not file_type.startswith('image/'):
        return jsonify({'error': 'Invalid file type'}), 400

    crop_type = request.form.get('crop_type')
    if not crop_type:
        return jsonify({'error': 'Crop type is required'}), 400

    # Upload to S3
    image_url = s3_service.upload_file(file_buffer, crop_type, file.filename)
    if not image_url:
        return jsonify({'error': 'Failed to upload image'}), 500

    # Create prediction record
    prediction = Prediction(
        user_id=get_jwt_identity(),
        crop_type=crop_type,
        image_path=image_url,
        disease='Processing',
        confidence=0.0
    )

    db.session.add(prediction)
    db.session.commit()

    from app.services.celery_service import process_image
    process_image.delay(prediction.id)

    return jsonify({
        'message': 'Image uploaded successfully',
        'prediction_id': prediction.id,
        'image_url': image_url
    }), 201


@prediction_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_prediction(id):
    user_id = int(get_jwt_identity())  # Ensure user_id is an integer
    print(f"🔍 Extracted JWT User ID: {user_id}")

    prediction = Prediction.query.get_or_404(id)
    print(f" Prediction User ID: {prediction.user_id}")


    if prediction.user_id != user_id:
        print(" Unauthorized: User ID mismatch!")
        return jsonify({'error': 'Unauthorized'}), 403


    recommendations = {}
    if prediction.disease != 'Processing':
        recommendations = recommendation_service.get_recommendations(prediction.crop_type, prediction.disease)  # ✅ Fixed

    return jsonify({
        'id': prediction.id,
        'image_url': prediction.image_path,
        'disease': prediction.disease,
        'confidence': prediction.confidence,
        'created_at': prediction.created_at.isoformat(),
        'recommendations': recommendations
    }), 200
