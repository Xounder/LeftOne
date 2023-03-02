import pygame, sys
from settings import screen_width, screen_height
from table_game import TableGame

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('LeftOne')
        self.clock = pygame.time.Clock()

        self.table_game = TableGame()
    
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.table_game.draw()
            self.table_game.update()
            
            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()