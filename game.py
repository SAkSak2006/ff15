import pygame
import sys
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random
from tkinter import Tk, Button, messagebox

# Инициализация Pygame
pygame.init()

# Переменная для контроля состояния игры
game_running = False
app = None  # Переменная для хранения приложения Ursina

def start_ursina_app():
    global app
    if app is None:  # Инициализируем приложение только один раз
        app = Ursina(fullscreen=False)
        Entity.default_shader = lit_with_shadows_shader

def run_game():
    global game_running
    game_running = True  # Обновляем состояние

    # Создаем землю и игрока
    ground = Entity(model='plane', collider='box', scale=640, texture="gltf_embedded_2.jpeg")
    player = FirstPersonController(model="sakcok.obj", texture='GT-Rgoldsand.png', scale=1, origin_y=-.5, z=-10)
    player.speed = 120
    player.jumping = 100
    player.camera_pivot.z = -8.5
    player.camera_pivot.y = 4.5
    player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(3, 3, 3))
    player.collider.visible = True

    def generate_trees():
        num_trees = 200
        ground_size = ground.scale * 0.5
        for i in range(num_trees):
            x = random.uniform(-ground_size[0], ground_size[0])
            z = random.uniform(-ground_size[2], ground_size[2])
            height = random.uniform(2, 3)

            tree = Entity(model='tree3.obj', origin_y=-.5, scale=(0.5, height, 0.5), texture="brick", x=x, z=z, collider='box')
            collider = Entity(model='cube', scale=(0.5, height, 0.5), color=color.red, x=x, z=z, y=(height / 2) - 0.5)
            collider.collider = BoxCollider(collider, Vec3(0, height / 2, 0), Vec3(1, height, 1))

        sun = DirectionalLight()
        sun.look_at(Vec3(1, -1, -1))
        Sky()

    generate_trees()

def toggle_menu():
    global game_running
    if game_running:
        app.paused = True  # Останавливаем игру
        game_running = False
        show_menu()  # Открываем меню

def show_menu():
    menu = Tk()
    menu.title("Меню")
    menu.geometry("300x300")

    def start_game():
        global game_running
        game_running = True
        menu.destroy()  # Закрыть меню
        app.paused = False  # Продолжить игру

    def select_car():
        messagebox.showinfo("Выбор машины", "Здесь вы можете выбрать машину.")

    def select_map():
        messagebox.showinfo("Выбор карты", "Здесь вы можете выбрать карту.")

    def settings():
        messagebox.showinfo("Настройки", "Здесь вы можете изменить настройки.")

    def exit_game():
        global game_running
        game_running = False
        pygame.quit()
        sys.exit()

    Button(menu, text="Продолжить игру", command=start_game).pack(pady=5)
    Button(menu, text="Выбор машины", command=select_car).pack(pady=5)
    Button(menu, text="Выбор карты", command=select_map).pack(pady=5)
    Button(menu, text="Настройки", command=settings).pack(pady=5)
    Button(menu, text="Выход", command=exit_game).pack(pady=5)

    menu.mainloop()  # Запускаем цикл меню

def update():
    if held_keys['escape']:  # Если нажата клавиша ESC
        toggle_menu()  # Открываем меню

# Основной запуск приложения
start_ursina_app()
run_game()

# Запуск основного цикла приложения только один раз
app.run()
