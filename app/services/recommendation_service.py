class RecommendationService:
    def __init__(self):
        self.recommendations = {
            'Bacterial_Blight': {
                'description': 'Bacterial blight is a serious disease caused by Xanthomonas oryzae pv. oryzae.',
                'treatments': [
                    'Use disease-resistant varieties',
                    'Apply copper-based bactericides',
                    'Ensure proper field drainage',
                    'Remove infected plants and debris'
                ]
            },
            'Brown_Spot': {
                'description': 'Brown spot is caused by the fungus Cochliobolus miyabeanus.',
                'treatments': [
                    'Apply fungicides',
                    'Maintain proper soil nutrients',
                    'Avoid water stress',
                    'Use certified disease-free seeds'
                ]
            },
            'Leaf_Blast': {
                'description': 'Rice blast is caused by the fungus Magnaporthe oryzae.',
                'treatments': [
                    'Use blast-resistant varieties',
                    'Apply fungicides preventively',
                    'Maintain proper water management',
                    'Balance nitrogen fertilization'
                ]
            },
            'Healthy': {
                'description': 'The plant appears healthy with no visible disease symptoms.',
                'treatments': [
                    'Continue regular monitoring',
                    'Maintain good agricultural practices',
                    'Follow recommended fertilization schedule',
                    'Ensure proper irrigation'
                ]
            }
        }
    
    def get_recommendations(self, disease):
        return self.recommendations.get(disease, {
            'description': 'Unknown disease',
            'treatments': ['Consult a local agricultural expert']
        }) 