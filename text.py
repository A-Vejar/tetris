from config import *

class Text:
    def __init__(self, app):
        self.app = app
        
    def titleRight(self):
        font = pygame.font.Font(None, 30)
        title = font.render('Next Tetrominoes', True, TEXT_COLOR)
        self.app.screen.blit(title, NEXT_POSITION_OFFSET + vector(550, 10))

    def titleLeft(self):
        font = pygame.font.Font(None, 30)
        level = font.render(f"Level: { self.app.tetris.level }", True, TEXT_COLOR)
        lines = font.render(f"Lines: { self.app.tetris.count_lines }", True, TEXT_COLOR)
        score = font.render(f"Score: { self.app.tetris.score }", True, TEXT_COLOR)
        max_score = font.render(f"Max Score: { self.app.tetris.max_score }", True, TEXT_COLOR)

        self.app.screen.blit(level, NEXT_POSITION_OFFSET + vector(0, 10))
        self.app.screen.blit(lines, NEXT_POSITION_OFFSET + vector(0, 50))
        self.app.screen.blit(score, NEXT_POSITION_OFFSET + vector(0, 90))
        self.app.screen.blit(max_score, NEXT_POSITION_OFFSET + vector(0, 130))

    def draw(self):
        self.titleLeft()
        self.titleRight()