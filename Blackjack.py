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
bet: int = 0
hint_string: str = ''

class Play:
    def __init__(self):
        self.deck = Deck()
        self.dealer = Hand()
        self.player = Hand()
        self.deck.shuffle()
        self.playing: bool = False
        self.valid_bet: bool = True if bet > 0 else False
        
    def blackjack(self):
        global bet
        show_dealer_card = pygame.image.load('img/' + self.dealer.card_img[1] + '.png').convert()
        
        if self.player.get_value() == 21 and self.dealer.get_value() == 21:
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            black_jack("Both with BlackJack!", 750, 70, grey)
            json_statistics["Blackjacks"] += 1
            json_statistics["Ties"] += 1
            time.sleep(2)
            self.play_or_exit()
        elif self.player.get_value() == 21:
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            black_jack("You got BlackJack!", 750, 70, green)
            json_statistics["Blackjacks"] += 1
            json_statistics["Money"] += 3*bet/2
            json_statistics["Wins"] += 1
            time.sleep(2)
            self.play_or_exit()
        elif self.dealer.get_value() == 21:
            game_display.blit(show_dealer_card, (dealer_card_coordX + 110, 200))
            black_jack("Dealer has BlackJack!", 750, 70, red)
            json_statistics["Money"] -= bet
            json_statistics["Loses"] += 1
            time.sleep(2)
            self.play_or_exit()

    def deal(self):
        global bet
        self.valid_bet = True if bet > 0 else False
        if self.valid_bet:
            self.playing = True
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
            game_texts(f"Dealers hand is: ", 500, 150)

            game_display.blit(dealer_card, (dealer_card_coordX, 200))
            game_display.blit(dealer_card_2, (dealer_card_coordX + 110, 200))

            game_display.fill(background_color, (280, 380, 400, 40))
            game_texts(f"Yours hand is: {self.player.get_value()}", 500, 400)
            
            game_display.blit(player_card, (player_card_coordX, 450))
            game_display.blit(player_card_2, (player_card_coordX + 110, 450))

            self.blackjack()

    def hit(self):
        global bet
        self.valid_bet = True if bet > 0 else False
        if self.valid_bet:
            game_display.fill(background_color, (230, 630, 400, 40))
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
                game_finish("You Busted!", 850, 70, red)
                json_statistics["Money"] -= bet
                json_statistics["Loses"] += 1
                time.sleep(5)
                self.play_or_exit()

    def stand(self):
        global bet
        self.valid_bet = True if bet > 0 else False
        if self.valid_bet:
            game_display.fill(background_color, (230, 630, 400, 40))
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
                game_finish("You Won!", 850, 70, green)
                json_statistics["Money"] += bet
                json_statistics["Wins"] += 1
                time.sleep(5)
                self.play_or_exit()
            elif self.player.get_value() < self.dealer.get_value():
                game_finish("Dealer Wins!", 850, 70, red)
                json_statistics["Money"] -= bet
                json_statistics["Loses"] += 1
                time.sleep(5)
                self.play_or_exit()
            else:
                game_finish("It's a Tie!", 850, 70, grey)
                json_statistics["Ties"] += 1
                time.sleep(5)
                self.play_or_exit()

    def double(self):
        global bet
        self.valid_bet = True if bet > 0 else False
        if self.valid_bet:
            game_display.fill(background_color, (230, 630, 400, 40))
            bet *= 2
            self.hit()
            if self.playing:
                self.stand()

    def hint(self):
        global bet
        self.valid_bet = True if bet > 0 else False
        if self.valid_bet:
            global hint_string
            is_ace_present = False
            for card in self.player.cards:
                if card.rank == "A":
                    is_ace_present = True
                    break

            player_value = self.player.get_value()
            dealer_card_value = VALUES[self.dealer.cards[0].rank]

            if not is_ace_present:
                if((player_value in [2, 3, 4, 5, 6, 7]) or 
                    (player_value == 8 and dealer_card_value not in [5, 6]) or
                    (player_value == 9 and dealer_card_value in [1, 7, 8, 9, 10]) or
                    (player_value == 10 and dealer_card_value in [1, 10]) or
                    (player_value == 12 and dealer_card_value in [1, 2, 3, 7, 8, 9, 10]) or
                    (player_value in [13, 14, 15, 16] and dealer_card_value in [1, 7, 8, 9, 10])
                ):
                    hint_string = "Hit"

                if((player_value == 8 and dealer_card_value in [5, 6]) or
                (player_value == 9 and dealer_card_value in [2, 3, 4, 5, 6]) or
                (player_value == 10 and dealer_card_value not in [1, 10]) or
                (player_value == 11)
                ):
                    hint_string = "Double"

                if((player_value == 12 and dealer_card_value in [4, 5, 6]) or
                (player_value in [13, 14, 15, 16] and dealer_card_value in [2, 3, 4, 5, 6]) or
                (player_value >= 17)
                ):
                    hint_string = "Stand"
            else:
                if((player_value in [13, 14, 15, 16] and dealer_card_value in [1, 2, 3, 7, 8, 9, 10]) or 
                    (player_value == 17 and dealer_card_value in [1, 7, 8, 9, 10]) or
                    (player_value == 18 and dealer_card_value in [9, 10])
                ):
                    hint_string = "Hit"

                if((player_value in [13, 14, 15, 16] and dealer_card_value in [4, 5, 6]) or
                (player_value == 17 and dealer_card_value in [2, 3, 4, 5, 6]) or
                (player_value == 18 and dealer_card_value in [3, 4, 5, 6]) or
                (player_value == 19 and dealer_card_value == 6)
                ):
                    hint_string = "Double"

                if((player_value == 18 and dealer_card_value in [1, 2, 7, 8]) or
                (player_value == 19 and dealer_card_value != 6) or
                (player_value == 20)
                ):
                    hint_string = "Stand"

            game_texts(f"Hint: {hint_string}", 450, 650)

    def exit(self):
        fd = open(os.path.join('D:/', 'Blackjack python', 'Blackjack', 'statistics.txt'), 'w')
        fd.write(json.dumps(json_statistics))
        fd.close()
        sys.exit()

    def play_or_exit(self):
        game_texts("Play again press Deal!", 400, 70)
        time.sleep(2)
        global bet
        bet = 0
        self.deck = Deck()
        self.deck.shuffle()
        self.dealer = Hand()
        self.player = Hand()
        game_display.fill(background_color)
        pygame.draw.rect(game_display, grey, pygame.Rect(0, 0, 200, 900))
        pygame.display.update()
        self.playing = False

play_blackjack: Play = Play()

running = True

input_box = pygame.Rect(25, 40, 150, 32)
color_inactive = pygame.Color(light_slat)
color_active = pygame.Color(dark_slat)
input_color = color_inactive
input_active = False
input_text = ''

while running:
    money = json_statistics["Money"]
    game_texts(f"Your amount is: {money}", 900, 400)
    game_texts("Bet:", 100, 20)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            fd = open(os.path.join('D:/', 'Blackjack python', 'Blackjack', 'statistics.txt'), 'w')
            fd.write(json.dumps(json_statistics))
            fd.close()
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                input_active = True
                input_text = ''
            else:
                input_active = False
            input_color = color_active if input_active else color_inactive
  
        if event.type == pygame.KEYDOWN:
            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    input_text += event.unicode

                if event.key == pygame.K_RETURN:
                    bet = int(input_text)
                    input_text = ''
                    input_active = False
                    input_color = color_active if input_active else color_inactive

        button("Deal", 25, 100, 150, 50, light_slat, dark_slat, play_blackjack.deal)
        button("Hit", 25, 200, 150, 50, light_slat, dark_slat, play_blackjack.hit)
        button("Stand", 25, 300, 150, 50, light_slat, dark_slat, play_blackjack.stand)
        button("Double", 25, 400, 150, 50, light_slat, dark_slat, play_blackjack.double)
        button("Hint", 25, 500, 150, 50, light_slat, dark_slat, play_blackjack.hint)
        button("EXIT", 25, 700, 150, 50, light_slat, dark_red, play_blackjack.exit)

    txt_surface = font.render(input_text, True, input_color)
    game_display.blit(txt_surface, (input_box.x+5, input_box.y+5))
    pygame.draw.rect(game_display, input_color, input_box, 2)
    
    pygame.display.flip()
