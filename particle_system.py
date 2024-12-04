import random
import numpy as np
import cv2


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.size = random.randint(2, 4)  # Smaller particles
        self.color = (200, 200, 200)  # Light gray

    def move(self, width, height):
        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x < 0 or self.x > width:
            self.vx *= -1
        if self.y < 0 or self.y > height:
            self.vy *= -1

    def draw(self, canvas):
        cv2.circle(canvas, (int(self.x), int(self.y)), self.size, self.color, -1)

    def interact(self, landmarks):
        for landmark in landmarks:
            # Move towards the landmark
            dx = landmark[0] - self.x
            dy = landmark[1] - self.y
            dist = np.sqrt(dx**2 + dy**2)

            if dist < 100:  # Interaction radius
                self.vx += dx / dist * 0.5
                self.vy += dy / dist * 0.5


class ParticleSystem:
    def __init__(self, num_particles, width, height):
        self.particles = np.array(
            [
                Particle(random.randint(0, width), random.randint(0, height))
                for _ in range(num_particles)
            ]
        )

    def update(self, canvas, landmarks, width, height):
        for particle in self.particles:
            particle.move(width, height)
            particle.draw(canvas)
            particle.interact(landmarks)
