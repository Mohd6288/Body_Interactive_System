import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python import BaseOptions


class PoseDetector:
    def __init__(self, model_path):
        base_options = BaseOptions(model_asset_path=str(model_path))
        options = vision.PoseLandmarkerOptions(
            base_options=base_options, output_segmentation_masks=False
        )
        self.detector = vision.PoseLandmarker.create_from_options(options)

    def detect(self, frame):
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        detection_result = self.detector.detect(mp_image)

        # Extract landmark positions (normalized)
        landmarks = []
        if detection_result.pose_landmarks:
            for lm in detection_result.pose_landmarks[0]:
                landmarks.append((lm.x, lm.y))
        return landmarks
