import pygame
import os
import sys
import random
from settings import WIDTH, HEIGHT, FPS, WHITE, BLACK, PINK
from menu import PauseMenu,MainMenu

class Game:
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        self.font_name = pygame.font.get_default_font()
        self.clock = pygame.time.Clock()
        self.selected_tiles = []  # 盘子中的图块
        self.score = 0
        self.time_left = 60
        self.highlight_color = PINK
        self.all_tiles = []  # 碗中的图块
        self.mouse_pos = (0, 0)  # 跟踪鼠标位置
        self.background_image = pygame.image.load('background.png')
        self.background_image = pygame.transform.scale(self.background_image, (WIDTH, HEIGHT))
        self.level = 1  # 当前关卡
        self.frozen_chance = 0  # 冰块生成的概率，第一关为0%
        self.margin = 50
        self.main_menu = MainMenu(self)
        
        # 调整碗的大小为原来的2/3
        self.bowl_image = pygame.image.load('碗.png')
        original_bowl_width, original_bowl_height = self.bowl_image.get_size()
        self.bowl_image = pygame.transform.scale(self.bowl_image, (original_bowl_width * 1// 2, original_bowl_height * 1 // 2))
        self.bowl_rect = self.bowl_image.get_rect()
        self.bowl_rect.center = (WIDTH // 2, HEIGHT * 3 // 4)  # 调整碗的center Y值，使其位于页面下方
        
        # 碗的位置确保有边
        self.bowl_rect.top = max(self.margin, self.bowl_rect.top)  # 确保顶部有边距
        self.bowl_rect.bottom = min(HEIGHT - self.margin, self.bowl_rect.bottom)   # 确保底部有边距
# 在__init__方法中添加暂停按钮的初始化
        self.pause_button_image = pygame.image.load('pause_button.png').convert_alpha()  # 加载图片
        self.pause_button_image = pygame.transform.scale(self.pause_button_image, (100, 50))  # 缩放到合适的大小
        self.pause_button_rect = self.pause_button_image.get_rect()
        self.pause_button_rect.bottomright = (WIDTH - 10, HEIGHT - 10)  # 放置在窗口的右下角

        
        self.plate_image = pygame.image.load('盘.png')
        self.plate_image = pygame.transform.scale(self.plate_image, (WIDTH // 3, HEIGHT // 4))
        self.plate_rect = self.plate_image.get_rect(center=(WIDTH // 2, HEIGHT // 6))

        
        self.load_data()
        pygame.mixer.init()
        pygame.mixer.music.load('background_music.mp3')
        pygame.mixer.music.play(-1)
    def next_level(self):
        self.level += 1
        self.frozen_chance = 10 * self.level
    def load_data(self):
        self.tiles = []
        self.tile_types = {}
        tile_path = 'tiles'
        for img_file in os.listdir(tile_path):
            if img_file.endswith('.png'):
                img = pygame.image.load(os.path.join(tile_path, img_file)).convert_alpha()
                img = pygame.transform.scale(img, (80, 80))  # 将图块的大小调整为80x80
                tile_type = img_file.split('.')[0]
                if tile_type not in self.tile_types:
                    self.tile_types[tile_type] = img
                # 如果是普通图块，加入到 tiles 列表
                if not tile_type.endswith('f'):
                    self.tiles.append((tile_type, img))
        self.sound_effect = pygame.mixer.Sound('effect.mp3')

    def new(self):
        """初始化新游戏"""
        self.all_tiles = self.generate_initial_layout(20, 30)
        self.playing = True
        self.score = 0
        self.selected_tiles = []
        self.time_left = 60  # 确保重新开始时，时间被重置到初始值
        self.level = 1 

    def generate_initial_layout(self, min_tiles, max_tiles):
        tiles=[]
        for tile_type, tile_img in self.tiles:
        # 每张图生成20到30个
            num_tiles = random.randint(min_tiles, max_tiles)
            for _ in range(num_tiles):
                while True:
                # 确保图块与图块大小相适应的随机位置生成在碗的范围内
                    x = random.randint(self.bowl_rect.left, self.bowl_rect.right - 80)  # 调整边界以适应新的图块大小
                    y = random.randint(self.bowl_rect.top, self.bowl_rect.bottom - 80)
                    if random.randint(0, 100) < self.frozen_chance:
                        frozen_tile_type = tile_type + 'f'  # 冰冻状态图块以f结尾
                        frozen_tile_img = self.tile_types[frozen_tile_type]  # 获取冰冻状态的图块图片
                        tiles.append((frozen_tile_type, frozen_tile_img, x, y, (x, y))) # 生成冰冻图块
                    else:
                        tiles.append((tile_type, tile_img, x, y))  # 生成普通图块

                    break
        return tiles

    def show_time_up_screen(self):
    # 加载时间结束图片
        time_up_image = pygame.image.load('time_up.png')
        time_up_image = pygame.transform.scale(time_up_image, (WIDTH, HEIGHT))
        time_up_rect = time_up_image.get_rect(topleft=(0, 0))  # 图片居中显示

    # 显示时间结束的图片
        self.window.blit(time_up_image, time_up_rect)

    # 加载返回主菜单按钮
        back_button_image = pygame.image.load('back.png').convert_alpha()  # 返回主菜单按钮图片
        back_button_image = pygame.transform.scale(back_button_image, (200, 80))  # 调整按钮大小
        back_button_rect = back_button_image.get_rect(center=(WIDTH // 2, HEIGHT - 100))  # 按钮位置

    # 显示返回按钮
        self.window.blit(back_button_image, back_button_rect)

        pygame.display.update()

    # 等待玩家点击返回主菜单按钮
        self.wait_for_menu_click(back_button_rect)
    def run(self):
        """主游戏循环"""
        while self.running:
            if not self.playing:
                self.show_main_menu()  # 显示主菜单
            else:
                self.play_game_loop()

    def play_game_loop(self):
        """游戏内循环"""
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw(self.window)

            
    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.pause_button_rect.collidepoint(event.pos):  # 检查是否点击了暂停按钮
                    self.playing = not self.playing  # 切换游戏的暂停状态
                else:
                    self.handle_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos

    def handle_click(self, pos):
        if len(self.selected_tiles) < 5:  # 盘子容量为5
            selected = False  # 用来确保只选中一个图块
        # 逆序遍历，确保优先选择最上面的图块
            for tile in reversed(self.all_tiles):
            # 检查图块的长度
                if len(tile) == 4:  # 普通图块
                    tile_type, tile_img, x, y = tile  # 解包普通图块
                    original_position = None  # 普通图块没有 original_position
                elif len(tile) == 5:  # 冰冻图块
                    tile_type, tile_img, x, y, original_position = tile
                else:
                    raise ValueError(f"Unexpected tile length: {len(tile)}")

            # 检查是否点击在图块上
                tile_rect = pygame.Rect(x, y, 80, 80)  # 确保矩形大小和图块大小一致
                if tile_rect.collidepoint(pos):
                    if tile_type.endswith('f'):  # 如果是冰冻图块
                    # 冰冻图块移动到盘子中，并保留原始位置
                        current_tile = (tile_type, tile_img, x, y, original_position)
                    else:
                    # 普通图块移动到盘子
                        current_tile = (tile_type, tile_img, x, y)

                # 将图块添加到盘子并从碗中移除
                    self.selected_tiles.append(current_tile)
                    self.all_tiles.remove(tile)
                    self.rearrange_tiles()  # 重新排列盘子里的图块

                    if len(self.selected_tiles) >= 3:
                        self.check_match()  # 检查是否有3个相同的图块
                    selected = True  # 已经选中了图块，跳出循环
                    break



    def check_match(self):
        print("Before match check:", self.selected_tiles)  # 打印当前选中的图块
        if len(self.selected_tiles) >= 3:
            # 统计每种图块的数量，包括冰冻状态的图块
            tile_count = {}
            for tile in self.selected_tiles:
                tile_type = tile[0].rstrip('f')  # 去掉'f'后缀以便统计同类型图块
                if tile_type in tile_count:
                    tile_count[tile_type] += 1
                else:
                    tile_count[tile_type] = 1

            matched = False
            for tile_type, count in tile_count.items():
                if count >= 3:
                    frozen_tiles = []
                    normal_tiles = []

                    for tile in self.selected_tiles:
                        if tile[0].rstrip('f') == tile_type:
                            if len(tile) == 5:  # 冰冻图块
                                frozen_tiles.append(tile)
                            else:
                                normal_tiles.append(tile)

                        if len(frozen_tiles) + len(normal_tiles) == 3:
                            break

                    # 如果找到了三个冰冻图块，解冻并返回原位置
                    if len(frozen_tiles) == 3:
                        print("Unfreezing tiles:", frozen_tiles)
                        self.unfreeze_and_return_tiles(frozen_tiles)
                        matched = True
                        break

                    # 如果找到普通图块，进行消除
                    elif len(normal_tiles) + len(frozen_tiles) >= 3:
                        tiles_to_remove = normal_tiles + frozen_tiles
                        print("Attempting to remove:", tiles_to_remove)
                        self.animate_overlap_and_disappear(tiles_to_remove)

                        # 从已选中的图块列表中移除这些图块
                        self.selected_tiles = [tile for tile in self.selected_tiles if tile not in tiles_to_remove]
                        self.score += 1
                        matched = True
                        break

            # 如果盘子已满且没有匹配，游戏结束
            if len(self.selected_tiles) == 5 and not matched:
                print("Game Over: No more possible matches!")
                self.show_failure_screen()
        #if not self.all_tiles and not self.selected_tiles:  # 确认所有图块都已消除
            #self.show_success_screen()
        if self.score >= 10 * self.level:  # 假设每关的目标分数是10乘以当前关卡数
            self.show_success_screen()
    def unfreeze_and_return_tiles(self, frozen_tiles):
        for idx, tile in enumerate(frozen_tiles):
            if len(tile) == 5:
                tile_type, tile_img, x, y, original_position = tile  # 取出原始位置
                original_x, original_y = original_position  # 取出原始的 x 和 y

            # 去掉'f'后缀，将图块变为普通状态
                unfrozen_tile_type = tile_type.rstrip('f')
                unfrozen_tile_img = self.tile_types[unfrozen_tile_type]

            # 返回到碗中的原始位置
                self.all_tiles.append((unfrozen_tile_type, unfrozen_tile_img, original_x, original_y))

    # 从盘子中移除解冻的图块
        self.selected_tiles = [tile for tile in self.selected_tiles if tile not in frozen_tiles]

    # 重新排列碗中的图块
        self.rearrange_tiles()


    def show_success_screen(self):
        # 加载通过关卡的图片
        success_image = pygame.image.load('success.png')
        success_image = pygame.transform.scale(success_image, (WIDTH, HEIGHT))
        success_rect = success_image.get_rect(topleft=(0, 0))  # 居中显示

        # 显示通过关卡的图片
        self.window.blit(success_image, success_rect)

        # 加载“下一关”按钮
        next_button_image = pygame.image.load('next_button.png').convert_alpha()
        next_button_image = pygame.transform.scale(next_button_image, (200, 80))  # 按钮大小
        next_button_rect = next_button_image.get_rect(center=(WIDTH // 2, HEIGHT - 100))  # 居中显示按钮

        # 显示按钮
        self.window.blit(next_button_image, next_button_rect)

        pygame.display.update()

        # 等待玩家点击“下一关”按钮
        self.wait_for_next_level(next_button_rect)
    def wait_for_next_level(self, next_button_rect):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                    self.running = False
                    waiting = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if next_button_rect.collidepoint(event.pos):
                        self.next_level()  # 进入下一关# 开始新关卡
                        waiting = False
    def next_level(self):
        self.level += 1
        self.frozen_chance = 10 * self.level  # 随着关卡增加冰块生成几率
        self.all_tiles = self.generate_initial_layout(20, 30)  # 生成新的图块布局
        self.selected_tiles = []  # 清空已选图块
        self.time_left = max(10, self.time_left - 10)
        self.score = 0  # 重置分数
    def show_failure_screen(self):
    # 加载失败图片
        failure_image = pygame.image.load('失败.png')
        failure_image = pygame.transform.scale(failure_image, (WIDTH , HEIGHT ))
        failure_rect = failure_image.get_rect(topleft=(0, 0))  # 图片居中

    # 绘制失败图片
        self.window.blit(failure_image, failure_rect)

    # 返回主菜单按钮
        back_button_image = pygame.transform.scale(pygame.image.load('back.png').convert_alpha(), (200, 80))  # 缩放图片大小为(200, 80)
        back_button_image.get_rect()  # 获取按钮图片的尺寸
        back_button_rect = back_button_image.get_rect(center=(WIDTH // 2, HEIGHT - 100))  # 将按钮放置在屏幕底部居中位置

    # 绘制返回按钮
        self.window.blit(back_button_image, back_button_rect)

        pygame.display.update()  # 更新屏幕

    # 等待玩家点击返回按钮
        self.wait_for_menu_click(back_button_rect)
    def show_main_menu(self):
        """显示主菜单并等待用户点击Start Game"""
        self.main_menu.display_menu()
        self.main_menu.handle_input()


    def wait_for_menu_click(self, button_rect):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False  # 停止当前游戏
                    self.running = False  # 停止整个程序
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        if button_rect.collidepoint(event.pos):  # 如果点击的位置在按钮区域内
                            waiting = False  # 停止等待，退出循环
                            self.playing = False  # 停止当前游戏，回到主菜单
            pygame.display.update()
            self.clock.tick(60)                   

    def rearrange_tiles(self):
        for idx, tile in enumerate(self.selected_tiles):
            if len(tile) == 4:  # 普通图块
                tile_type, tile_img, x, y = tile  # 解包普通图块
            elif len(tile) == 5:  # 冰冻图块
                tile_type, tile_img, x, y, original_position = tile  # 解包冰冻图块
            else:
                raise ValueError(f"Unexpected tile length: {len(tile)}")

        # 重新计算新位置
            new_x = self.plate_rect.left + idx * 50
            new_y = self.plate_rect.top + (self.plate_rect.height - 50) // 2
        
        # 根据图块长度重新组合元组
            if len(tile) == 4:  # 普通图块更新位置
                self.selected_tiles[idx] = (tile_type, tile_img, new_x, new_y)
            elif len(tile) == 5:  # 冰冻图块更新位置，但保留 original_position
                self.selected_tiles[idx] = (tile_type, tile_img, new_x, new_y, original_position)

    def draw(self, screen):
    # 绘制背景和主要组件
        screen.blit(self.background_image, (0, 0))
        screen.blit(self.bowl_image, self.bowl_rect)
        screen.blit(self.plate_image, self.plate_rect)
        screen.blit(self.pause_button_image, self.pause_button_rect)

    # 绘制碗中的图块
        hover_tile = None  # 用来保存鼠标悬停的图块信息
        for tile in self.all_tiles:
        # 根据长度解包普通图块或冰冻图块
            if len(tile) == 4:  # 普通图块
                tile_type, tile_img, x, y = tile
            elif len(tile) == 5:  # 冰冻图块
                tile_type, tile_img, x, y, original_position = tile
            else:
                raise ValueError(f"Unexpected tile length: {len(tile)}")

        # 绘制图块
            screen.blit(tile_img, (x, y))

        # 检查是否悬停在图块上
            if pygame.Rect(x, y, 80, 80).collidepoint(self.mouse_pos):
                hover_tile = (tile_img, x, y)  # 记录悬停的图块

    # 如果找到悬停的图块，绘制粉色边框
        if hover_tile:
            tile_img, x, y = hover_tile
            mask = pygame.mask.from_surface(tile_img)
            outline = mask.outline()  # 获取图块的轮廓
            if outline:
                transformed_outline = [(x + point[0], y + point[1]) for point in outline]  # 转换到屏幕坐标
                pygame.draw.polygon(screen, self.highlight_color, transformed_outline, 2)  

    # 绘制盘子中的图块
        for tile in self.selected_tiles:
        # 根据长度解包普通图块或冰冻图块
            if len(tile) == 4:  # 普通图块
                tile_type, tile_img, x, y = tile
            elif len(tile) == 5:  # 冰冻图块
                tile_type, tile_img, x, y, original_position = tile
            else:
                raise ValueError(f"Unexpected tile length: {len(tile)}")

        # 绘制图块
            screen.blit(tile_img, (x, y))

    # 在左下角绘制分数
        self.draw_text(screen, f"Score: {self.score}   ", 30, 100, HEIGHT - 30)
        self.draw_text(screen, f"Time left: {int(self.time_left)}", 30, 250, HEIGHT - 30)

    # 更新显示
        pygame.display.update()
    
    


    
    def update(self):
        """更新游戏状态"""
        self.time_left -= 1 / FPS
        if self.time_left <= 0:
            print("Time's up!")
            self.playing = False
            self.show_time_up_screen()

    def draw_text(self, screen, text, size, x, y):
        """绘制文本"""
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x, y))
        screen.blit(text_surface, text_rect)
        
        
    
    def animate_overlap_and_disappear(self, tiles):
        if not tiles:
            return

    # 获取第一个图块的位置作为目标位置
        target_x, target_y = tiles[0][2], tiles[0][3]

    # 将后面的图块移动到第一个图块的位置
        for tile in tiles[1:]:  # 仅移动除第一个以外的图块
            self.animate_move(tile, (target_x, target_y))

    # 移动完成后，从屏幕和列表中移除所有匹配的图块
        self.remove_tiles(tiles)

    def animate_move(self, tile, target_pos):
        current_x, current_y = tile[2], tile[3]
        target_x, target_y = target_pos

        while (current_x, current_y) != (target_x, target_y):
        # 简单的线性插值移动
            current_x += (target_x - current_x) // 10 or (1 if target_x > current_x else -1)
            current_y += (target_y - current_y) // 10 or (1 if target_y > current_y else -1)
        
        # 更新整个窗口以保持其他部分不变
            self.draw(self.window)
        
        # 绘制移动的图块
            self.window.blit(tile[1], (current_x, current_y))

            pygame.display.update([pygame.Rect(current_x, current_y, tile[1].get_width(), tile[1].get_height())])
            self.clock.tick(FPS)
    
    # 更新图块的最终位置
        tile_idx = self.selected_tiles.index(tile)
        self.selected_tiles[tile_idx] = (tile[0], tile[1], target_x, target_y)

    def remove_tiles(self, tiles):
        for tile in tiles:
            if tile in self.selected_tiles:
                self.selected_tiles.remove(tile)