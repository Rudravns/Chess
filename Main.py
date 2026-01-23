import pygame
import sys,os
from Helper import *
from Data_types import *
import Pieces


class App:
    def __init__(self):
        pygame.init()
        pygame.display.init()
        pygame.font.init()


        self.last_width, self.last_height = 1000, 600
        self.screen = pygame.display.set_mode((self.last_width, self.last_height), pygame.RESIZABLE)
        pygame.display.set_caption("Chess")
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        

        self.clock = pygame.time.Clock()
        self.tick = 120  # FPS
        self.dt = 0.0

    def run(self):
        while True:
            self.dt = self.clock.tick(self.tick) / 1000
            self.screen.fill((0, 0, 0))

            # drawing
            self.draw_board(white_square_color=LIGHT_BROWN, black_square_color=DARK_BROWN)

            # text
            render_text(
                text=f"FPS: {round(self.clock.get_fps())}",
                position=(10, 10),
                size=36,
                color=(255, 255, 255)
            )

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    self.last_width, self.last_height = event.w, event.h
                    #self.screen = pygame.display.set_mode((self.last_width, self.last_height), pygame.RESIZABLE)
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_F11:
                       self.screen = pygame.display.set_mode(
                           get_fullscreen() if self.screen.get_size() != get_fullscreen() else (self.last_width, self.last_height),  
                           pygame.RESIZABLE)



            pygame.display.flip()

      
    def draw_board(self, white_square_color: ColorType, black_square_color: ColorType):
        h, w = self.screen.get_size()
        square_h = h // 8
        square_w = w // 8
        square_size = min(square_h, square_w)


        for row in range(8):
            for col in range(8):
                color = white_square_color if (row + col) % 2 == 0 else black_square_color
                pygame.draw.rect(
                    self.screen,
                    pygame.Color(color),
                    (col * square_size, row * square_size, square_size, square_size)
                )


if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    app = App()
    app.run()
