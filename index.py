import pygame
from pygame.locals import *
import sys
import time
import random

WIDTH = 750
HEIGHT = 500

class Game:
    def __init__(self):
        self.reset = True
        self.active = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.accuracy = '0%'
        self.results = 'Time: 0 Accuracy: 0% Wpm: 0'
        self.wpm = 0
        self.end = False
        self.HEAD_C = (255, 213, 102)
        self.TEXT_C = (240, 240, 240)
        self.RESULT_C = (255, 70, 70)
        
        pygame.init()
        self.open_img = pygame.image.load('C:\\Users\\KIIT\\OneDrive\\Documents\\Speed Typing Test\\type-speed-open.png')
        self.open_img = pygame.transform.scale(self.open_img, (WIDTH, HEIGHT))

        self.bg = pygame.image.load("C:\\Users\\KIIT\\OneDrive\\Documents\\Speed Typing Test\\background.jpg")
        self.bg = pygame.transform.scale(self.bg, (750, 750))

        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Type Speed Test')

    def draw_text(self, screen, msg, y, fsize, color):
        font = pygame.font.Font(None, fsize)
        text = font.render(msg, 1, color)
        text_rect = text.get_rect(center=(WIDTH/2, y))
        screen.blit(text, text_rect)
        pygame.display.update()
        
    def get_sentence(self):
        with open("C:\\Users\\KIIT\\OneDrive\\Documents\\Speed Typing Test\\sentences.txt") as f:
            sentences = f.read().split('\n')
        sentence = random.choice(sentences)
        return sentence

    def show_results(self, screen):
        self.total_time = time.time() - self.time_start

        correct_chars = 0
        for i in range(len(self.input_text)):
            if i < len(self.word) and self.input_text[i] == self.word[i]:
                correct_chars += 1

        self.accuracy = correct_chars / len(self.input_text) * 100
        self.wpm = len(self.input_text.split()) * 60 / self.total_time

        self.results = f'Time: {round(self.total_time)} secs   Accuracy: {round(self.accuracy)}%   Wpm: {round(self.wpm)}'
        self.end = True
        print(self.total_time)

        self.time_img = pygame.image.load("C:\\Users\\KIIT\\OneDrive\\Documents\\Speed Typing Test\\icon.png")
        self.time_img = pygame.transform.scale(self.time_img, (130, 130))
        screen.blit(self.time_img, (WIDTH/2-75, HEIGHT-120))
        self.draw_text(screen, "Reset", HEIGHT-70, 26, (90, 90, 90))

        print(self.results)
        pygame.display.update()




    def run(self):
        self.reset_game()
        self.running = True

        while self.running:
            clock = pygame.time.Clock()
            self.screen.fill((0, 0, 0), (50, 250, 650, 50))
            pygame.draw.rect(self.screen, self.HEAD_C, (50, 250, 650, 50), 2)
            self.draw_text(self.screen, self.input_text, 274, 26, (250, 250, 250))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONUP:
                    x, y = pygame.mouse.get_pos()
                    if 50 <= x <= 650 and 250 <= y <= 300:
                        self.active = True
                        self.input_text = ''
                        self.time_start = time.time()
                    elif 310 <= x <= 510 and 390 <= y <= HEIGHT and self.end:
                        self.reset_game()
                        x, y = pygame.mouse.get_pos()

                elif event.type == pygame.KEYDOWN:
                    if self.active and not self.end:
                        if event.key == pygame.K_RETURN:
                            print(self.input_text)
                            self.show_results(self.screen)
                            print(self.results)
                            self.draw_text(self.screen, self.results, 350, 28, self.RESULT_C)
                            self.end = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.input_text = self.input_text[:-1]
                        else:
                            try:
                                self.input_text += event.unicode
                            except:
                                pass

            pygame.display.update()
            clock.tick(60)

    def reset_game(self):
        self.screen.blit(self.open_img, (0, 0))
        pygame.display.update()
        time.sleep(1)
        
        self.reset = False
        self.end = False
        self.input_text = ''
        self.word = ''
        self.time_start = 0
        self.total_time = 0
        self.wpm = 0

        self.word = self.get_sentence()
        if not self.word:
            self.reset_game()

        self.screen.fill((0, 0, 0))
        self.screen.blit(self.bg, (0, 0))
        msg = "Typing Speed Test"
        self.draw_text(self.screen, msg, 80, 80, self.HEAD_C)
        pygame.draw.rect(self.screen, (255, 192, 25), (50, 250, 650, 50), 2)
        self.draw_text(self.screen, self.word, 200, 28, self.TEXT_C)
        pygame.display.update()

Game().run()
