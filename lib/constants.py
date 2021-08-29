import pygame
import string

# Paths
PATH_TO_DICTIONARY = "media/dictionary.txt"

# Characters
ALPHABET = set(string.ascii_lowercase + string.ascii_uppercase)
LINE_SPACING = -2

# Font sizes
DEFAULT_FONT_SIZE = 32
DEFAULT_SMALL_FONT_SIZE = 14

# Screen sizes
WIDTH = 1280
HEIGHT = 720

# Colors
BLACK = pygame.color.Color(0, 0, 0)
WHITE = pygame.color.Color(255, 255, 255)
RED = pygame.color.Color(255, 0, 0)
COLOR_INACTIVE = pygame.color.Color(171, 219, 227)
COLOR_ACTIVE = pygame.color.Color(30, 129, 176)
