import pygame
from plane_sprites import *
from plane_home import *


class PlaneGame(object):

    def __init__(self,screen):
        print("游戏初始化...")
        self.screen = screen
        # 2. 创建游戏的时钟
        self.clock = pygame.time.Clock()
        # 3. 调用私有方法，精灵和精灵组的创建
        self.__create_sprites()
        # 4.设置定时事件 创建敌机 1s一个
        pygame.time.set_timer(CREATE_ENEMY_EVENT,500)
        pygame.time.set_timer(HERO_FIRE_EVENT,300)
        pygame.time.set_timer(ENEMY_HIDE_EVENT,200)

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

        # 创建英雄生命的精灵和精灵组
        life1 = Life(1)
        life2 = Life(2)
        life3 = Life(3)
        self.life_group = pygame.sprite.Group(life1,life2,life3)

        self.blast_group = pygame.sprite.Group()

    @staticmethod
    def __play_music():
        """ 播放音乐"""
        pygame.mixer.music.load('./sound/back_music.mp3')  # 加载背景音乐
        pygame.mixer.music.set_volume(0.5)  # 设置音量
        pygame.mixer.music.play(-1)  # 播放背景音乐

    def start_game(self):
        print("游戏开始...")
        self.__play_music()
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
            elif event.type == ENEMY_HIDE_EVENT:
                for blast1 in self.blast_group.sprites():
                    self.blast_group.remove(blast1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pressed_array = pygame.mouse.get_pressed()
                for index in range(len(pressed_array)):
                    if pressed_array[index]:
                        if index == 0:
                            print('Pressed LEFT Button!')
                            plane.start_game()
                        # elif index == 1:
                        #     print('The mouse wheel Pressed!')
                        # elif index == 2:
                        #     print('Pressed RIGHT Button!')
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

        blast_list = []
        # 1. 子弹摧毁敌机
        collisions = pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        if collisions:
            for hero_bullet in collisions:  # in hero_shot_enemy.keys():
                # 击中的爆炸效果
                rect = hero_bullet.rect
                # print("rect==",rect)
                blast = Blast(rect)
                self.blast_group.add(blast)
            self.hero.score += 1
            # print("得分: " , self.hero.score)
        # 2. 敌机撞毁英雄
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)

        # 判断列表是否有内容
        if len(enemies) > 0:
            # 获取精灵组生命数
            nums = len(self.life_group)
            if nums > 0:
                for life in self.life_group.sprites():
                    # 按照位置从左至右删除
                    if life.num == nums:
                        self.life_group.remove(life)
            else:
                # 让英雄牺牲
                self.hero.kill()
                # 结束游戏
                PlaneGame.__game_over()
            # pygame.quit()
            # plane_home = PlaneHome()
            # plane_home.load()

    def __update_sprites(self):

        self.back_group.update()
        self.back_group.draw(self.screen)

        self.enemy_group.update()
        self.enemy_group.draw(self.screen)

        self.hero_group.update(self,1)
        self.hero_group.draw(self.screen)

        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

        self.life_group.update()
        self.life_group.draw(self.screen)

        self.blast_group.update()
        self.blast_group.draw(self.screen)

        #  动态添加分数
        self.drawText()

    def drawText(self):
        game_font = pygame.font.SysFont('SimHei',30)  # 字体
        # 绘制游戏得分
        self.screen.blit(game_font.render('当前得分：%d' % self.hero.score, True, [255, 0, 0]), [20, 20])
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
    # plane.start_game()
