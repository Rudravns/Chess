import pygame
import sys, os, random
from Helper import render_text, load_image

class App:    
    def __init__(self):

        # Initialize Pygame and set up the window
        pygame.init()
        self.last_width, self.last_height = 800, 600
        self.screen = pygame.display.set_mode((self.last_width, self.last_height))
        pygame.display.set_caption("Chess")

    
        # Set up the clock for managing the frame rate
        self.clock = pygame.time.Clock()
        self.Tick = 120 #FPS
        self.dt = 0

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))  # Clear screen with black
            self.dt = self.clock.tick(self.Tick)/1000  # Delta time in seconds

            #drawing
            self.draw_board("#d2bef6","#35009e")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            #draw text
            render_text(self.screen, "Chess Game", 36, (255, 255, 255), (10, 10))
            
            pygame.display.flip()
            
    def draw_board(self, White_square_color = "#ffffff", Black_square_color = "#000000"):
        h, w = self.screen.get_size()

        square_size = min(h, w) // 8
        for row in range(8):
            for col in range(8):
                color = White_square_color if (row + col) % 2 == 0 else Black_square_color
                pygame.draw.rect(self.screen, pygame.Color(color), 
                                 (col * square_size, row * square_size, square_size, square_size))






if __name__ == "__main__":
    Window = App()
    Window.run()