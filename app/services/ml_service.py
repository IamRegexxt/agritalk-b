import tensorflow as tf
import numpy as np
import cv2
from PIL import Image
import requests
from io import BytesIO

class MLService:
    def __init__(self):
        # Load the model
        self.model = tf.keras.models.load_model('app/ml_models/rice_disease_model.h5')
        self.class_names = ['Bacterial_Blight', 'Brown_Spot', 'Healthy', 'Leaf_Blast']
        self.target_size = (224, 224)  # Model's expected input size
        
    def preprocess_image(self, image_url):
        # Download image from URL
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))
        
        # Convert to numpy array
        img_array = np.array(img)
        
        # Resize
        img_resized = cv2.resize(img_array, self.target_size)
        
        # Normalize
        img_normalized = img_resized / 255.0
        
        # Add batch dimension
        img_batch = np.expand_dims(img_normalized, axis=0)
        
        return img_batch
        
    def predict(self, image_url):
        try:
            # Preprocess the image
            processed_image = self.preprocess_image(image_url)
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            
            # Get the predicted class and confidence
            predicted_class_index = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_index])
            disease = self.class_names[predicted_class_index]
            
            return {
                'disease': disease,
                'confidence': confidence
            }
            
        except Exception as e:
            print(f"Prediction error: {str(e)}")
            return None 