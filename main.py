import cv2
import numpy as np
import pathlib
from particle_system import ParticleSystem
from pose_detection import PoseDetector
from utils import scale_landmarks, download_model


def main():
    # Paths and parameters
    model_path = pathlib.Path("pose_landmarker.task")
    canvas_width, canvas_height = 1280, 720
    num_particles = 500  # Reduce for better performance

    # Check and download model if necessary
    if not model_path.exists():
        print("Model file not found. Downloading...")
        download_model(model_path)

    # Initialize pose detector
    pose_detector = PoseDetector(model_path)

    # Initialize particle system
    particle_system = ParticleSystem(num_particles, canvas_width, canvas_height)

    # Initialize video capture and canvas
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Cannot access webcam.")
        return
    canvas = np.zeros((canvas_height, canvas_width, 3), dtype=np.uint8)

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Flip and prepare frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect pose landmarks
            landmarks = pose_detector.detect(rgb_frame)

            # Scale landmarks to canvas size
            scaled_landmarks = scale_landmarks(landmarks, canvas_width, canvas_height)

            # Clear canvas
            canvas.fill(0)

            # Draw body landmarks
            for x, y in scaled_landmarks:
                cv2.circle(canvas, (x, y), 5, (0, 255, 0), -1)  # Green dots for landmarks

            # Update and draw particles
            particle_system.update(canvas, scaled_landmarks, canvas_width, canvas_height)

            # Show visualization
            cv2.imshow("Particle System with Landmarks", canvas)

            # Quit on 'q'
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
