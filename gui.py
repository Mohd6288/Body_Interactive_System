import tkinter as tk
import threading


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Particle System Control")

        # Default parameters
        self.friction = 0.95
        self.max_speed = 5
        self.interaction_radius = 100

        # Create sliders
        self._create_slider("Friction", 0.8, 1.0, self.friction, lambda v: self._set_param("friction", v))
        self._create_slider("Max Speed", 1, 10, self.max_speed, lambda v: self._set_param("max_speed", v))
        self._create_slider("Interaction Radius", 50, 200, self.interaction_radius, lambda v: self._set_param("interaction_radius", v))

        self.lock = threading.Lock()

    def _create_slider(self, label, min_val, max_val, default, command):
        frame = tk.Frame(self.root)
        frame.pack(pady=5)
        tk.Label(frame, text=label).pack(side=tk.LEFT, padx=10)
        slider = tk.Scale(frame, from_=min_val, to=max_val, resolution=0.01 if isinstance(min_val, float) else 1,
                          orient=tk.HORIZONTAL, command=command)
        slider.set(default)
        slider.pack(side=tk.LEFT)

    def _set_param(self, param, value):
        with self.lock:
            setattr(self, param, float(value))

    def get_params(self):
        with self.lock:
            return self.friction, self.max_speed, self.interaction_radius

    def start(self):
        self.root.mainloop()
