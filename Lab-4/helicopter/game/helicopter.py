"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.4
MAX_SPEED = 6.0
DRAG = 0.8


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0

    def handle_input(self, keys_pressed):
        direction = int(keys_pressed[pygame.K_DOWN]) - int(keys_pressed[pygame.K_UP])
        if direction:
            # Discard old momentum when the player reverses direction.
            if self.vy * direction < 0:
                self.vy = 0.0
            self.vy += direction * THRUST
            self.vy = max(-MAX_SPEED, min(MAX_SPEED, self.vy))
        else:
            self.vy *= DRAG
            if abs(self.vy) < 0.05:
                self.vy = 0.0

    def update(self, height_bound):
        self.y += self.vy
        half_height = self.height / 2
        if self.y < half_height:
            self.y = half_height
            self.vy = 0
        elif self.y > height_bound - half_height:
            self.y = height_bound - half_height
            self.vy = 0

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
