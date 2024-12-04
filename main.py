import cv2
import numpy as np
import pathlib
import threading
from particle_system import ParticleSystem
from pose_detection import PoseDetector
from utils import scale_landmarks, download_model
from gui import GUI


def run_particle_system(gui):
    # Paths and parameters
    model_path = pathlib.Path("pose_landmarker.task")
    canvas_width, canvas_height = 1280, 720
    num_particles = 500

    # Check and download the pose model if necessary
    if not model_path.exists():
        print("Model file not found. Downloading...")
        download_model(model_path)

    # Initialize pose detector
    pose_detector = PoseDetector(model_path)

    # Initialize particle system
    particle_system = ParticleSystem(num_particles, canvas_width, canvas_height, (255, 255, 255))

    # Initialize video capture
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
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

            # Flip and prepare the frame
            frame = cv2.flip(frame, 1)
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect pose landmarks
            landmarks = pose_detector.detect(rgb_frame)

            # Scale landmarks to match the canvas size
            scaled_landmarks = scale_landmarks(landmarks, canvas_width, canvas_height)

            # Clear the canvas
            canvas.fill(0)

            # Draw body landmarks
            for x, y in scaled_landmarks:
                cv2.circle(canvas, (x, y), 5, (0, 255, 0), -1)

            # Get parameters from the GUI
            friction, max_speed, interaction_radius = gui.get_params()

            # Update particle system
            particle_system.update(canvas, scaled_landmarks, friction, max_speed, interaction_radius)

            # Show the canvas
            cv2.imshow("Particle System with Landmarks", canvas)

            # Quit on pressing 'q'
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break
    except Exception as e:
        print(f"Error in particle system thread: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()


def main():
    # Initialize GUI
    gui = GUI()

    # Run the particle system in a separate thread
    particle_thread = threading.Thread(target=run_particle_system, args=(gui,))
    particle_thread.daemon = True
    particle_thread.start()

    # Start the GUI in the main thread
    gui.start()


if __name__ == "__main__":
    main()
