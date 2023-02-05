import pygame as pygame

display_width: float = 1100
display_height: float = 800

player_card_coordX: float = 300
dealer_card_coordX: float = 400

background_color: tuple[int, int, int] = (34,139,34)
grey: tuple[int, int, int] = (220,220,220)
black: tuple[int, int, int] = (0,0,0)
green: tuple[int, int, int] = (0, 200, 0)
red: tuple[int, int, int] = (255,0,0)
light_slat: tuple[int, int, int] = (119,136,153)
dark_slat: tuple[int, int, int] = (47, 79, 79)
dark_red: tuple[int, int, int] = (255, 0, 0)

pygame.init()

font: tuple[str, int] = pygame.font.SysFont("Arial", 20)
textfont: tuple[str, int] = pygame.font.SysFont('Comic Sans MS', 35)
game_end: tuple[str, int] = pygame.font.SysFont('dejavusans', 100)
blackjack: tuple[str, int] = pygame.font.SysFont('roboto', 70)

SUITS: tuple[str, ...] = ("C", "D", "H", "S")
RANKS: tuple[str, ...] = ('A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K')
VALUES: dict[str, int] = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 10, 'Q': 10, 'K': 10}

CARD_SIZE: tuple[int, int] = (72, 96)
CARD_CENTER: tuple[int, int] = (36, 48)
CARD_BACK_SIZE: tuple[int, int] = (72, 96)
CARD_BACK_CENTER: tuple[int, int] = (36, 48)