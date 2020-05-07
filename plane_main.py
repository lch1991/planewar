import pygame
from plane_sprites import *


class PlaneGame(object):

    def __init__(self):
        print("游戏初始化...")
        # 1. 创建游戏的窗口
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 4.设置定时事件 创建敌机 1s一个
        pygame.time.set_timer(CREATE_ENEMY_EVENT,1000)
        pygame.time.set_timer(HERO_FIRE_EVENT,500)

    def __create_sprites(self):
        ## 两张背景图交替滚动
        bg1 = BackGround()
        bg2 = BackGround(True)
        self.back_group = pygame.sprite.Group(bg1,bg2)

        # 创建敌机的精灵组
        self.enemy_group = pygame.sprite.Group()

        # 创建英雄的精灵和精灵组
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        print("游戏开始...")
        while True:
            # 1. 设置刷新帧率
            self.clock.tick(FRAME_PER_SEC)
            # 2. 事件监听
            self.__event_handler()
            # 3. 碰撞检测
            self.__check_collide()
            # 4. 更新/绘制精灵组
            self.__update_sprites()
            # 5. 更新显示
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            # 判断是否退出游戏
            if event.type == pygame.QUIT:
                PlaneGame.__game_over()
            elif event.type == CREATE_ENEMY_EVENT:
                print("敌机出场...")
                # 创建敌机精灵
                enemy = Enemy()
                self.enemy_group.add(enemy)
            elif event.type == HERO_FIRE_EVENT:
                self.hero.fire()

        # 使用键盘提供的方法获取键盘按键 - 按键元组
        keys_pressed =pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            print("向右...")
            self.hero.speed = 2
            self.hero.update(self,1)
        elif keys_pressed[pygame.K_LEFT]:
            print("向左...")
            self.hero.speed = -2
            self.hero.update(self, 1)
        elif keys_pressed[pygame.K_DOWN]:
            print("向下...")
            self.hero.speed = 1
            self.hero.update(self, 0)
        elif keys_pressed[pygame.K_UP]:
            print("向上...")
            self.hero.speed = -1
            self.hero.update(self, 0)
        else:
            self.hero.speed = 0

    def __check_collide(self):

        # 1. 子弹摧毁敌机
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)

        # 2. 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表时候有内容
        if len(enemies) > 0:
            # 让英雄牺牲
            self.hero.kill()

            # 结束游戏
            PlaneGame.__game_over()

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update(self,1)
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    # 静态方法
    @staticmethod
    def __game_over():
        print("游戏结束...")
        pygame.quit()
        exit()

if __name__ == '__main__':
    # 创建游戏对象
    plane = PlaneGame()
    # 启动游戏
    plane.start_game()
