import pygame
import sys
import random
from pygame.locals import *

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BADDIE_MIN_SIZE = 10
BADDIE_Max_SIZE = 40
BADDIE_MIN_SPEED = 1
BADDIE_MAX_SPEED = 8
BADDIE_RATE = 6
PLAYER_MOVE_RATE = 5
FPS = 30


def terminate():
    """
    Closes the game
    :return:None
    """
    pygame.quit()
    sys.exit()


def wait_for_input():
    """
    Closes the game if pressed 'ESC' or close button
    :return:None
    """
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    terminate()
                return


def player_has_hit_buddie(player_rect, baddies):
    """
    Checks for hitting player
    :param player_rect:
    :param baddies:
    :return: Bool
    """
    for b in baddies:
        if player_rect.colliderect(b['rect']):
            return True
    return False


def draw_text(text: str, font, surface, x: float, y: float):
    """
    Draws text
    :param text:
    :param font:
    :param surface:
    :param x:
    :param y:
    :return: None
    """
    textobj = font.render(text, 1, WHITE)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


pygame.init()
main_clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('ЗЫ ГАМЕ')
pygame.mouse.set_visible(False)

font = pygame.font.SysFont('None', 48)

player_image = pygame.image.load('images/player.png')
player_rect = player_image.get_rect()
baddie_image = pygame.image.load('images/baddie.png')

draw_text('Уклоняйка', font, screen, (SCREEN_WIDTH / 3) + 20, (SCREEN_HEIGHT / 3))
draw_text('Нажмите Ф чтобы начать', font, screen, (SCREEN_WIDTH / 3) - 90, (SCREEN_HEIGHT / 3) + 50)
pygame.display.update()
wait_for_input()

top_score = 0
while True:
    badies = []
    score = 0
    player_rect.topleft = (SCREEN_WIDTH / 2, SCREEN_HEIGHT - 50)
    move_left = move_right = move_up = move_down = False
    baddie_add_counter = 0

    while True:
        score += 1
        baddie_add_counter += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            if event.type == KEYDOWN:
                if event.key == K_LEFT:
                    move_right = False
                    move_left = True
                if event.key == K_RIGHT:
                    move_right = True
                    move_left = False
                if event.key == K_UP:
                    move_down = False
                    move_up = True
                if event.key == K_DOWN:
                    move_up = False
                    move_down = True

            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_LEFT:
                    move_left = False
                if event.key == K_RIGHT:
                    move_right = False
                if event.key == K_UP:
                    move_up = False
                if event.key == K_DOWN:
                    move_down = False

            if event.type == MOUSEMOTION:
                player_rect.move_ip(event.pos[0] - player_rect.centerx, event.pos[1] - player_rect.centery)

        if baddie_add_counter == BADDIE_RATE:
            baddie_add_counter = 0
            baddie_size = random.randint(BADDIE_MIN_SIZE, BADDIE_Max_SIZE)
            new_baddie = {'rect': pygame.Rect(random.randint(0, SCREEN_WIDTH-baddie_size), 0 - baddie_size,
                                              baddie_size, baddie_size),
                          'speed': random.randint(BADDIE_MIN_SPEED, BADDIE_MAX_SPEED),
                          'surface': pygame.transform.scale(baddie_image, (baddie_size, baddie_size))}
            badies.append(new_baddie)

        if move_left and player_rect.left > 0:
            player_rect.move_ip(-1 * PLAYER_MOVE_RATE, 0)
        if move_right and player_rect.right < SCREEN_WIDTH:
            player_rect.move_ip(PLAYER_MOVE_RATE, 0)
        if move_up and player_rect.top > 0:
            player_rect.move_ip(0, -1 * PLAYER_MOVE_RATE)
        if move_down and player_rect.bottom < SCREEN_HEIGHT:
            player_rect.move_ip(0, PLAYER_MOVE_RATE)

        pygame.mouse.set_pos(player_rect.centerx, player_rect.centery)

        for b in badies:
            b['rect'].move_ip(0, b['speed'])

        for b in badies:
            if b['rect'].top > SCREEN_HEIGHT:
                badies.remove(b)

        screen.fill(BLACK)

        draw_text(f'Счет: {score}', font, screen, 10, 0)
        draw_text(f'Рекорд: {top_score}', font, screen, 10, 40)

        screen.blit(player_image, player_rect)

        for b in badies:
            screen.blit(b['surface'], b['rect'])

        pygame.display.update()

        if player_has_hit_buddie(player_rect, badies):
            if score > top_score:
                top_score = score
            break

        main_clock.tick(FPS)

    draw_text(f'КОНЕЦ ИГРЫ!', font, screen, (SCREEN_WIDTH / 4) + 20, (SCREEN_HEIGHT / 3))
    draw_text(f'Нажмите Ф чтобы начать снова', font, screen, (SCREEN_WIDTH / 4) - 90, (SCREEN_HEIGHT / 3) + 50)
    pygame.display.update()
    wait_for_input()
