"""Record real Pygame-rendered gameplay with reproducible scripted inputs."""
import os
os.environ.setdefault('SDL_VIDEODRIVER', 'dummy')
os.environ.setdefault('SDL_AUDIODRIVER', 'dummy')
import sys
import random
import subprocess
from pathlib import Path
import pygame

source, output, mode = sys.argv[1:]
sys.path.insert(0, str(Path(source).resolve()))
from game.game_engine import GameEngine
from game.renderer import WINDOW_SIZE

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)
font = pygame.font.SysFont('consolas', 22)
label_font = pygame.font.SysFont('consolas', 16)
random.seed(1)
engine = GameEngine()
encoder = subprocess.Popen([
    'ffmpeg', '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pixel_format',
    'rgb24', '-video_size', '700x500', '-framerate', '60', '-i', '-',
    '-an', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', output
], stdin=subprocess.PIPE)
for frame in range(600):
    pygame.event.pump()
    if mode == 'before':
        up = 260 <= frame < 375
        down = frame >= 375
        description = ('Walls have no collision' if frame < 260 else
                       'Hold Up, then reverse to Down' if frame < 450 else
                       'Missing bottom boundary')
    else:
        down = frame < 90 or 170 <= frame < 320
        up = 90 <= frame < 170
        if frame == 175:
            engine.handle_keydown(pygame.K_SPACE)
        if frame == 360:
            engine.handle_keydown(pygame.K_r)
        description = ('Movement and full-body boundaries' if frame < 175 else
                       'Shield absorbs first wall; next wall ends game' if frame < 360 else
                       'R restarts with distance zero')
    engine.handle_input({pygame.K_UP: up, pygame.K_DOWN: down})
    engine.update()
    engine.draw(screen, font)
    pygame.draw.rect(screen, (245, 245, 245), (0, 462, 700, 38))
    screen.blit(label_font.render(mode.upper() + ' | Scripted gameplay capture', True, (20, 20, 20)), (10, 464))
    screen.blit(label_font.render(description, True, (20, 20, 20)), (10, 482))
    pygame.display.flip()
    encoder.stdin.write(pygame.image.tobytes(screen, 'RGB'))
encoder.stdin.close()
if encoder.wait() != 0:
    raise RuntimeError('Video encoding failed')
pygame.quit()
