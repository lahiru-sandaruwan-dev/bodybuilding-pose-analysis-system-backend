# # -------------------New Codes with feedbacks---------------------------------
import numpy as np
import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError

# Load the trained model with custom objects
model = tf.keras.models.load_model('app/models/front_double_biceps_model_optimized (1).h5', custom_objects={'mse': MeanSquaredError()})

# Define ideal angles for the Front Double Biceps pose
ideal_angles = np.array([100, 180, 50, 160])  # [Elbow angle, Shoulder angle, Wrist angle, Triceps angle]

def get_correction_feedback(current_angles, ideal_angles):
    feedback = []
    
    # Elbow Angle: The arm should be around 90-120°.
    diff_elbow = ideal_angles[0] - current_angles[0]
    if diff_elbow > 5:
        feedback.append(f"Increase the elbow angle a little. (Increase by {abs(diff_elbow)}°)")
    elif diff_elbow < -5:
        feedback.append(f"Decrease the elbow angle a little. (Decrease by {abs(diff_elbow)}°)")
    else:
        feedback.append("Elbow position looks good!")

    # Shoulder Angle: The angle should be around 180°.
    diff_shoulder = ideal_angles[1] - current_angles[1]
    if diff_shoulder > 5:
        feedback.append(f"Relax your shoulders and aim for a 180° shoulder alignment. (Increase by {abs(diff_shoulder)}°)")
    elif diff_shoulder < -5:
        feedback.append(f"Bring your shoulders closer to a 180° alignment. (Decrease by {abs(diff_shoulder)}°)")
    else:
        feedback.append("Shoulder positioning looks good!")

    # Wrist Angle: The wrist should be around 45-60°.
    diff_wrist = ideal_angles[2] - current_angles[2]
    if diff_wrist > 5:
        feedback.append(f"Adjust your wrist angle to around 45-60°. (Increase by {abs(diff_wrist)}°)")
    elif diff_wrist < -5:
        feedback.append(f"Bring your wrist angle closer to 45-60°. (Decrease by {abs(diff_wrist)}°)")
    else:
        feedback.append("Wrist position looks good!")

    # Triceps Angle: The triceps should have a slight flexion.
    diff_triceps = ideal_angles[3] - current_angles[3]
    if diff_triceps > 5:
        feedback.append(f"Relax your triceps slightly. (Decrease by {abs(diff_triceps)}°)")
    elif diff_triceps < -5:
        feedback.append(f"Contract your triceps slightly. (Increase by {abs(diff_triceps)}°)")
    else:
        feedback.append("Triceps position looks good!")

    return feedback

def analyze_pose(angles):
    """
    Processes pose angles through the model and returns predictions.
    :param angles: List of 4 angles (e.g., [160, 160, 85, 85])
    :return: JSON response with predictions
    """
    if not angles or len(angles) != 4:
        return {
            "status": "error",
            "isSuccessful": False,
            "message": "Invalid input. Provide exactly 4 angle values.",
            "data": None
        }, 400

    try:
        # Convert input angles to numpy array and normalize
        test_angles = np.array([angles]) / 180.0  # Normalize input (scale to 0-1 range)

        # Predict results
        predictions = model.predict(test_angles)
        pose_correctness_pred, injury_risk_pred, predicted_muscle_imbalance, \
        biceps_injury_pred, triceps_injury_pred, shoulders_injury_pred = predictions

        # Convert injury risk probability to percentage
        biceps_injury_percentage = round(float(biceps_injury_pred[0][0]) * 100, 1)
        triceps_injury_percentage = round(float(triceps_injury_pred[0][0]) * 100, 1)
        shoulders_injury_percentage = round(float(shoulders_injury_pred[0][0]) * 100, 1)

        # Determine final pose status
        pose_status = "Pose is Correct" if pose_correctness_pred[0][0] > 0.8 else "Pose is Incorrect"
        
        # Get feedback on how to improve the pose if it's incorrect
        if pose_correctness_pred[0][0] < 0.8:
            feedback = get_correction_feedback(angles, ideal_angles)
        else:
            feedback = ["Pose is perfect!"]

        # Set injury risk thresholds
        injury_status_biceps = "High Risk of Injury" if biceps_injury_pred[0][0] > 0.2 else "Low Risk of Injury"
        injury_status_triceps = "High Risk of Injury" if triceps_injury_pred[0][0] > 0.25 else "Low Risk of Injury"
        injury_status_shoulders = "High Risk of Injury" if shoulders_injury_pred[0][0] > 0.2 else "Low Risk of Injury"

        # Prepare response data
        data = {
            "pose_status": pose_status,
            "pose_correctness_score": round(float(pose_correctness_pred[0][0]), 2),
            "injury_risk_percentage": round(float(injury_risk_pred[0][0]) * 100, 1),
            "biceps_injury_risk": {
                "probability": biceps_injury_percentage,
                "status": injury_status_biceps
            },
            "triceps_injury_risk": {
                "probability": triceps_injury_percentage,
                "status": injury_status_triceps
            },
            "shoulders_injury_risk": {
                "probability": shoulders_injury_percentage,
                "status": injury_status_shoulders
            },
            "predicted_muscle_imbalance": predicted_muscle_imbalance[0].tolist(),
            "feedback": feedback  # Add the feedback to the response
        }

        return {
            "status": "success",
            "isSuccessful": True,
            "message": f"{pose_status}",
            "data": data
        }, 200

    except Exception as e:
        return {
            "status": "error",
            "isSuccessful": False,
            "message": str(e),
            "data": None
        }, 500


# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.losses import MeanSquaredError
# from flask import Flask, request, jsonify
# from flask_socketio import SocketIO, emit

# # Initialize Flask app and SocketIO
# app = Flask(__name__)
# socketio = SocketIO(app)

# # Load the trained model with custom objects
# model = tf.keras.models.load_model('app/models/front_double_biceps_model_optimized (1).h5', custom_objects={'mse': MeanSquaredError()})

# # Define ideal angles for the Front Double Biceps pose
# ideal_angles = np.array([100, 180, 50, 160])  # [Elbow angle, Shoulder angle, Wrist angle, Triceps angle]

# def get_correction_feedback(current_angles, ideal_angles):
#     feedback = []
    
#     # Elbow Angle: The arm should be around 90-120°.
#     diff_elbow = ideal_angles[0] - current_angles[0]
#     if diff_elbow > 5:
#         feedback.append(f"Increase the elbow angle a little. (Increase by {abs(diff_elbow)}°)")
#     elif diff_elbow < -5:
#         feedback.append(f"Decrease the elbow angle a little. (Decrease by {abs(diff_elbow)}°)")
#     else:
#         feedback.append("Elbow position looks good!")

#     # Shoulder Angle: The angle should be around 180°.
#     diff_shoulder = ideal_angles[1] - current_angles[1]
#     if diff_shoulder > 5:
#         feedback.append(f"Relax your shoulders and aim for a 180° shoulder alignment. (Increase by {abs(diff_shoulder)}°)")
#     elif diff_shoulder < -5:
#         feedback.append(f"Bring your shoulders closer to a 180° alignment. (Decrease by {abs(diff_shoulder)}°)")
#     else:
#         feedback.append("Shoulder positioning looks good!")

#     # Wrist Angle: The wrist should be around 45-60°.
#     diff_wrist = ideal_angles[2] - current_angles[2]
#     if diff_wrist > 5:
#         feedback.append(f"Adjust your wrist angle to around 45-60°. (Increase by {abs(diff_wrist)}°)")
#     elif diff_wrist < -5:
#         feedback.append(f"Bring your wrist angle closer to 45-60°. (Decrease by {abs(diff_wrist)}°)")
#     else:
#         feedback.append("Wrist position looks good!")

#     # Triceps Angle: The triceps should have a slight flexion.
#     diff_triceps = ideal_angles[3] - current_angles[3]
#     if diff_triceps > 5:
#         feedback.append(f"Relax your triceps slightly. (Decrease by {abs(diff_triceps)}°)")
#     elif diff_triceps < -5:
#         feedback.append(f"Contract your triceps slightly. (Increase by {abs(diff_triceps)}°)")
#     else:
#         feedback.append("Triceps position looks good!")

#     return feedback

# def analyze_pose(angles):
#     """
#     Processes pose angles through the model and returns predictions.
#     :param angles: List of 4 angles (e.g., [160, 160, 85, 85])
#     :return: JSON response with predictions
#     """
#     if not angles or len(angles) != 4:
#         return {
#             "status": "error",
#             "isSuccessful": False,
#             "message": "Invalid input. Provide exactly 4 angle values.",
#             "data": None
#         }, 400

#     try:
#         # Convert input angles to numpy array and normalize
#         test_angles = np.array([angles]) / 180.0  # Normalize input (scale to 0-1 range)

#         # Predict results
#         predictions = model.predict(test_angles)
#         pose_correctness_pred, injury_risk_pred, predicted_muscle_imbalance, \
#         biceps_injury_pred, triceps_injury_pred, shoulders_injury_pred = predictions

#         # Convert injury risk probability to percentage
#         biceps_injury_percentage = round(float(biceps_injury_pred[0][0]) * 100, 1)
#         triceps_injury_percentage = round(float(triceps_injury_pred[0][0]) * 100, 1)
#         shoulders_injury_percentage = round(float(shoulders_injury_pred[0][0]) * 100, 1)

#         # Determine final pose status
#         pose_status = "Pose is Correct" if pose_correctness_pred[0][0] > 0.8 else "Pose is Incorrect"
        
#         # Get feedback on how to improve the pose if it's incorrect
#         if pose_correctness_pred[0][0] < 0.8:
#             feedback = get_correction_feedback(angles, ideal_angles)
#         else:
#             feedback = ["Pose is perfect!"]

#         # Set injury risk thresholds
#         injury_status_biceps = "High Risk of Injury" if biceps_injury_pred[0][0] > 0.2 else "Low Risk of Injury"
#         injury_status_triceps = "High Risk of Injury" if triceps_injury_pred[0][0] > 0.25 else "Low Risk of Injury"
#         injury_status_shoulders = "High Risk of Injury" if shoulders_injury_pred[0][0] > 0.2 else "Low Risk of Injury"

#         # Prepare response data
#         data = {
#             "pose_status": pose_status,
#             "pose_correctness_score": round(float(pose_correctness_pred[0][0]), 2),
#             "injury_risk_percentage": round(float(injury_risk_pred[0][0]) * 100, 1),
#             "biceps_injury_risk": {
#                 "probability": biceps_injury_percentage,
#                 "status": injury_status_biceps
#             },
#             "triceps_injury_risk": {
#                 "probability": triceps_injury_percentage,
#                 "status": injury_status_triceps
#             },
#             "shoulders_injury_risk": {
#                 "probability": shoulders_injury_percentage,
#                 "status": injury_status_shoulders
#             },
#             "predicted_muscle_imbalance": predicted_muscle_imbalance[0].tolist(),
#             "feedback": feedback  # Add the feedback to the response
#         }

#         return data  # Return the data for socket emission

#     except Exception as e:
#         return {
#             "status": "error",
#             "isSuccessful": False,
#             "message": str(e),
#             "data": None
#         }

# # SocketIO event for receiving angles and emitting predictions
# @socketio.on('pose_data')
# def handle_pose_data(data):
#     angles = data.get('angles', [])
#     if not angles or len(angles) != 4:
#         emit('pose_response', {'status': 'error', 'message': 'Invalid input. Provide exactly 4 angle values.'})
#         return
    
#     response_data = analyze_pose(angles)
#     emit('pose_response', response_data)

# if __name__ == '__main__':
#     socketio.run(app, debug=True)
