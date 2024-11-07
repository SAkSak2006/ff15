import pygame
import sys
from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
from ursina.shaders import lit_with_shadows_shader
import random
from tkinter import Tk, Button, messagebox

# Initialize Pygame
pygame.init()

# Game state variables
game_running = False
app = None

# Main Menu function
def show_main_menu():
    main_menu = Tk()
    main_menu.title("Главное меню")
    main_menu.geometry("300x300")

    def start_game():
        main_menu.destroy()
        start_ursina_app()
        run_game()

    def open_settings():
        messagebox.showinfo("Настройки", "Это меню настроек.")

    def exit_game():
        pygame.quit()
        sys.exit()

    Button(main_menu, text="Начать игру", command=start_game).pack(pady=5)
    Button(main_menu, text="Настройки", command=open_settings).pack(pady=5)
    Button(main_menu, text="Выход", command=exit_game).pack(pady=5)

    main_menu.mainloop()

def start_ursina_app():
    global app
    if app is None:
        app = Ursina(fullscreen=False)
        Entity.default_shader = lit_with_shadows_shader

def run_game():
    global game_running
    game_running = True

    ground = Entity(model='rotikmanal.glb', collider='box', scale=1, texture="gltf_embedded_2.jpeg")
    player = Player(model="sakcok.obj", texture='GT-Rgoldsand.png', scale=1, origin_y=-.5, z=-10)
    player.speed = 120
    player.jumping = 100
    player.camera_pivot.z = -8.5
    player.camera_pivot.y = 7.5
    player.collider = BoxCollider(player, Vec3(0, 1, 0), Vec3(3, 3, 3))
    player.collider.visible = True

    camera_controller = ThirdPersonCamera(target=player, distance=10)

    def generate_trees():
        num_trees = 0
        ground_size = ground.scale * 1
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
        app.paused = True
        game_running = False
        show_in_game_menu()

def show_in_game_menu():
    in_game_menu = Tk()
    in_game_menu.title("Меню во время игры")
    in_game_menu.geometry("300x300")

    def resume_game():
        in_game_menu.destroy()
        app.paused = False

    def exit_to_main_menu():
        global game_running
        game_running = False
        app.quit()  # Завершаем Ursina
        in_game_menu.destroy()
        show_main_menu()

    Button(in_game_menu, text="Продолжить игру", command=resume_game).pack(pady=5)

    in_game_menu.mainloop()

def update():
    if held_keys['escape']:
        toggle_menu()

class ThirdPersonCamera(Entity):
    def __init__(self, target, **kwargs):
        super().__init__()
        self.target = target
        self.distance = 20
        self.camera_pivot = Entity(parent=self, position=(0, 2, 0))
        camera.parent = self.camera_pivot
        camera.position = (0, 0, -self.distance)
        camera.look_at(self.target)
        camera.fov = 110

        # Чувствительность мыши
        self.mouse_sensitivity = Vec2(120, 120)

        # Добавляем параметры из kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        # Вращаем камеру только при удерживании средней кнопки мыши
        if held_keys['middle mouse']:
            mouse_movement = Vec2(mouse.velocity[0], mouse.velocity[1]) * self.mouse_sensitivity
            self.camera_pivot.rotation_y += mouse_movement.x
            self.camera_pivot.rotation_x -= mouse_movement.y

            # Ограничиваем вертикальный угол обзора камеры
            self.camera_pivot.rotation_x = clamp(self.camera_pivot.rotation_x, -30, 30)

        # Обновляем положение камеры относительно игрока
        self.position = self.target.position

class Player(Entity):
    def __init__(self, **kwargs):
        super().__init__()
        self.model = 'cube'
        self.texture = 'white_cube'
        self.scale = (1, 1, 1)
        self.origin_y = 0
        self.collider = 'box'
        self.speed = 5
        self.turn_speed = 120

        # Добавляем камеру-пивот для управления вращением камеры вокруг игрока
        self.camera_pivot = Entity(parent=self, position=(0, 2, 0))

        # Добавляем параметры из kwargs
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self):
        if held_keys['a']:
            self.rotation_y -= self.turn_speed * time.dt
        elif held_keys['d']:
            self.rotation_y += self.turn_speed * time.dt

        move_direction = Vec3(0, 0, 0)
        if held_keys['w']:
            move_direction += self.forward
        if held_keys['s']:
            move_direction -= self.forward

        self.position += move_direction * time.dt * self.speed

# Start the main menu first
show_main_menu()
run_game()
app.run()
