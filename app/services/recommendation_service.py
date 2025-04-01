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
                'Common_Rust': {
                    'description': 'Fungal disease causing small, circular brown pustules.',
                    'treatments': [
                        'Apply foliar fungicides',
                        'Plant early in the season',
                        'Use resistant hybrids',
                        'Monitor humidity levels'
                    ]
                },
                'Gray_Leaf_Spot': {
                    'description': 'Fungal disease causing rectangular gray lesions.',
                    'treatments': [
                        'Rotate with non-host crops',
                        'Apply fungicides preventively',
                        'Improve air circulation',
                        'Remove crop debris'
                    ]
                }
                # Note: "Healthy" is handled separately in get_recommendations.
            },
            'rice': {
                'leaf_blast': {
                    'description': 'Fungal disease affecting leaves and panicles.',
                    'treatments': [
                        'Use resistant varieties',
                        'Apply fungicides preventively',
                        'Maintain proper water management',
                        'Balance nitrogen fertilization'
                    ]
                },
                'bacterial_leaf_blight': {
                    'description': 'Bacterial disease causing yellow to white lesions.',
                    'treatments': [
                        'Plant resistant varieties',
                        'Use balanced fertilization',
                        'Avoid excessive nitrogen',
                        'Maintain proper spacing'
                    ]
                },
                'brown_spot': {
                    'description': 'Fungal disease causing oval brown spots.',
                    'treatments': [
                        'Apply fungicides',
                        'Maintain proper soil nutrients',
                        'Avoid water stress',
                        'Use certified seeds'
                    ]
                },
                # Added missing diseases from constants for rice:
                'narrow_brown_spot': {
                    'description': 'Fungal disease causing narrow brown spots on leaves.',
                    'treatments': [
                        'Apply appropriate fungicides',
                        'Ensure proper water management',
                        'Remove infected plants',
                        'Practice crop rotation'
                    ]
                },
                'healthy': {  # Lowercase "healthy" added so both cases are covered.
                    'description': 'The plant appears healthy with no visible disease symptoms.',
                    'treatments': [
                        'Continue regular monitoring',
                        'Maintain good agricultural practices',
                        'Follow recommended fertilization schedule',
                        'Ensure proper irrigation'
                    ]
                },
                'leaf_scald': {
                    'description': 'A disease that causes scalding on rice leaves, leading to discoloration.',
                    'treatments': [
                        'Apply fungicides',
                        'Improve field drainage',
                        'Remove infected residues',
                        'Maintain proper spacing'
                    ]
                },
                'Rice Hispa': {
                    'description': 'A pest infestation that causes damage to the rice crop by feeding on the plant tissue.',
                    'treatments': [
                        'Apply recommended insecticides',
                        'Monitor pest population',
                        'Use integrated pest management strategies',
                        'Remove infested plant parts'
                    ]
                },
                'Neck_Blast': {
                    'description': 'A disease affecting the neck of the rice plant, leading to rot and yield loss.',
                    'treatments': [
                        'Use resistant varieties',
                        'Apply appropriate fungicides',
                        'Practice crop rotation',
                        'Improve field hygiene'
                    ]
                },
                'Sheath Blight': {
                    'description': 'A fungal disease affecting the sheath of the rice plant, causing lesions and reducing yield.',
                    'treatments': [
                        'Apply fungicides',
                        'Reduce planting density',
                        'Improve field drainage',
                        'Remove infected plant debris'
                    ]
                },
                'Tungro': {
                    'description': 'A viral disease transmitted by insects, causing stunting and yellowing of rice plants.',
                    'treatments': [
                        'Control insect vectors',
                        'Remove infected plants',
                        'Use resistant varieties',
                        'Practice proper water management'
                    ]
                }
            },
            'tomato': {
                'Tomato___Early_blight': {
                    'description': 'Fungal disease causing dark spots with concentric rings.',
                    'treatments': [
                        'Apply copper-based fungicides',
                        'Remove infected leaves',
                        'Improve air circulation',
                        'Mulch around plants'
                    ]
                },
                'Tomato___Leaf_Mold': {
                    'description': 'Fungal disease causing yellow spots and mold growth.',
                    'treatments': [
                        'Reduce humidity',
                        'Improve ventilation',
                        'Apply fungicides',
                        'Remove infected leaves'
                    ]
                },
                # Added missing diseases from constants for tomato:
                'Tomato___Bacterial_spot': {
                    'description': 'A bacterial infection that causes dark spots on tomato leaves and fruits.',
                    'treatments': [
                        'Apply copper-based bactericides',
                        'Use certified disease-free seeds',
                        'Ensure proper spacing',
                        'Remove infected parts'
                    ]
                },
                'Tomato___healthy': {
                    'description': 'The plant appears healthy with no visible disease symptoms.',
                    'treatments': [
                        'Continue regular monitoring',
                        'Maintain proper nutrition',
                        'Follow recommended irrigation practices',
                        'Practice crop hygiene'
                    ]
                },
                'Tomato___Late_blight': {
                    'description': 'A highly destructive fungal disease that causes dark, water-soaked lesions on leaves, stems, and fruits.',
                    'treatments': [
                        'Apply fungicides containing chlorothalonil or copper-based compounds',
                        'Remove and destroy infected plant parts',
                        'Improve air circulation and avoid overhead watering',
                        'Use disease-resistant tomato varieties'
                    ]
                },
                'Tomato___Septoria_leaf_spot': {
                    'description': 'A fungal disease resulting in small, dark spots on the leaves.',
                    'treatments': [
                        'Apply appropriate fungicides',
                        'Remove infected foliage',
                        'Ensure proper spacing',
                        'Use resistant varieties'
                    ]
                },
                'Tomato___Spider_mites Two-spotted_spider_mite': {
                    'description': 'A pest infestation causing damage and stippling on leaves.',
                    'treatments': [
                        'Use miticides',
                        'Introduce natural predators',
                        'Increase humidity',
                        'Regularly inspect and clean plants'
                    ]
                },
                'Tomato___Target_Spot': {
                    'description': 'A fungal disease characterized by circular spots with concentric rings on leaves.',
                    'treatments': [
                        'Apply fungicides',
                        'Practice crop rotation',
                        'Remove infected leaves',
                        'Improve field ventilation'
                    ]
                },
                'Tomato___Tomato_mosaic_virus': {
                    'description': 'A viral disease causing mottled leaves and reduced plant vigor.',
                    'treatments': [
                        'Remove infected plants',
                        'Control insect vectors',
                        'Use resistant varieties',
                        'Maintain field sanitation'
                    ]
                },
                'Tomato___Tomato_Yellow_Leaf_Curl_Virus': {
                    'description': 'A viral disease leading to yellowing and curling of leaves, affecting yield.',
                    'treatments': [
                        'Remove infected plants',
                        'Control whitefly populations',
                        'Use resistant cultivars',
                        'Ensure proper field management'
                    ]
                }
            }
        }

    def get_recommendations(self, crop_type, disease):
        # Handle the case where a "Healthy" status is explicitly provided.
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
