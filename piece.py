from config import *
import random

# Inherits the properties and features from Pygame Sprite Class
class Block(pygame.sprite.Sprite):
    def __init__(self, tetromino, position, color):
        # Instances
        self.tetromino = tetromino
        self.position = pygame.math.Vector2(position) + POSITION_OFFSET
        self.next_position = pygame.math.Vector2(position) + NEXT_POSITION_OFFSET if self.tetromino.count == 1 else pygame.math.Vector2(position) + (NEXT_POSITION_OFFSET + vector (0, 5)) if self.tetromino.count == 2 else pygame.math.Vector2(position) + (NEXT_POSITION_OFFSET + vector (0, 10)) if self.tetromino.count == 3 else None
        self.alive = True

        # Sprite group class - Pygame
        super().__init__(tetromino.tetris.sprite)
        self.image = pygame.Surface([TILE, TILE])
        pygame.draw.rect(self.image, color, (1, 1, TILE - 2, TILE - 2)) # FIX !???
        self.rect = self.image.get_rect()

    # Set the position of the block created
    def setRectPosition(self):
        position = [self.next_position, self.position][self.tetromino.current]
        self.rect.topleft = position * TILE

    def isAlive(self):
        if not self.alive:
            self.kill()

    # Rotates the blocks though the field --> A' = A - P | A'' = A'.rotate | A = A'' + P
    def rotate(self, _position, direction):
        aux = self.position - _position
        rotated = aux.rotate(90) if direction == 'right' else aux.rotate(-90) if direction == 'left' else None
        return rotated + _position
        
    # Collide between walls of the screen and ignores the initial tetromino piece falling
    def isCollide(self, position):
        x, y = int(position.x), int(position.y)
        if INITIAL_GRID <= x < END_GRID and y < HEIGHT and (y < 0 or not self.tetromino.tetris.array_field[y][x]):
            return False
        return True
    
    def update(self):
        self.isAlive()
        self.setRectPosition()

# Tetromino class behaviour
class Tetromino:
    bag = []

    def __init__(self, tetris, current = True, count = 0, landing = False):
        # Instances
        self.tetris = tetris
        self.current = current
        self.count = count
        self.landing = landing
        self.name = ''
        self.block = self.randomTetromino()

        self.initial_y_position = int(self.block[0].position.y / TILE)
        
    # Random bag of tetrominos
    def randomTetromino(self):
        if not Tetromino.bag:
            Tetromino.bag = list(TETROMINOES_SHAPE.keys())
            random.shuffle(Tetromino.bag)

        data = Tetromino.bag.pop()
        self.name = data
        return [Block(self, pos, TETROMINOES_COLOR[data]) for pos in TETROMINOES_SHAPE[data]]
    
    # Collide between blocks
    def isCollide(self, blocks_position):
        return any(map(Block.isCollide, self.block, blocks_position))
    
    # Rotate the tetromino
    def rotate(self, direction):
        # TODO: FIX !!!
        if self.name == 'O_SHAPE':
            return
        _position = self.block[0].position
        new_block_position = [block.rotate(_position, direction) for block in self.block]

        if not self.isCollide(new_block_position):
            for i, block in enumerate(self.block):
                block.position = new_block_position[i]

    # Tetromino movements
    def move(self, direction):
        move_direction = MOVEMENT[direction]
        new_block_position = [block.position + move_direction for block in self.block]
        
        # Moves the blocks to the new position --> Checks if one of the blocks has a collision at the new position
        if not self.isCollide(new_block_position):
            for block in self.block:
                block.position += move_direction
        elif direction == 'down':
            self.landing = True

    def position(self):
        return self.block[0].position
        #new_block_position = [block.rotate(_position, direction) for block in self.block]

    def update(self):
        self.move(direction = 'down')
        self.position()