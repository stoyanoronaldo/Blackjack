import time
import sys
import os
import json
import pygame
from Hand import Hand
from Deck import Deck
from Constants import *

pygame.init()

clock = pygame.time.Clock()

game_display = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('BlackJack')
game_display.fill(background_color)
pygame.draw.rect(game_display, grey, pygame.Rect(0, 0, 200, 900))

def text_objects(text: str, font: tuple[str, int]):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def end_text_objects(text: str, font : tuple[str, int], color: tuple[int, int, int]):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def game_texts(text: str, x: float, y: float):
    TextSurf, TextRect = text_objects(text, textfont)
    TextRect.center = (x, y)
    game_display.blit(TextSurf, TextRect)
    pygame.display.update()

def game_finish(text: str, x: float, y: float, color: tuple[int, int, int]):
    TextSurf, TextRect = end_text_objects(text, game_end, color)
    TextRect.center = (x, y)
    game_display.blit(TextSurf, TextRect)
    pygame.display.update()

def black_jack(text: str, x: float, y: float, color: tuple[int, int, int]):
    TextSurf, TextRect = end_text_objects(text, blackjack, color)
    TextRect.center = (x, y)
    game_display.blit(TextSurf, TextRect)
    pygame.display.update()
    
def button(name: str, x: float, y: float, width: float, height: float,
           inactive : tuple[int, int, int], active : tuple[int, int, int], action=None):

    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(game_display, active, (x, y, width, height))
        if click[0] == 1 != None:
            action()
    else:
        pygame.draw.rect(game_display, inactive, (x, y, width, height))

    TextSurf, TextRect = text_objects(name, font)
    TextRect.center = ((x + (width/2)), (y + (height/2)))
    game_display.blit(TextSurf, TextRect)

fd = open(os.path.join('D:/', 'Blackjack python', 'Blackjack', 'statistics.txt'))
statistics: str = fd.read()
json_statistics: dict[str, int] = json.loads(statistics)
fd.close()

class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        
    def blackjack(self):
        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        
        if self.player.get_value() == 21 and self.dealer.get_value() == 21:
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            black_jack("Both with BlackJack!", 500, 250, grey)
            time.sleep(2)
            self.play_or_exit()
        elif self.player.get_value() == 21:
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            black_jack("You got BlackJack!", 500, 250, green)
            time.sleep(2)
            self.play_or_exit()
        elif self.dealer.get_value() == 21:
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            black_jack("Dealer has BlackJack!", 500, 250, red)
            time.sleep(2)
            self.play_or_exit()

    def deal(self):
        for _ in range(2):
            self.dealer.add_card(self.deck.deal_card())
            self.player.add_card(self.deck.deal_card())

        self.number_player_cards: int = 2
        self.number_dealer_cards: int = 2

        self.dealer.display_cards()
        self.player.display_cards()

        dealer_card = pygame.image.load('img/' + self.dealer.card_img[0] + '.png').convert()
        dealer_card_2 = pygame.image.load('img/back.png').convert()
            
        player_card = pygame.image.load('img/' + self.player.card_img[0] + '.png').convert()
        player_card_2 = pygame.image.load('img/' + self.player.card_img[1] + '.png').convert()

        game_display.fill(background_color, (280, 130, 400, 40))
        game_texts(f"Dealers hand is: {self.dealer.get_value()}", 500, 150)

        game_display.blit(dealer_card, (dealer_card_coordX, 200))
        game_display.blit(dealer_card_2, (dealer_card_coordX + 110, 200))

        game_display.fill(background_color, (280, 380, 400, 40))
        game_texts(f"Yours hand is: {self.player.get_value()}", 500, 400)
        
        game_display.blit(player_card, (player_card_coordX, 450))
        game_display.blit(player_card_2, (player_card_coordX + 110, 450))

        self.blackjack()

    def hit(self):
        self.player.add_card(self.deck.deal_card())
        
        self.player.display_cards()
        player_card = pygame.image.load('img/' + self.player.card_img[self.number_player_cards] + '.png').convert()
        game_display.blit(player_card, (player_card_coordX + self.number_player_cards * 110, 450))

        self.number_player_cards += 1

        game_display.fill(background_color, (280, 380, 400, 40))
        game_texts(f"Yours hand is: {self.player.get_value()}", 500, 400)
         
        if self.player.get_value() > 21:
            show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            game_finish("You Busted!", 700, 70, red)
            time.sleep(5)
            self.play_or_exit()

    def stand(self):
        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))

        while self.dealer.get_value() < 17:
            self.dealer.add_card(self.deck.deal_card())
            self.dealer.display_cards()
            dealer_card = pygame.image.load('img/' + self.dealer.card_img[self.number_dealer_cards] + '.png').convert()
            game_display.blit(dealer_card, (dealer_card_coordX + 110 * self.number_dealer_cards, 200))
            self.number_dealer_cards += 1
            game_display.fill(background_color, (280, 130, 400, 40))
            game_texts(f"Dealers hand is: {self.dealer.get_value()}", 500, 150)

        if self.dealer.get_value() > 21 or self.player.get_value() > self.dealer.get_value():
            game_finish("You Won!", 700, 70, green)
            time.sleep(5)
            self.play_or_exit()
        elif self.player.get_value() < self.dealer.get_value():
            game_finish("Dealer Wins!", 700, 70, red)
            time.sleep(5)
            self.play_or_exit()
        else:
            game_finish("It's a Tie!", 700, 70, grey)
            time.sleep(5)
            self.play_or_exit()

    def double(self):
        pass

    def hint(self):
        pass

    def exit(self):
        fd = open(os.path.join('D:/', 'Blackjack python', 'Blackjack', 'statistics.txt'), 'w')
        fd.write(str(json_statistics))
        fd.close()
        sys.exit()

    def play_or_exit(self):
        game_texts("Play again press Deal!", 200, 70)
        time.sleep(2)
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Hand()
        self.player = Hand()
        game_display.fill(background_color)
        pygame.draw.rect(game_display, grey, pygame.Rect(0, 0, 200, 900))
        pygame.display.update()

play_blackjack: Play = Play()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fd = open(os.path.join('D:/', 'Blackjack python', 'Blackjack', 'statistics.txt'), 'w')
            fd.write(str(json_statistics))
            fd.close()
            running = False

        button("Deal", 25, 100, 150, 50, light_slat, dark_slat, play_blackjack.deal)
        button("Hit", 25, 200, 150, 50, light_slat, dark_slat, play_blackjack.hit)
        button("Stand", 25, 300, 150, 50, light_slat, dark_slat, play_blackjack.stand)
        button("Double", 25, 400, 150, 50, light_slat, dark_slat, play_blackjack.double)
        button("Hint", 25, 500, 150, 50, light_slat, dark_slat, play_blackjack.hint)
        button("EXIT", 25, 700, 150, 50, light_slat, dark_red, play_blackjack.exit)
    
    pygame.display.flip()
