import pygame
import sys
from typing import *

pygame.display.init()
pygame.font.init()

#=====================================================
#text rendering
#=====================================================
def render_text(text:str, position:tuple, size:int = 50, color:str|tuple = "#000000", font:pygame.font.Font = pygame.font.SysFont("Arial", 16), Bold = False, Italic = False, Underline = False, Draw = True) -> pygame.Surface:
    """Render text using the specified font and color."""

    #get the screen
    screen = pygame.display.get_surface()

    #convert color if it's a string
    if isinstance(color, str):
        color = pygame.Color(color)

    #set font styles
    font.set_bold(Bold)
    font.set_italic(Italic)
    font.set_underline(Underline)

    #render the text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)

    #draw the text on the screen if required
    if Draw: screen.blit(text_surface, text_rect)

    #return the text surface and its rectangle
    return text_surface, text_rect



#=====================================================
#Loading/Saving Files
#=====================================================

def load_image(path):
    """Load an image from the specified path."""
    try:
        image = pygame.image.load(path)
        return image.convert_alpha()
    except pygame.error as e:
        print(f"Unable to load image at {path}: {e}")
        sys.exit(1)

def load_font(path, size):
    """Load a font from the specified path with the given size."""
    try:
        font = pygame.font.Font(path, size)
        return font
    except IOError as e:
        print(f"Unable to load font at {path}: {e}")
        sys.exit(1)