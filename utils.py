import urllib.request


def download_model(model_path):
    url = "https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_heavy/float16/latest/pose_landmarker_heavy.task"
    print(f"Downloading model from {url}...")
    urllib.request.urlretrieve(url, model_path)
    print(f"Model downloaded and saved as {model_path}")


def scale_landmarks(landmarks, width, height):
    return [(int(lm[0] * width), int(lm[1] * height)) for lm in landmarks]
