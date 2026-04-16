import flet as ft
import asyncio
from game import Game
from ui import UI

class RouletteApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Русская рулетка'
        self.page.window_width = 400
        self.page.window_height = 650
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # 3 жизни, 2 пули в барабане
        self.game = Game(lives=3, bullets=2)
        self.ui = UI()

        # Добавляем звуки (ссылки на публичные эффекты, можно заменить на локальные файлы)
        self.shot_sound = ft.Audio(src="https://actions.google.com/sounds/v1/weapons/gunshot.ogg", autoplay=False)
        self.empty_sound = ft.Audio(src="https://actions.google.com/sounds/v1/tools/ratchet_wrench.ogg", autoplay=False)
        self.page.overlay.extend([self.shot_sound, self.empty_sound])

        self.bind_events()
        self.page.add(*self.ui.build())
        self.update_lives_ui()
    
    def bind_events(self):
        self.ui.shoot_btn.on_click = self.shoot
        self.ui.reset_btn.on_click = self.restart

    def update_lives_ui(self):
        # Отрисовка сердечек: целые и потерянные
        self.ui.lives.value = "❤️" * self.game.lives + "🖤" * (self.game.max_lives - self.game.lives)
        self.page.update()
    
    async def animate_drum(self):
        # Отключаем кнопку во время анимации
        self.ui.shoot_btn.disabled = True
        self.ui.drum.src = "https://img.icons8.com/color/256/revolver.png"
        self.page.update()

        # Плавная анимация вращения с помощью async
        for i in range(1, 15):
            self.ui.drum.rotate.angle = i * 0.5  # Вращаем картинку
            self.page.update()
            await asyncio.sleep(0.04) # Не блокирует интерфейс!
        
        self.ui.drum.rotate.angle = 0
    
    async def shoot(self, e):
        if not self.game.alive:
            return
            
        await self.animate_drum()
        result = self.game.shot()

        if result == "fatal_boom":
            self.shot_sound.play()
            self.ui.drum.src = "https://img.icons8.com/color/256/skull.png" # Картинка черепа
            self.ui.status.value ="🧨 BOOM! ИГРА ОКОНЧЕНА"
            self.ui.status.color = "red"
            self.show_dialog("Конец игры 🎈", "Вы потеряли все жизни!")
        elif result == "boom":
            self.shot_sound.play()
            self.ui.drum.src = "https://img.icons8.com/color/256/explosion.png" # Картинка взрыва
            self.ui.status.value = "💥 Попадание! Минус жизнь."
            self.ui.status.color = "orange"
            self.ui.shoot_btn.disabled = False
        else:
            self.empty_sound.play()
            self.ui.status.value = "😅 Повезло! Холостой."
            self.ui.status.color = 'green'
            self.ui.shoot_btn.disabled = False

        self.update_lives_ui()
        self.ui.round.value = f'Раунд: {self.game.current_position}'
        self.page.update()
    
    def restart(self, e):
        self.game.reset()
        self.ui.status.value ="Нажми на кнопку выстрел"
        self.ui.status.color = "white"
        self.ui.round.value ="Раунд: 1"
        self.ui.drum.src = "https://img.icons8.com/color/256/revolver.png"
        self.ui.shoot_btn.disabled = False
        self.update_lives_ui()
        self.page.update()
    
    def show_dialog(self, title, message):
        dlg = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=lambda e: self.close_dialog())
            ],
        )
        self.page.dialog = dlg
        dlg.open = True
        self.page.update()
    
    def close_dialog(self):
        self.page.dialog.open = False
        self.page.update()