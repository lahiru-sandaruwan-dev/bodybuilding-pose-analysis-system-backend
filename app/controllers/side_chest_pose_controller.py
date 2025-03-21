# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.losses import MeanSquaredError

# # Load the trained model with custom objects
# model = tf.keras.models.load_model('app/models/side_chest_pose_model.h5', custom_objects={'mse': MeanSquaredError()})

# def analyze_side_chest_pose(angles):
#     """
#     Processes side chest pose angles through the model and returns predictions.
#     :param angles: List of 4 angles (e.g., [145, 165, 80, 90])
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
#         pose_status = "Side Chest Pose is Correct" if pose_correctness_pred[0][0] > 0.79 else "Side Chest Pose is Incorrect"

#         # Set injury risk thresholds
#         injury_status_biceps = "High Risk of Injury" if biceps_injury_pred[0][0] > 0.2 else "Low Risk of Injury"
#         injury_status_triceps = "High Risk of Injury" if triceps_injury_pred[0][0] > 0.25 else "Low Risk of Injury"
#         injury_status_shoulders = "High Risk of Injury" if shoulders_injury_pred[0][0] > 0.2 else "Low Risk of Injury"

#         # Prepare response data
#         data = {
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
#             "predicted_muscle_imbalance": predicted_muscle_imbalance[0].tolist()
#         }

#         return {
#             "status": "success",
#             "isSuccessful": True,
#             "message": f"{pose_status}",
#             "data": data
#         }, 200

#     except Exception as e:
#         return {
#             "status": "error",
#             "isSuccessful": False,
#             "message": str(e),
#             "data": None
#         }, 500

# -------------------New Codes with feedbacks---------------------------------
import numpy as np
import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError

# Load the trained model with custom objects
model = tf.keras.models.load_model('app/models/side_chest_pose_model.h5', custom_objects={'mse': MeanSquaredError()})

# Define ideal angles for the Side Chest pose
ideal_angles = np.array([165, 175, 90, 20])  # [Elbow angle, Shoulder angle, Chest angle, Torso twist angle]

def get_correction_feedback(current_angles, ideal_angles):
    feedback = []
    
    # Elbow Angle: The arm should be around 160-170°.
    diff_elbow = ideal_angles[0] - current_angles[0]
    if diff_elbow > 5:
        feedback.append(f"Raise your arm a little more. (Increase by {abs(diff_elbow)}°)")
    elif diff_elbow < -5:
        feedback.append(f"Lower your arm a little. (Decrease by {abs(diff_elbow)}°)")
    else:
        feedback.append("Arm position looks good!")

    # Shoulder Angle: The angle should be 90°.
    diff_shoulder = ideal_angles[1] - current_angles[1]
    if diff_shoulder > 5:
        feedback.append(f"Pull your shoulder back a little. (Increase by {abs(diff_shoulder)}°)")
    elif diff_shoulder < -5:
        feedback.append(f"Bring your shoulder forward a little. (Decrease by {abs(diff_shoulder)}°)")
    else:
        feedback.append("Shoulder position looks good!")

    # Chest Angle: The torso should have a slight twist (~20°).
    diff_chest = ideal_angles[2] - current_angles[2]
    if diff_chest > 5:
        feedback.append(f"Twist your chest slightly more. (Increase by {abs(diff_chest)}°)")
    elif diff_chest < -5:
        feedback.append(f"Relax your chest twist. (Decrease by {abs(diff_chest)}°)")
    else:
        feedback.append("Chest positioning looks good!")

    # Torso Twist Angle: Keep the torso slightly rotated (~20°).
    diff_torso = ideal_angles[3] - current_angles[3]
    if diff_torso > 5:
        feedback.append(f"Twist your torso a bit more. (Increase by {abs(diff_torso)}°)")
    elif diff_torso < -5:
        feedback.append(f"Relax your torso twist. (Decrease by {abs(diff_torso)}°)")
    else:
        feedback.append("Torso twist looks good!")

    return feedback

def analyze_side_chest_pose(angles):
    """
    Processes side chest pose angles through the model and returns predictions.
    :param angles: List of 4 angles (e.g., [145, 165, 80, 90])
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
        pose_status = "Side Chest Pose is Correct" if pose_correctness_pred[0][0] > 0.79 else "Side Chest Pose is Incorrect"

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

