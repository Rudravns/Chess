import os
import pygame
from typing import * # pyright: ignore[reportWildcardImportFromLibrary]
from Data_types import *


pygame.init()
pygame.display.init()
pygame.font.init()

#====================================================
# Screen Funcs
#====================================================
def get_fullscreen() -> Size:
    """Get the current fullscreen resolution."""
    return FULLSCREEN

@overload
def scale(value: int | float, *, round_values: bool = False) -> int | float: ...

@overload
def scale(
    value: tuple[int | float, ...],
    *,
    round_values: bool = False
) -> tuple[int | float, ...]: ...


def scale(
    value: int | float | tuple[int | float, ...],
    *,
    round_values: bool = False
) -> int | float | tuple[int | float, ...]:
    """Scale a value or tuple of values based on the current fullscreen resolution."""
    screen_w, screen_h = get_fullscreen()
    base_w, base_h = BASE_SIZE  # Base resolution for scaling

    scale_factor = min(screen_w / base_w, screen_h / base_h)

    if isinstance(value, (int, float)):
        scaled_value = value * scale_factor
        return round(scaled_value) if round_values else scaled_value

    if isinstance(value, tuple):
        return tuple(scale(v, round_values=round_values) for v in value)

    raise TypeError("Value must be an int, float, or tuple of int/float.")
# =====================================================
# Text rendering
# =====================================================
def render_text(
    text: str,
    position: Position,
    size: int = 50,
    color: ColorType = "#000000",
    font: Optional[pygame.font.Font] = None,
    bold: bool = False,
    italic: bool = False,
    underline: bool = False,
    draw: bool = True
) -> Tuple[pygame.Surface, pygame.Rect]:
    """Render text to the active display surface."""

    screen = pygame.display.get_surface()
    if screen is None:
        raise RuntimeError("Display surface not initialized. Call pygame.display.set_mode().")

    # Create font if none provided
    if font is None:
        font = pygame.font.SysFont("Arial", size)

    # Convert color string to pygame.Color
    if isinstance(color, str):
        color = pygame.Color(color)  # type: ignore

    # Apply font styles
    font.set_bold(bold)
    font.set_italic(italic)
    font.set_underline(underline)

    # Render text
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(topleft=position)

    if draw:
        screen.blit(text_surface, text_rect)

    return text_surface, text_rect


# =====================================================
# Loading / Saving Files
# =====================================================
def load_image(path: str) -> pygame.Surface:
    """Load an image from disk with alpha support."""
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        DATA_DIR = os.path.join(BASE_DIR, "assets")
        image = pygame.image.load(os.path.join(DATA_DIR, path))
        return image
    except pygame.error as e:
        raise FileNotFoundError(f"Unable to load image at '{path}': {e}") from e


def load_font(path: str, size: int) -> pygame.font.Font:
    """Load a font from disk."""
    try:
        return pygame.font.Font(path, size)
    except IOError as e:
        raise FileNotFoundError(f"Unable to load font at '{path}': {e}") from e


def load_sound(path: str) -> pygame.mixer.Sound:
    """Load a sound from disk."""
    try:
        return pygame.mixer.Sound(path)
    except pygame.error as e:
        raise FileNotFoundError(f"Unable to load sound at '{path}': {e}") from e



# =====================================================
# Sprite Sheets
# =====================================================
class SpriteSheet:
    def __init__(self, image_location: str):
        self.sprite_sheet = load_image(image_location)
        self.sprite_sheet_rect = self.sprite_sheet.get_rect()
        self.imgs: List[ImageType] = []
        
    
    @overload
    def extract_image(self, points: List[Rect], scale: Tuple[int|float, int|float], Alpha: int = 255) -> List[ImageType]: ...
    
    @overload
    def extract_image(self, Crop_size: Tuple[int|float, int|float], Crop_start: Tuple[int|float, int|float], Scale: Tuple[int|float, int|float],  Alpha: int = 255) -> List[ImageType]: ...

    def extract_image(self, *args, Alpha: int = 255, **kwargs) -> List[ImageType]:
        """Extract images from the sprite sheet."""
        images = []
        if 'points' in kwargs:
            points = kwargs['points']
            scale = kwargs['scale']
            for point in points:
                x, y, w, h = point
                image = pygame.Surface((w, h), pygame.SRCALPHA)
                image.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
                image = pygame.transform.scale(image, scale)
                image.set_alpha(Alpha)
                images.append(ImageType(image))
        else:
            Crop_size = kwargs['Crop_size']
            Crop_start = kwargs['Crop_start']
            Scale = kwargs['Scale']
            x_start, y_start = Crop_start
            w_crop, h_crop = Crop_size
            for y in range(y_start, self.sprite_sheet_rect.height, h_crop):
                for x in range(x_start, self.sprite_sheet_rect.width, w_crop):
                    image = pygame.Surface((w_crop, h_crop), pygame.SRCALPHA)
                    image.blit(self.sprite_sheet, (0, 0), (x, y, w_crop, h_crop))
                    image = pygame.transform.scale(image, Scale)
                    image.set_alpha(Alpha)
                    images.append(ImageType(image))
        self.imgs = images
        return images

    def get_image(self, index: int) -> ImageType:
        """Get an extracted image by index."""
        return self.imgs[index]
    