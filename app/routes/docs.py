from flask import Blueprint, jsonify

docs_bp = Blueprint('docs', __name__)

@docs_bp.route('/docs', methods=['GET'])
def get_api_docs():
    api_docs = {
        "api_version": "1.0.0",
        "endpoints": {
            "Authentication": {
                "/api/register": {
                    "method": "POST",
                    "description": "Register a new user",
                    "params": ["email", "password"]
                },
                "/api/login": {
                    "method": "POST",
                    "description": "Login and receive JWT token",
                    "params": ["email", "password"]
                }
            },
            "Predictions": {
                "/api/upload": {
                    "method": "POST",
                    "description": "Upload an image for disease prediction",
                    "params": ["image (file)"],
                    "auth_required": True
                },
                "/api/predictions/{id}": {
                    "method": "GET",
                    "description": "Get prediction results",
                    "params": ["id (path)"],
                    "auth_required": True
                }
            },
            "Feedback": {
                "/api/feedback": {
                    "method": "POST",
                    "description": "Submit feedback on a prediction",
                    "params": ["prediction_id", "accuracy_rating", "comments (optional)"],
                    "auth_required": True
                },
                "/api/feedback/{prediction_id}": {
                    "method": "GET",
                    "description": "Get feedback for a prediction",
                    "params": ["prediction_id (path)"],
                    "auth_required": True
                }
            },
            "User": {
                "/api/user/history": {
                    "method": "GET",
                    "description": "Get user's prediction history",
                    "auth_required": True
                },
                "/api/user/stats": {
                    "method": "GET",
                    "description": "Get user's statistics",
                    "auth_required": True
                }
            },
            "Admin": {
                "/api/admin/users": {
                    "method": "GET",
                    "description": "Get all users (admin only)",
                    "auth_required": True
                },
                "/api/admin/recent-predictions": {
                    "method": "GET",
                    "description": "Get recent predictions (admin only)",
                    "auth_required": True
                },
                "/api/admin/recent-feedback": {
                    "method": "GET",
                    "description": "Get recent feedback (admin only)",
                    "auth_required": True
                }
            },
            "Analytics": {
                "/api/analytics/summary": {
                    "method": "GET",
                    "description": "Get analytics summary (admin only)",
                    "auth_required": True
                },
                "/api/analytics/predictions": {
                    "method": "GET",
                    "description": "Get prediction analytics (admin only)",
                    "auth_required": True
                },
                "/api/analytics/feedback": {
                    "method": "GET",
                    "description": "Get feedback analytics (admin only)",
                    "auth_required": True
                }
            }
        }
    }
    
    return jsonify(api_docs), 200 