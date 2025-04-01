import numpy as np
import cv2
from PIL import Image
import requests
from io import BytesIO
import onnxruntime
from app.utils.constants import CROP_TYPES, DISEASE_TYPES


class MLService:
    def __init__(self):
        # Load ONNX models for each crop type using onnxruntime
        self.models = {
            # 'corn': onnxruntime.InferenceSession('app/ml_models/corn_disease_model.onnx'),
            'rice': onnxruntime.InferenceSession('app/ml_models/rice.onnx'),
            'tomato': onnxruntime.InferenceSession('app/ml_models/tomato.onnx')
        }
        self.target_size = (224, 224)  # Input size expected by the model

    def preprocess_image(self, image_url):
        try:
            # Download image from URL
            response = requests.get(image_url)
            img = Image.open(BytesIO(response.content))

            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')

            # Convert image to numpy array and resize
            img_array = np.array(img)
            img_resized = cv2.resize(img_array, self.target_size)

            # Convert to float32 and scale to [0, 1]
            img_resized = img_resized.astype(np.float32) / 255.0

            # Normalize using ImageNet mean and std
            mean = np.array([0.485, 0.456, 0.406])
            std = np.array([0.229, 0.224, 0.225])
            img_normalized = (img_resized - mean) / std

            # Transpose to channel-first format: (channels, height, width)
            img_transposed = np.transpose(img_normalized, (2, 0, 1))

            # Add batch dimension: (1, channels, height, width)
            img_batch = np.expand_dims(img_transposed, axis=0)

            return img_batch

        except Exception as e:
            print(f"Image preprocessing error: {str(e)}")
            return None

    def predict(self, image_url, crop_type):
        if crop_type not in CROP_TYPES:
            raise ValueError(f"Invalid crop type. Must be one of {CROP_TYPES}")

        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_url)
            if processed_image is None:
                return None

            # Get the ONNX model session and determine input name
            session = self.models[crop_type]
            input_name = session.get_inputs()[0].name

            # Run inference using the ONNX runtime
            # Ensure the input is of type float32
            predictions = session.run(None, {input_name: processed_image.astype(np.float32)})[0]

            # Get predicted class and confidence
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])
            disease = DISEASE_TYPES[crop_type][predicted_class_index]

            return {
                'disease': disease,
                'confidence': confidence,
                'crop_type': crop_type
            }

        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return None
