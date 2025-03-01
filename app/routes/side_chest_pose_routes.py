from flask import Blueprint, request, jsonify
from app.controllers.side_chest_pose_controller import analyze_side_chest_pose  # Import the side chest pose controller

# Initialize Blueprint
side_chest_pose_bp = Blueprint('side_chest_pose', __name__)

@side_chest_pose_bp.route('/analyze_pose/side_chest', methods=['POST'])
def analyze_side_chest_route():
    """
    API Endpoint: `/api/analyze_pose/side_chest`
    Accepts JSON body with 'angles' array for side chest pose.
    """
    data = request.json
    angles = data.get("angles")
    
    if not angles:
        return jsonify({"error": "Angles are required"}), 400
    
    response, status_code = analyze_side_chest_pose(angles)
    return jsonify(response), status_code
