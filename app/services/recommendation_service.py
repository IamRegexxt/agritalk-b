class RecommendationService:
    def __init__(self):
        self.recommendations = {
            'corn': {
                'Blight': {
                    'description': 'A fungal disease that causes long brown streaks on leaves.',
                    'treatments': [
                        'Apply fungicides containing pyraclostrobin',
                        'Rotate crops to reduce disease pressure',
                        'Plant resistant varieties',
                        'Improve field drainage'
                    ]
                },
                'Common Rust': {
                    'description': 'Fungal disease causing small, circular brown pustules.',
                    'treatments': [
                        'Apply foliar fungicides',
                        'Plant early in the season',
                        'Use resistant hybrids',
                        'Monitor humidity levels'
                    ]
                },
                'Gray Leaf Spot': {
                    'description': 'Fungal disease causing rectangular gray lesions.',
                    'treatments': [
                        'Rotate with non-host crops',
                        'Apply fungicides preventively',
                        'Improve air circulation',
                        'Remove crop debris'
                    ]
                }
            },
            'rice': {
                'Blast': {
                    'description': 'Fungal disease affecting leaves and panicles.',
                    'treatments': [
                        'Use resistant varieties',
                        'Apply fungicides preventively',
                        'Maintain proper water management',
                        'Balance nitrogen fertilization'
                    ]
                },
                'Bacterial Blight': {
                    'description': 'Bacterial disease causing yellow to white lesions.',
                    'treatments': [
                        'Plant resistant varieties',
                        'Use balanced fertilization',
                        'Avoid excessive nitrogen',
                        'Maintain proper spacing'
                    ]
                },
                'Brown Spot': {
                    'description': 'Fungal disease causing oval brown spots.',
                    'treatments': [
                        'Apply fungicides',
                        'Maintain proper soil nutrients',
                        'Avoid water stress',
                        'Use certified seeds'
                    ]
                }
            },
            'tomato': {
                'Early Blight': {
                    'description': 'Fungal disease causing dark spots with concentric rings.',
                    'treatments': [
                        'Apply copper-based fungicides',
                        'Remove infected leaves',
                        'Improve air circulation',
                        'Mulch around plants'
                    ]
                },
                'Late Blight': {
                    'description': 'Water mold causing dark, water-soaked lesions.',
                    'treatments': [
                        'Apply preventive fungicides',
                        'Remove infected plants',
                        'Avoid overhead irrigation',
                        'Space plants properly'
                    ]
                },
                'Leaf Mold': {
                    'description': 'Fungal disease causing yellow spots and mold growth.',
                    'treatments': [
                        'Reduce humidity',
                        'Improve ventilation',
                        'Apply fungicides',
                        'Remove infected leaves'
                    ]
                }
            }
        }
    
    def get_recommendations(self, crop_type, disease):
        if disease == 'Healthy':
            return {
                'description': 'The plant appears healthy with no visible disease symptoms.',
                'treatments': [
                    'Continue regular monitoring',
                    'Maintain good agricultural practices',
                    'Follow recommended fertilization schedule',
                    'Ensure proper irrigation'
                ]
            }
            
        return self.recommendations.get(crop_type, {}).get(disease, {
            'description': 'Unknown disease',
            'treatments': ['Consult a local agricultural expert']
        }) 