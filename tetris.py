from config import *
from piece import Tetromino

# Speed Game
def speedGame(nivel, game_speed):
    speed = (0.8 - ((nivel - 1) * 0.007))**(nivel - 1)
    return int(speed * game_speed)

# TODO: Refactor class
class Tetris:
    MAX_SCORE = 0
    count = 0

    def __init__(self, app, game_speed):
        # Instances
        self.app = app
        self.sprite = pygame.sprite.Group() # Sprite objects container
        self.array_field = self.field()
        self.hard_drop = False
        self.soft_drop = False

        # Score
        self.level = 1
        self.lines = 0
        self.count_lines = 0
        self.score = 0
        self.max_score = 0
        self.combo = 0
        self.clear_points = { 0: 0, 1: 100, 2: 300 , 3: 500, 4: 800 }
        self.perfect_clear_points = { 0: 0, 1: 800, 2: 1200, 3: 1800, 4: 2000 }

        # Speed
        self.time_speed = speedGame(self.level, game_speed)

        # Tetromino class instance
        self.tetromino = Tetromino(self)
        self.next_tetromino = self.nextTetrominoes() if Tetris.count == 0 else None

    # Tetrominoes
    def nextTetrominoes(self):
        tetrominoes = []
        for i in range(1, (TETROMINOES_DISPLAY + 1)):
            Tetris.count = i
            data = Tetromino(self, current = False, count = i)
            tetrominoes.append(data)

        return tetrominoes

    # Game controller for the hold key-down button
    def controlUnhold(self, keyboard):
        if keyboard == pygame.K_DOWN:
            self.soft_drop = False
        
    # Game controllers
    def control(self, keyboard):
        if keyboard == pygame.K_LEFT:
            self.tetromino.move(direction = 'left')
        elif keyboard == pygame.K_RIGHT:
            self.tetromino.move(direction = 'right')
        elif keyboard == pygame.K_UP:
            self.tetromino.rotate(direction = 'right')
        elif keyboard == pygame.K_LCTRL or keyboard == pygame.K_z:
            self.tetromino.rotate(direction = 'left')
        elif keyboard == pygame.K_SPACE:
            self.hard_drop = True
        elif keyboard == pygame.K_DOWN:
            self.soft_drop = True

    # Get score
    def dropCountLines(self):
        position = 0
        if not self.hard_drop:
            position = self.tetromino.block[0].position.y
        return position
    
    # Get score
    def getHardDropScore(self):
        if self.hard_drop:
            self.score += 2 * (self.tetromino.block[0].position.y - self.dropCountLines())
    
    # Get score
    def getClearScore(self):
        if self.count_lines >= 10:
            self.level += 1
            self.count_lines -= 10

        self.count_lines += self.lines
        self.score += (self.clear_points[self.lines] * self.level)
        self.lines = 0

    # Get score
    def getPerfectClearScore(self):
        if self.count_lines >= 10:
            self.level += 1
            self.count_lines -= 10

        self.count_lines += self.lines
        self.score += (self.perfect_clear_points[self.lines] * self.level)
        self.lines = 0

    # Game over
    def endGame(self):
        if self.tetromino.block[0].position.y == POSITION_OFFSET[1]:
            pygame.time.wait(250)
            return True
        
    # TODO: Needs Changes
    def showGameOverMessage(self):
        font = pygame.font.Font(None, 74)
        game_over_text = font.render('Game Over', True, GAME_OVER_COLOR_MESSAGE)
        text_rect = game_over_text.get_rect(center=(WIDTH * TILE // 2, HEIGHT * TILE // 2))
        self.app.screen.blit(game_over_text, text_rect)

        # Continue button
        continue_text = font.render('To continue press r', True, TEXT_COLOR)
        continue_rect = continue_text.get_rect(center=(WIDTH * TILE // 2, HEIGHT * TILE // 2 + 50))
        self.app.screen.blit(continue_text, continue_rect)

        pygame.display.flip()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.__init__(self.app, GAME_SPEED)
                        waiting_for_input = False

    # Clear lines
    def clearLines(self):
        row = HEIGHT - 1
        for j in range(HEIGHT - 1, -1, -1):
            for i in range(INITIAL_GRID, END_GRID):
                self.array_field[row][i] = self.array_field[j][i]

                if self.array_field[j][i]:
                    self.array_field[row][i].position = vector(i, j)

            # Checks if the row line is full
            if sum(map(bool, self.array_field[j])) < (END_GRID - INITIAL_GRID):
                row -= 1
                # Reset the combo
                if self.combo <= -1:
                    self.combo = 0
                else:
                    self.combo -= 1
            else:
                for i in range(INITIAL_GRID, END_GRID):
                    self.array_field[row][i].alive = False
                    self.array_field[row][i] = 0

                # Score
                self.lines += 1
                self.combo += 1
                self.score += (50 * self.combo * self.level)

        if all(all(element == 0 for element in row) for row in self.array_field) and self.lines > 0:
            self.getPerfectClearScore()

    # Handles the movements of the tetrominos through the field --> Stores the landing position of the tetrominos / Calculates the collisions
    def landingFieldPosition(self):
        for block in self.tetromino.block:
            x, y = int(block.position.x), int(block.position.y)
            self.array_field[y][x] = block

    # Game field array (2D) --> Set the initial game field position
    def field(self):
        return [[0 for i in range(WIDTH)] for j in range(HEIGHT)]

    # Landing behaviour (When a piece lands, its creates a new instance)
    def landing(self):
        if self.tetromino.landing:
            if self.endGame():
                Tetris.MAX_SCORE = max(self.score, Tetris.MAX_SCORE)
                
                # End game
                self.showGameOverMessage()

                # Resume music
                pygame.mixer.music.unpause()
                self.max_score = Tetris.MAX_SCORE
                self.next_tetromino = self.nextTetrominoes()

            else:
                if Tetris.count == 0:
                    self.next_tetromino = self.nextTetrominoes()

                self.getHardDropScore()
                self.hard_drop = False
                self.landingFieldPosition()
                self.next_tetromino[Tetris.count-1].current = True
                self.tetromino = self.next_tetromino[Tetris.count-1]
                Tetris.count -= 1
    
    # Render
    def grids(self):
        for i in range(INITIAL_GRID, END_GRID):
            for j in range(HEIGHT):
                pygame.draw.rect(self.app.screen, GRID_COLOR, (i * TILE, j * TILE, TILE, TILE), 1)

    def update(self):
        # Access to the "trigger list" by using the index next to it.
        trigger = [self.app.trigger, self.app.hard_drop_trigger][self.hard_drop]
        if trigger:
            self.clearLines()
            self.tetromino.update()
            self.landing()
            self.getClearScore()
        
        if self.soft_drop:
            self.tetromino.update()
            self.score += 1
        
        self.sprite.update()
        self.dropCountLines()

    def draw(self):
        self.grids()
        self.sprite.draw(self.app.screen)