import numpy as np
import tensorflow as tf
from tensorflow.keras.losses import MeanSquaredError

# Load the trained model with custom objects
model = tf.keras.models.load_model('app/models/side_chest_pose_model.h5', custom_objects={'mse': MeanSquaredError()})

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

        # Set injury risk thresholds
        injury_status_biceps = "High Risk of Injury" if biceps_injury_pred[0][0] > 0.2 else "Low Risk of Injury"
        injury_status_triceps = "High Risk of Injury" if triceps_injury_pred[0][0] > 0.25 else "Low Risk of Injury"
        injury_status_shoulders = "High Risk of Injury" if shoulders_injury_pred[0][0] > 0.2 else "Low Risk of Injury"

        # Prepare response data
        data = {
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
            "predicted_muscle_imbalance": predicted_muscle_imbalance[0].tolist()
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
