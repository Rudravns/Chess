from typing import * # pyright: ignore[reportWildcardImportFromLibrary]
import pygame

pygame.init()
pygame.display.init()
pygame.font.init()


#====================================================
# Data Types
#====================================================
ColorType: TypeAlias = Union[
    str,
    tuple[int, int, int],
    tuple[int, int, int, int],
]

Size: TypeAlias = tuple[int | float, int | float]
Rect: TypeAlias = tuple[int | float, int | float, int | float, int | float]
Position: TypeAlias = tuple[int | float, int | float]
PiecePosition: TypeAlias = tuple[str, int]

#====================================================
# Class Data Types
#====================================================
class ImageType:
    __slots__ = ("_surface",)

    def __init__(self, surface: pygame.Surface):
        self._surface = surface.convert_alpha()

    @property
    def surface(self) -> pygame.Surface:
        return self._surface

    def draw(self, position: Position) -> None:
        screen = pygame.display.get_surface()
        if screen is None:
            raise RuntimeError("Display not initialized")
        screen.blit(self._surface, position)

    def scale(self, size: Size) -> "ImageType":
        return ImageType(pygame.transform.scale(self._surface, size))

    def tint(self, color: ColorType) -> "ImageType":
        surf = self._surface.copy()
        surf.fill(color, special_flags=pygame.BLEND_RGBA_MULT)
        return ImageType(surf)

    def to_black_piece(self) -> "ImageType":
        surf = self._surface.copy()

        with pygame.PixelArray(surf) as px:
            px.replace(
            (255, 255, 255),  # color to find
            (60, 60, 60),     # replacement color
            0.2               # distance
        )

        return ImageType(surf)
    def get_rect(self) -> pygame.Rect:
        return self._surface.get_rect()

    def __repr__(self) -> str:
        return f"<ImageType size={self._surface.get_size()}>"

    def __eq__(self, other: object) -> bool:
        return isinstance(other, ImageType) and self._surface is other._surface

    def __hash__(self) -> int:
        return id(self._surface)



#====================================================
# Constants
#====================================================
FULLSCREEN = pygame.display.Info().current_w, pygame.display.Info().current_h
BASE_SIZE = (1000, 600)
START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

#====================================================
# Color Definitions
#====================================================
WHITE: ColorType = "#FFFFFF"
BLACK: ColorType = "#000000"
RED: ColorType = "#FF0000"
GREEN: ColorType = "#00FF00"
BLUE: ColorType = "#0000FF"
YELLOW: ColorType = "#FFFF00"
MAGENTA: ColorType = "#FF00FF"
CYAN: ColorType = "#00FFFF"
GREY: ColorType = "#808080"
LIGHT_GREY: ColorType = "#C0C0C0"
DARK_GREY: ColorType = "#404040"
TRANSPARENT: ColorType = "#00000000"
SEMI_TRANSPARENT: ColorType = "#00000080"
VERY_LIGHT_BLUE: ColorType = "#d2bef6"
LIGHT_BLUE: ColorType = "#a066f0"
DARK_BLUE: ColorType = "#35009e"
VERY_DARK_BLUE: ColorType = "#1a0066"
LIGHT_BROWN: ColorType = "#f0d9b5"
DARK_BROWN: ColorType = "#b58863"
MOSS_GREEN: ColorType = "#a4b080"
EARTH_BROWN: ColorType = "#4d3a2b"
NEON_CYAN: ColorType = "#00f2ff"
DEEP_VOID: ColorType = "#0a0a0a"
GLOW_PURPLE: ColorType = "#bf00ff"
ULTRA_LIGHT_GRAY: ColorType = "#ffffff"
MID_GRAY: ColorType = "#808080"
DEEP_CHARCOAL: ColorType = "#2b2b2b"
LIGHT_ROSE: ColorType = "#f0d2d2"
DARK_ROSE: ColorType = "#b25d5d"
LIGHT_SLATE: ColorType = "#e1e1e1"
DARK_SLATE: ColorType = "#71828f"
LIGHT_GREEN: ColorType = "#eedd82"
DARK_GREEN: ColorType = "#779556"
PROMO_BG_OVERLAY   = "#000000A0"  # black, ~63% opacity
PROMO_PANEL        = "#2F313AFF"  # fully opaque
PROMO_OPTION       = "#3E4150FF"
PROMO_OPTION_HOVER = "#5A5E78FF"
PROMO_BORDER       = "#C8CAD6FF"
PROMO_TEXT         = "#E6E6F0FF"
CHECK = "#ff3838ff"
