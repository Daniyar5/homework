import flet as ft
import math

class UI:
    def __init__(self):
        self.title = ft.Text("Русская рулетка", size=26, weight="bold")
        self.status = ft.Text("Крути барабан!", size=20)
        self.round = ft.Text("Выстрел: 0/6", size=16)
        self.lives = ft.Text("Жизни: ❤️❤️❤️", size=20)

       # Изображение револьвера
        self.drum = ft.Image(
            src="gun.png",
            width=150,
            height=150,
            rotate=ft.Rotate(0, alignment=ft.Alignment(0, 0)),
            # БЫЛО: animate_rotation=ft.animation.Animation(500, ft.AnimationCurve.EASE_OUT)
            # СТАЛО (убрали .animation):
            animate_rotation=ft.Animation(500, ft.AnimationCurve.EASE_OUT)
        )

        self.shoot_btn = ft.ElevatedButton("🔫 Выстрел")
        self.reset_btn = ft.ElevatedButton("🔃 Перезарядка")
    
    def build(self):
        return [
            self.title,
            self.lives,
            ft.Container(self.drum, padding=20), # Контейнер для отступов вокруг картинки
            self.status,
            self.round,
            ft.Row([self.shoot_btn, self.reset_btn], alignment=ft.MainAxisAlignment.CENTER)
        ]