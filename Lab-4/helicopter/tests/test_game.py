import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import unittest
import pygame
from game.helicopter import Helicopter, MAX_SPEED
from game.game_engine import GameEngine, SCROLL_SPEED, PIXELS_PER_METRE
from game.obstacle import Obstacle
from game.renderer import HEIGHT, WINDOW_SIZE


class GameTests(unittest.TestCase):
    def setUp(self):
        self.engine = GameEngine()
        self.engine.frames_until_spawn = 1000

    def wall(self, x=90, gap_y=150):
        return Obstacle(x, gap_y, 150, 60, HEIGHT, SCROLL_SPEED)

    def test_speed_cap_and_immediate_reversal(self):
        heli = self.engine.helicopter
        for _ in range(200):
            heli.handle_input({pygame.K_UP: True, pygame.K_DOWN: False})
        self.assertEqual(heli.vy, -MAX_SPEED)
        heli.handle_input({pygame.K_UP: False, pygame.K_DOWN: True})
        self.assertGreater(heli.vy, 0)
        for _ in range(200):
            heli.handle_input({pygame.K_UP: False, pygame.K_DOWN: True})
        self.assertEqual(heli.vy, MAX_SPEED)
        heli.handle_input({pygame.K_UP: True, pygame.K_DOWN: False})
        self.assertLess(heli.vy, 0)

    def test_full_body_boundaries(self):
        heli = self.engine.helicopter
        for direction in (-1, 1):
            for _ in range(1000):
                heli.vy = direction * MAX_SPEED
                heli.update(HEIGHT)
                self.assertGreaterEqual(heli.get_rect().top, 0)
                self.assertLessEqual(heli.get_rect().bottom, HEIGHT)
            self.assertEqual(heli.vy, 0)

    def test_release_and_simultaneous_keys_brake(self):
        heli = self.engine.helicopter
        heli.vy = MAX_SPEED
        for _ in range(100):
            heli.handle_input({pygame.K_UP: False, pygame.K_DOWN: False})
        self.assertEqual(heli.vy, 0)
        heli.vy = MAX_SPEED
        heli.handle_input({pygame.K_UP: True, pygame.K_DOWN: True})
        self.assertLess(heli.vy, MAX_SPEED)

    def test_both_walls_cause_game_over(self):
        for y in (50, 400):
            self.setUp()
            self.engine.helicopter.y = y
            self.engine.obstacles = [self.wall()]
            self.engine.update()
            self.assertTrue(self.engine.game_over)

    def test_entire_gap_is_safe(self):
        # Include positions flush with the two gap edges.
        for y in range(87, 214):
            self.setUp()
            self.engine.helicopter.y = y
            self.engine.obstacles = [self.wall()]
            self.engine.update()
            self.assertFalse(self.engine.game_over, y)

    def test_score_increases_and_freezes(self):
        for _ in range(60):
            self.engine.update()
        self.assertAlmostEqual(self.engine.distance, 60 * SCROLL_SPEED / PIXELS_PER_METRE)
        self.engine.obstacles = [self.wall()]
        self.engine.update()
        self.assertTrue(self.engine.game_over)
        snapshot = (self.engine.distance, self.engine.helicopter.y, self.engine.obstacles[0].x)
        self.engine.handle_input({pygame.K_UP: True, pygame.K_DOWN: False})
        self.engine.update()
        self.assertEqual(snapshot, (self.engine.distance, self.engine.helicopter.y, self.engine.obstacles[0].x))

    def test_restart_clears_every_state(self):
        self.engine.obstacles = [self.wall()]
        self.engine.update()
        self.engine.handle_keydown(pygame.K_r)
        self.assertFalse(self.engine.game_over)
        self.assertEqual(self.engine.distance, 0)
        self.assertEqual(self.engine.obstacles, [])
        self.assertEqual(self.engine.helicopter.y, HEIGHT / 2)
        self.assertFalse(self.engine.shield_active)
        self.assertIsNone(self.engine.shielded_obstacle)

    def test_shield_consumes_one_continuous_hit(self):
        first = self.wall()
        self.engine.obstacles = [first]
        self.engine.handle_keydown(pygame.K_SPACE)
        self.assertTrue(self.engine.shield_active)
        self.engine.update()
        self.assertFalse(self.engine.shield_active)
        self.assertFalse(self.engine.game_over)
        for _ in range(3):
            self.engine.update()
            self.assertFalse(self.engine.game_over)
        self.engine.obstacles.append(self.wall())
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_shield_reactivation_and_overlap_end(self):
        first = self.wall()
        self.engine.obstacles = [first]
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        first.x = -100
        self.engine.update()
        self.assertIsNone(self.engine.shielded_obstacle)
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.obstacles = [self.wall()]
        self.engine.update()
        self.assertFalse(self.engine.game_over)
        self.assertFalse(self.engine.shield_active)

    def test_two_simultaneous_walls_exhaust_shield(self):
        self.engine.obstacles = [self.wall(), self.wall()]
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.update()
        self.assertTrue(self.engine.game_over)

    def test_render_running_shield_and_game_over(self):
        pygame.init()
        surface = pygame.Surface(WINDOW_SIZE)
        font = pygame.font.SysFont('consolas', 22)
        self.engine.draw(surface, font)
        self.engine.handle_keydown(pygame.K_SPACE)
        self.engine.draw(surface, font)
        self.engine.game_over = True
        self.engine.draw(surface, font)
        pygame.quit()


if __name__ == '__main__':
    unittest.main()
