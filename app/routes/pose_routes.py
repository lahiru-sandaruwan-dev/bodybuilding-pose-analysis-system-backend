from flask import Blueprint, request, jsonify
from app.controllers.pose_controller import analyze_pose

# Initialize Blueprint
pose_bp = Blueprint('pose', __name__)

@pose_bp.route('/analyze_pose/front_double_biceps', methods=['POST'])
def analyze_pose_route():
    """
    API Endpoint: `/api/analyze_pose`
    Accepts JSON body with 'angles' array.
    """
    data = request.json
    angles = data.get("angles")
    response, status_code = analyze_pose(angles)
    return jsonify(response), status_code

# from flask import Blueprint, request, jsonify
# from flask_socketio import emit
# from app import socketio  # Import the initialized socketio instance
# from app.controllers.pose_controller import analyze_pose

# # Initialize Blueprint
# pose_bp = Blueprint('pose', __name__)

# @socketio.on('pose_data')  # Handling the Socket.IO event
# def handle_pose_data(data):
#     """
#     Handle incoming pose data sent from the client (via socket).
#     The data should include the angles array.
#     """
#     angles = data.get("angles")
    
#     if not angles or len(angles) != 4:
#         emit('error', {'message': 'Invalid input. Provide exactly 4 angle values.'})
#         return

#     # Call the analyze_pose function to get the pose analysis
#     response, status_code = analyze_pose(angles)
    
#     # Emit the result to the client
#     emit('pose_analysis_result', response)  # Send the result back to the client

# @pose_bp.route('/analyze_pose/front_double_biceps', methods=['POST'])
# def analyze_pose_route():
#     """
#     API Endpoint: `/api/analyze_pose/front_double_biceps`
#     Accepts JSON body with 'angles' array.
#     """
#     data = request.json
#     angles = data.get("angles")
#     response, status_code = analyze_pose(angles)
#     return jsonify(response), status_code

