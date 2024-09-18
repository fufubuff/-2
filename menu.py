import pygame
import sys

class MainMenu:
    def __init__(self, game):
        self.game = game
        self.options = ["Start Game", "Settings", "Quit"]
        self.selected_option = None
        self.font = pygame.font.SysFont('Arial', 40)

        # 加载背景图
        self.background = pygame.image.load('背景.png')  # 确保背景图路径正确
        self.background = pygame.transform.scale(self.background, (self.game.window.get_width(), self.game.window.get_height()))

        # 加载并缩放按钮图片，等比例缩小
        self.button_images = {
            #"Start Game":self.scale_image('start.png', 150, 60),
            "Start Game": pygame.transform.scale(pygame.image.load('start.png').convert_alpha(), (200, 80)), 
            "Settings": pygame.transform.scale(pygame.image.load('set.png').convert_alpha(), (200, 80)), 
            "Quit": pygame.transform.scale(pygame.image.load('quit.png').convert_alpha(), (200, 80)), 
            #"Settings": self.scale_image('set.png', 150, 60),  # 等比例缩小
            
            #"Quit": self.scale_image('quit.png', 150, 60)  # 等比例缩小
        }
        button_spacing = 100  # 你可以根据需要调整这个值
        window_center_x = self.game.window.get_width() // 2
        start_y = self.game.window.get_height() // 2.5  # 开始位置设置为页面高度的1/3

        self.button_rects = {
        "Start Game": self.button_images["Start Game"].get_rect(center=(window_center_x, start_y)),  # 第一个按钮位于1/3处
        "Settings": self.button_images["Settings"].get_rect(center=(window_center_x, start_y + button_spacing)),  # 第二个按钮在第一个按钮下方一个间距
        "Quit": self.button_images["Quit"].get_rect(center=(window_center_x, start_y + 2 * button_spacing))  # 第三个按钮在第二个按钮下方一个间距
        }
        # 按钮的矩形区域（用于检测鼠标点击）
    def display_rules(self):
        """显示规则图片"""
        rules_image = pygame.image.load('rules.png')  # 加载规则图片
        rules_image = pygame.transform.scale(rules_image, (self.game.window.get_width(), self.game.window.get_height()))
        self.game.window.blit(rules_image, (0, 0))
        pygame.display.flip()

    def wait_for_rules_acknowledgment(self):
        """等待用户点击以确认阅读规则"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # 点击鼠标左键确认
                    if event.button == 1:
                        waiting = False

    def scale_image(self, img_path, max_width, max_height):
        """等比例缩小图片"""
        img = pygame.image.load(img_path).convert_alpha()
        width, height = img.get_size()
        aspect_ratio = width / height
        if width > height:
            new_width = min(max_width, width)
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = min(max_height, height)
            new_width = int(new_height * aspect_ratio)
        return pygame.transform.scale(img, (new_width, new_height))

    def display_menu(self):
        """绘制主菜单"""
        self.game.window.blit(self.background, (0, 0))  # 绘制背景
        for option in self.options:
            self.game.window.blit(self.button_images[option], self.button_rects[option])  # 绘制按钮
        pygame.display.flip()

    def handle_input(self):
        """处理鼠标输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    for option in self.options:
                        if self.button_rects[option].collidepoint(event.pos):  # 检测鼠标是否点击在按钮上
                            self.select_option(option)


    def select_option(self, option):
        """根据选项执行操作"""
        if option == "Start Game":
            self.display_rules()  # 显示游戏规则
            self.wait_for_rules_acknowledgment() 
            self.game.new()
            self.game.playing = True
        elif option == "Settings":
            self.game.settings_menu = SettingsMenu(self.game)  # 显示设置菜单
            self.game.settings_menu.display_menu()
        elif option == "Quit":
            self.game.quit_menu = QuitMenu(self.game)  # 显示退出确认页面
            self.game.quit_menu.display_quit_page()
class PauseMenu:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.SysFont('Arial', 40)
        self.options = ["Continue", "Main Menu"]
        self.selected_option = None

        # 暂停菜单的背景和按钮
        self.background = pygame.Surface(self.game.window.get_size())
        self.background.set_alpha(128)  # 半透明背景
        self.background.fill((0, 0, 0))  # 黑色背景
        self.button_images = {
            "Continue": pygame.transform.scale(pygame.image.load('continue.png').convert_alpha(), (200, 80)),
            "Main Menu": pygame.transform.scale(pygame.image.load('main_menu.png').convert_alpha(), (200, 80))
        }

        self.button_rects = {
            "Continue": self.button_images["Continue"].get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 - 50)),
            "Main Menu": self.button_images["Main Menu"].get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() // 2 + 50))
        }

    def display_menu(self):
        self.game.window.blit(self.background, (0, 0))  # 绘制半透明背景
        for option in self.options:
            self.game.window.blit(self.button_images[option], self.button_rects[option])
        pygame.display.flip()

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for option in self.options:
                    if self.button_rects[option].collidepoint(event.pos):
                        self.select_option(option)

    def select_option(self, option):
        if option == "Continue":
            self.game.paused = False
        elif option == "Main Menu":
            self.game.running = False
            MainMenu(self.game)  # 重新显示主菜单
class SettingsMenu:
    """设置菜单"""
    def __init__(self, game):
        self.game = game
        self.settings_options = ["Sound", "Graphics", "Back"]
        self.selected_option = None
        self.font = pygame.font.SysFont('Arial', 40)

        # 加载背景图
        self.background = pygame.image.load('settings_background.png')  # 加载设置背景图
        self.background = pygame.transform.scale(self.background, (self.game.window.get_width(), self.game.window.get_height()))

        # 加载按钮图片
        self.sound_button_image = pygame.image.load('sound.png').convert_alpha()  # 加载Sound按钮图片
        self.sound_button_image = pygame.transform.scale(self.sound_button_image, (100, 50))
        self.graphics_button_image = pygame.image.load('graphics.png').convert_alpha()  # 加载Graphics按钮图片
        self.graphics_button_image = pygame.transform.scale(self.graphics_button_image, (100, 50))
        self.back_button_image = pygame.image.load('back.png').convert_alpha()  # 加载Back按钮图片
        self.back_button_image = pygame.transform.scale(self.back_button_image, (100, 50))

        # 计算每个按钮的位置，使它们在页面底部均匀排布
        screen_width = self.game.window.get_width()
        screen_height = self.game.window.get_height()
        spacing = screen_width // 4  # 按钮之间的间隔

        self.button_rects = {
            "Sound": self.sound_button_image.get_rect(center=(spacing, screen_height - 50)),
            "Graphics": self.graphics_button_image.get_rect(center=(spacing * 2, screen_height - 50)),
            "Back": self.back_button_image.get_rect(center=(spacing * 3, screen_height - 50))
        }

    def display_menu(self):
        """显示设置菜单"""
        self.game.window.blit(self.background, (0, 0))  # 绘制设置背景

        # 绘制底部的按钮
        for option in self.settings_options:
            if option == "Sound":
                self.game.window.blit(self.sound_button_image, self.button_rects[option])
            elif option == "Graphics":
                self.game.window.blit(self.graphics_button_image, self.button_rects[option])
            elif option == "Back":
                self.game.window.blit(self.back_button_image, self.button_rects[option])

        pygame.display.flip()

        # 进入事件循环，等待玩家选择
        self.wait_for_input()

    def wait_for_input(self):
        """等待用户输入，处理back按钮点击"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 鼠标左键点击
                        for option in self.settings_options:
                            if self.button_rects[option].collidepoint(event.pos):
                                self.select_option(option)
                                if option == "Back":
                                    waiting = False  # 点击back时退出循环，返回主菜单

    def select_option(self, option):
        """处理设置菜单选项"""
        if option == "Back":
            return  # 返回主菜单
        elif option == "Sound":
            print("Sound settings")  # 可以实现声音设置逻辑
        elif option == "Graphics":
            print("Graphics settings")  # 可以实现图像设置逻辑
class QuitMenu:
    """退出确认菜单"""
    def __init__(self, game):
        self.game = game
        self.quit_background = pygame.image.load('quit_confirm.png')  # 加载确认退出的背景图
        self.back_button_image = pygame.image.load('back.png').convert_alpha()  # 加载返回按钮
        self.back_button_image = pygame.transform.scale(self.back_button_image, (100, 50))
        self.back_button_rect = self.back_button_image.get_rect(center=(self.game.window.get_width() // 2, self.game.window.get_height() - 50))

    def display_quit_page(self):
        """显示确认退出的页面，并平铺背景"""
        for x in range(0, self.game.window.get_width(), self.quit_background.get_width()):
            for y in range(0, self.game.window.get_height(), self.quit_background.get_height()):
                self.game.window.blit(self.quit_background, (x, y))

        # 绘制back按钮
        self.game.window.blit(self.back_button_image, self.back_button_rect)
        pygame.display.flip()

        # 进入事件循环，等待玩家确认退出或返回主菜单
        self.wait_for_input()

    def wait_for_input(self):
        """等待用户输入，处理back按钮点击"""
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 鼠标左键点击
                        if self.back_button_rect.collidepoint(event.pos):
                            waiting = False  # 结束等待，返回主菜单
