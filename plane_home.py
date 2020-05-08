import pygame
from plane_sprites import *
from plane_main import *


class PlaneHome(object):

    def load(self):
        pygame.init()
        white = 255, 255, 255
        # 1. 创建游戏的窗口
        screen = pygame.display.set_mode(SCREEN_RECT.size)
        pygame.display.set_caption("飞机大战")
        myfont = pygame.font.Font(None, 60)
        textImage = myfont.render("Plane War", True, white)
        screen.blit(textImage, (130, 100))
        start = pygame.image.load("./images/again.png")
        screen.blit(start, (90, 400))
        pygame.display.update()

        while True:
            for event in pygame.event.get():
                # 判断是否退出游戏
                if event.type == pygame.QUIT:
                    PlaneGame.__game_over()
                # 监听鼠标点击事件
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pressed_array = pygame.mouse.get_pressed()
                    for index in range(len(pressed_array)):
                        if pressed_array[index]:
                            if index == 0:
                                pos = pygame.mouse.get_pos()
                                # 判断鼠标的点击范围
                                if 90 < pos[0] < 390 and 400 < pos[1] < 441:
                                    plane = PlaneGame(screen)
                                    plane.start_game()


if __name__ == '__main__':
    home = PlaneHome()
    home.load()