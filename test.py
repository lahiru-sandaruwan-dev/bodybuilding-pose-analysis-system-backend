# import cv2
# import os
# import numpy as np
# import tensorflow as tf
# from tensorflow.keras.models import Model
# from tensorflow.keras.layers import Dense, Dropout, BatchNormalization, Input, LeakyReLU, Conv1D, Flatten
# from tensorflow.keras.optimizers import AdamW
# from tensorflow.keras.regularizers import l2
# from tensorflow.keras.callbacks import ReduceLROnPlateau
# from openpose import pyopenpose as op  # Ensure OpenPose is installed

# # === Step 1: Initialize OpenPose ===
# params = {"model_folder": "openpose/models/", "hand": False, "face": False}
# opWrapper = op.WrapperPython()
# opWrapper.configure(params)
# opWrapper.start()

# # === Step 2: Extract Keypoints from Images ===
# def extract_keypoints(image_path):
#     image = cv2.imread(image_path)
#     datum = op.Datum()
#     datum.cvInputData = image
#     opWrapper.emplaceAndPop([datum])
    
#     if datum.poseKeypoints is None:
#         return None  # No keypoints detected
    
#     return datum.poseKeypoints[0]  # Return first person keypoints

# # === Step 3: Preprocess Keypoints ===
# def preprocess_keypoints(keypoints):
#     # Select relevant keypoints (arms, elbows, shoulders)
#     indices = [2, 3, 4, 5, 6, 7]  # Adjust indices based on OpenPose's keypoint order
#     selected_keypoints = keypoints[indices, :2].flatten()  # Extract (x, y) positions
#     return selected_keypoints / 255.0  # Normalize values

# # === Step 4: Load and Process Dataset ===
# def load_dataset(image_folder, label_correct):
#     features, labels = [], []
#     for file in os.listdir(image_folder):
#         image_path = os.path.join(image_folder, file)
#         keypoints = extract_keypoints(image_path)
#         if keypoints is not None:
#             features.append(preprocess_keypoints(keypoints))
#             labels.append(label_correct)
    
#     return np.array(features), np.array(labels)

# # Load dataset
# correct_features, correct_labels = load_dataset("dataset/correct_poses", label_correct=1)
# incorrect_features, incorrect_labels = load_dataset("dataset/incorrect_poses", label_correct=0)

# # Combine dataset
# X = np.vstack((correct_features, incorrect_features))
# y = np.concatenate((correct_labels, incorrect_labels))

# # === Step 5: Define CNN Model ===
# input_layer = Input(shape=(X.shape[1], 1))  # CNN expects 1D input
# x = Conv1D(64, kernel_size=3, activation='relu', padding='same')(input_layer)
# x = BatchNormalization()(x)
# x = LeakyReLU(alpha=0.3)(x)
# x = Dropout(0.3)(x)

# x = Conv1D(128, kernel_size=3, activation='relu', padding='same')(x)
# x = BatchNormalization()(x)
# x = LeakyReLU(alpha=0.3)(x)
# x = Dropout(0.4)(x)

# x = Flatten()(x)
# x = Dense(64, activation='relu', kernel_regularizer=l2(0.001))(x)
# x = Dropout(0.4)(x)

# # Outputs
# pose_output = Dense(1, activation='sigmoid', name='pose_correctness')(x)
# injury_output = Dense(1, activation='sigmoid', name='injury_risk')(x)
# biceps_injury_output = Dense(1, activation='sigmoid', name='biceps_injury_risk')(x)
# triceps_injury_output = Dense(1, activation='sigmoid', name='triceps_injury_risk')(x)
# shoulders_injury_output = Dense(1, activation='sigmoid', name='shoulders_injury_risk')(x)

# # Compile Model
# model = Model(inputs=input_layer, outputs=[pose_output, injury_output, biceps_injury_output, triceps_injury_output, shoulders_injury_output])
# model.compile(optimizer=AdamW(learning_rate=0.001),
#               loss='binary_crossentropy',
#               metrics=['accuracy'])

# # === Step 6: Train Model ===
# X = X.reshape((X.shape[0], X.shape[1], 1))  # Reshape for CNN
# model.fit(X, {'pose_correctness': y, 'injury_risk': y, 'biceps_injury_risk': y, 'triceps_injury_risk': y, 'shoulders_injury_risk': y},
#           epochs=50, batch_size=32, validation_split=0.2, verbose=1)

# # Save Model
# model.save('front_double_biceps_openpose_model.h5')

# print("Model training complete and saved.")
