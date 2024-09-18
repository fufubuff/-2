import pygame
import sys
from game import Game
from menu import MainMenu,PauseMenu  # 导入菜单类

def init_game():
    """初始化游戏"""
    pygame.init()
    game = Game()
    return game

def run_main_menu(game):
    """主菜单循环"""
    main_menu = MainMenu(game)
    while not game.playing:  # 只要游戏还没开始，保持显示主菜单
        main_menu.handle_input()  # 处理鼠标点击
        main_menu.display_menu()  # 显示主菜单

def run_game_loop(game):
    """游戏主循环"""
    while game.running:  # 游戏循环持续运行
        game.run()  # 调用Game类中的run方法，启动游戏
        if not game.playing:
            # 游戏结束后返回主菜单
            run_main_menu(game)

def quit_game():
    """退出游戏"""
    pygame.quit()

if __name__ == '__main__':
    game = init_game()  # 初始化游戏
    run_main_menu(game)  # 启动主菜单
    try:
        run_game_loop(game)  # 运行游戏主循环
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        quit_game()  # 确保退出游戏并释放资源
