from config import *
from tetris import Tetris
from text import Text
import sys

# Main
class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Tetris')

        # Music
        pygame.mixer.music.load('assets/tetris_song.mp3')
        pygame.mixer.music.play(-1)  

        # Instances
        self.screen = pygame.display.set_mode(GAME_SCREEN)
        self.clock = pygame.time.Clock()
        self.timer()

        # Tetris class instance
        self.tetris = Tetris(self, GAME_SPEED)
        # Message class instance
        self.text = Text(self)

    # Set a timer for the animations movements
    def timer(self):
        # Custom events
        self.user_event = pygame.USEREVENT + 0
        self.hard_user_event = pygame.USEREVENT + 1
        self.soft_user_event = pygame.USEREVENT + 2

        # Animation triggers
        self.trigger = False
        self.hard_drop_trigger = False
        self.soft_drop_trigger = False

        # Set an event type to appear on the event queue every given number of milliseconds
        pygame.time.set_timer(self.user_event, GAME_SPEED)
        pygame.time.set_timer(self.hard_user_event, HARD_DROP_SPEED)
        pygame.time.set_timer(self.soft_user_event, SOFT_DROP_SPEED)

    # Game events
    def events(self):
        self.trigger = False
        self.hard_drop_trigger = False
        self.soft_drop_trigger = False

        for e in pygame.event.get():
            if e.type == pygame.QUIT or (e.type == pygame.KEYDOWN and e.type == pygame.K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif e.type == pygame.KEYDOWN:
                self.tetris.control(keyboard = e.key)
            elif e.type == pygame.KEYUP:
                self.tetris.controlUnhold(keyboard = e.key)

            # Animation triggers
            if e.type == self.user_event:
                self.trigger = True
            elif e.type == self.hard_user_event:
                self.hard_drop_trigger = True
            elif e.type == self.soft_user_event:
                self.soft_drop_trigger = True

    def update(self):
        self.tetris.update()
        self.clock.tick(FPS) # Frame rate

    def draw(self):
        self.screen.fill(color = MAIN_COLOR)
        self.tetris.draw()
        self.text.draw()
        pygame.display.flip() # Updates the entire display

    def run(self):
        while True:
            self.events()
            self.update()
            self.draw()

# Starts the game
if __name__ == '__main__':
    app = App()
    app.run()