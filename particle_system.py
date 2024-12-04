import random
import numpy as np
import cv2


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-2, 2)
        self.vy = random.uniform(-2, 2)
        self.ax = 0
        self.ay = 0
        self.size = random.randint(2, 5)
        self.color = color

    def move(self, width, height, friction, max_speed):
        # Update velocity with acceleration
        self.vx += self.ax
        self.vy += self.ay

        # Apply friction
        self.vx *= friction
        self.vy *= friction

        # Limit velocity to max speed
        speed = np.sqrt(self.vx**2 + self.vy**2)
        if speed > max_speed:
            self.vx = (self.vx / speed) * max_speed
            self.vy = (self.vy / speed) * max_speed

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Bounce off edges
        if self.x < 0 or self.x > width:
            self.vx *= -1
        if self.y < 0 or self.y > height:
            self.vy *= -1

        # Reset acceleration
        self.ax = 0
        self.ay = 0

    def draw(self, canvas):
        cv2.circle(canvas, (int(self.x), int(self.y)), self.size, self.color, -1)

    def interact(self, landmarks, interaction_radius):
        for landmark in landmarks:
            # Calculate interaction force
            dx = landmark[0] - self.x
            dy = landmark[1] - self.y
            dist = np.sqrt(dx**2 + dy**2)

            if dist < interaction_radius:  # Interaction radius
                force = (interaction_radius - dist) / interaction_radius
                self.ax += force * dx / dist
                self.ay += force * dy / dist


class ParticleSystem:
    def __init__(self, num_particles, width, height, color):
        self.particles = [
            Particle(random.randint(0, width), random.randint(0, height), color)
            for _ in range(num_particles)
        ]

    def update(self, canvas, landmarks, friction, max_speed, interaction_radius):
        for particle in self.particles:
            particle.interact(landmarks, interaction_radius)
            particle.move(canvas.shape[1], canvas.shape[0], friction, max_speed)
            particle.draw(canvas)
