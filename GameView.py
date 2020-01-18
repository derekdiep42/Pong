import pygame
import ctypes

pygame.font.init()
fps = 50
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0 , 0)

screen = pygame.display.set_mode((660, 420))
clock = pygame.time.Clock()
pygame.display.set_caption('Pong Game')


class Player(object):
    def __init__(self, x, y, size_x, size_y, color):
        self.image = pygame.Surface((size_x, size_y), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.image.convert_alpha()

        self.rect.left = x
        self.rect.top = y
        self.color = color
        self.movement = [0, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        self.boundaries()

    def boundaries(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 420:
            self.rect.bottom = 420


class Ball(object):
    def __init__(self, x, y, size, color, score_right, score_left):
        self.image = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.image.fill(color)
        self.image.convert_alpha()

        self.rect.left = x
        self.rect.top = y

        self.score_right = score_right
        self.score_left = score_left
        self.color = color
        self.movement = [5, 5]
        self.max_speed = 10
        self.pause = True

    def draw(self):
        font1 = pygame.font.SysFont("Arial", 20)
        font2 = pygame.font.SysFont("Arial", 20)
        font3 = pygame.font.SysFont("Arial", 10)
        text1 = font1.render(str(self.score_left), True, white)
        text2 = font2.render(str(self.score_right), True, white)
        text3 = font3.render("Press Tab to shoot", True, white)
        screen.blit(self.image, self.rect)
        screen.blit(text1, (140, 25))
        screen.blit(text2, (508, 25))
        screen.blit(text3, (281, 7))

    def update(self):
        if self.rect.top <= 0 or self.rect.bottom >= 420:
            self.movement[1] = -1*self.movement[1]

        if self.movement[1] > self.max_speed:
            self.movement[1] = self.max_speed

        self.rect = self.rect.move(self.movement)
        self.boundaries()

        if self.rect.left <= 0 or self.rect.right >= 660:
            self.pause = True

    def boundaries(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 420:
            self.rect.bottom = 420
        if self.rect.left <= 0:
            self.rect.left = 0
            self.score_right = self.score_right + 1
        if self.rect.right >= 660:
            self.rect.right = 660
            self.score_left = self.score_left + 1


def main():
    game_over = False

    player1 = Player(50, 56, 8, 70, white)
    player2 = Player(598, 56, 8, 70, white)
    pong_ball = Ball(331, 210, 15, red, 0, 0)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    player1.movement[1] = -9
                if event.key == pygame.K_s:
                    player1.movement[1] = 9
                if event.key == pygame.K_UP:
                    player2.movement[1] = -9
                if event.key == pygame.K_DOWN:
                    player2.movement[1] = 9
                if event.key == pygame.K_TAB and pong_ball.pause:
                    pong_ball.pause = False
                    pong_ball.movement[0] = 5
                    pong_ball.movement[1] = 5
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_w or event.key == pygame.K_s:
                    player1.movement[1] = 0
                if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    player2.movement[1] = 0

        if pong_ball.pause:
            pong_ball.movement[0] = 0
            pong_ball.movement[1] = 0
            pong_ball.rect.left = 331
            pong_ball.rect.top = 210

        if pygame.sprite.collide_rect(player1, pong_ball):
            pong_ball.rect.left = pong_ball.rect.left + 8
            pong_ball.movement[0] = -1*pong_ball.movement[0]
            pong_ball.movement[1] = pong_ball.movement[1] - player1.movement[1]

        if pygame.sprite.collide_rect(player2, pong_ball):
            pong_ball.rect.left = pong_ball.rect.left - 8
            pong_ball.movement[0] = -1*pong_ball.movement[0]
            pong_ball.movement[1] = pong_ball.movement[1] - player1.movement[1]

        if pong_ball.score_left == 7:
            game_over = True
            ctypes.windll.user32.MessageBoxW(0, "Left Player Wins!!!", "Game Over", 1)

        if pong_ball.score_right == 7:
            game_over = True
            ctypes.windll.user32.MessageBoxW(0, "Right Player Wins!!!", "Game Over", 1)

        player1.update()
        player2.update()
        pong_ball.update()

        screen.fill(black)
        player1.draw()
        player2.draw()
        pong_ball.draw()

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
    quit()


main()


