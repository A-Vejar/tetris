import pygame

vector = pygame.math.Vector2

# Game Settings
FPS = 60
GAME_SPEED = 600
HARD_DROP_SPEED = 15
SOFT_DROP_SPEED = GAME_SPEED // 2
MAIN_COLOR = '#0A0A0A'
GRID_COLOR = '#7f7f7f'
TEXT_COLOR = '#ffffff'
GAME_OVER_COLOR_MESSAGE = '#8B0000'

# Windows Size Settings
WIDTH = 26
HEIGHT = 20
TILE = 30
GAME_SCREEN = [WIDTH * TILE, HEIGHT * TILE]
INITIAL_GRID = (WIDTH // 2) - 5
END_GRID = (WIDTH // 2) + 5

# Tetromino Pieces Settings
TETROMINOES_DISPLAY = 3
POSITION_OFFSET = vector(WIDTH // 2 - 1, 0)
NEXT_POSITION_OFFSET = vector((WIDTH + END_GRID) // 2, (HEIGHT // 2) - 6)

MOVEMENT = {
    'left': vector(-1,0),
    'right': vector(1,0),
    'down': vector(0,1)
}
TETROMINOES_SHAPE = {
    'I_SHAPE': [(0, 0), (0, 1), (0, -1), (0, -2)],
    'J_SHAPE': [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L_SHAPE': [(0, 0), (1, 0), (0, -1), (0, -2)],
    'O_SHAPE': [(0, 0), (0, -1), (1, 0), (1, -1)],
    'S_SHAPE': [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z_SHAPE': [(0, 0), (1, 0), (0, -1), (-1, -1)],
    'T_SHAPE': [(0, 0), (-1, 0), (1, 0), (0, -1)]
}
TETROMINOES_COLOR = {
    'I_SHAPE': '#00ffff',
    'J_SHAPE': '#0000ff',
    'L_SHAPE': '#ff7f00',
    'O_SHAPE': '#ffff00',
    'S_SHAPE': '#00ff00',
    'Z_SHAPE': '#ff0000',
    'T_SHAPE': '#800080'
}