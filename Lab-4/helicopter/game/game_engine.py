"""
GameEngine: manages movement, collisions, distance, shield and restart.
"""

import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3
PIXELS_PER_METRE = 10


class GameEngine:
    def __init__(self):
        self.helicopter = Helicopter(x=100, y=HEIGHT / 2)
        self.obstacles = []
        self.frames_until_spawn = 0
        self.game_over = False
        self.distance = 0.0
        self.shield_active = False
        self.shielded_obstacle = None

    def _spawn_obstacle(self):
        margin = 60
        gap_y = random.randint(margin + GAP_HEIGHT // 2, HEIGHT - margin - GAP_HEIGHT // 2)
        self.obstacles.append(Obstacle(
            x=WIDTH, gap_y=gap_y, gap_height=GAP_HEIGHT,
            wall_width=WALL_WIDTH, screen_height=HEIGHT, speed=SCROLL_SPEED,
        ))

    def handle_input(self, keys_pressed):
        if not self.game_over:
            self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        if self.game_over and key == pygame.K_r:
            self.__init__()
        elif not self.game_over and key == pygame.K_SPACE:
            self.shield_active = True

    def update(self):
        if self.game_over:
            return
        self.helicopter.update(HEIGHT)
        self.distance += SCROLL_SPEED / PIXELS_PER_METRE

        self.frames_until_spawn -= 1
        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        for obstacle in self.obstacles:
            obstacle.update()
        self.obstacles = [o for o in self.obstacles if not o.is_off_screen()]

        helicopter_rect = self.helicopter.get_rect()
        # Ignore only the ongoing contact that consumed the shield.
        # Leaving the wall (including entering its gap) ends that contact.
        if self.shielded_obstacle is not None:
            if not (helicopter_rect.colliderect(self.shielded_obstacle.get_top_rect()) or
                    helicopter_rect.colliderect(self.shielded_obstacle.get_bottom_rect())):
                self.shielded_obstacle = None
        for obstacle in self.obstacles:
            if obstacle is self.shielded_obstacle:
                continue
            if (helicopter_rect.colliderect(obstacle.get_top_rect()) or
                    helicopter_rect.colliderect(obstacle.get_bottom_rect())):
                if self.shield_active:
                    self.shield_active = False
                    self.shielded_obstacle = obstacle
                else:
                    self.game_over = True
                    break

    def draw(self, surface, font):
        from game import renderer
        renderer.draw_scene(surface, self.helicopter, self.obstacles, self.shield_active)
        renderer.draw_text(surface, font, 'Up/Down: fly   Space: shield   R: restart', (12, 12))
        renderer.draw_text(surface, font, f'Distance: {self.distance:.1f} m', (12, 42))
        status = 'ACTIVE - one hit' if self.shield_active else 'OFF - Space to activate'
        renderer.draw_text(surface, font, f'Shield: {status}', (12, 72))
        if self.game_over:
            renderer.draw_banner(surface, font, f'GAME OVER | {self.distance:.1f} m | R: restart')
