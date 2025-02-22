from flask import Blueprint, request, jsonify
from app.controllers.pose_controller import analyze_pose

# Initialize Blueprint
pose_bp = Blueprint('pose', __name__)

@pose_bp.route('/analyze_pose', methods=['POST'])
def analyze_pose_route():
    """
    API Endpoint: `/api/analyze_pose`
    Accepts JSON body with 'angles' array.
    """
    data = request.json
    angles = data.get("angles")
    response, status_code = analyze_pose(angles)
    return jsonify(response), status_code
