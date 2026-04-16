import flet as ft
import flet_audio as fta # <--- 1. ДОБАВЛЯЕМ НОВЫЙ ИМПОРТ
import asyncio
import math
from game import Game
from ui import UI

class RouletteApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Русская рулетка'
        self.page.window_width = 500
        self.page.window_height = 600
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        
        # 2. МЕНЯЕМ ft.Audio НА fta.Audio
        self.shoot_sound = fta.Audio(src="shoot.mp3", autoplay=False)
        self.page.overlay.append(self.shoot_sound)

        # Настраиваем игру: 3 жизни, 2 пули
        self.game = Game(lives=3, bullets_count=2)
        self.ui = UI()

        self.bind_events()
        self.page.add(*self.ui.build())
        self.update_lives_ui()
    
    def bind_events(self):
        self.ui.shoot_btn.on_click = self.shoot
        self.ui.reset_btn.on_click = self.restart
    
    def update_lives_ui(self):
        # Рисуем полные и пустые сердца в зависимости от количества жизней
        hearts = "❤️" * self.game.lives
        lost_hearts = "🖤" * (self.game.max_lives - self.game.lives)
        self.ui.lives.value = f"Жизни: {hearts}{lost_hearts}"

    async def animate_drum(self):
        # Плавная анимация: прибавляем 360 градусов (2 Пи)
        self.ui.drum.rotate.angle += math.pi * 2
        self.page.update()
        await asyncio.sleep(0.5) # Ждем пока проиграется анимация
    
    async def shoot(self, e):
        # Проверки перед выстрелом
        if not self.game.alive:
            return
        if self.game.current_position > 6:
            self.ui.status.value = "Барабан пуст! Жми перезарядку."
            self.ui.status.color = "black"
            self.page.update()
            return

        self.ui.shoot_btn.disabled = True # Блокируем кнопку, чтобы не кликали дважды
        self.page.update()

        await self.animate_drum()
        result = self.game.shot()

        if result == "boom":
            self.shoot_sound.play() # Проигрываем звук
            self.ui.drum.src = "blast.png" # Меняем на картинку взрыва
            self.ui.status.value = "🧨 БАМ! Минус жизнь"
            self.ui.status.color = "red"
            self.update_lives_ui()

            if not self.game.alive:
                self.show_dialog("Игра окончена 🎈", "У вас закончились жизни!")
        else:
            self.ui.drum.src = "gun.png"
            self.ui.status.value = "😅 Повезло!"
            self.ui.status.color = 'green'
        
        self.ui.round.value = f'Выстрел: {self.game.current_position - 1}/6'
        self.ui.shoot_btn.disabled = False
        self.page.update()

        # Если в нас попали, но мы живы - возвращаем картинку револьвера через секунду
        if result == "boom" and self.game.alive:
            await asyncio.sleep(1.2)
            self.ui.drum.src = "gun.png"
            self.page.update()
    
    def restart(self, e):
        self.game.reset()
        self.update_lives_ui()
        self.ui.status.value ="Нажми на кнопку выстрел"
        self.ui.status.color = "black"
        self.ui.round.value ="Камора: 1/6"
        self.ui.drum.src = "gun.png"
        
        # Сброс угла поворота барабана
        self.ui.drum.rotate.angle = 0
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
        self.restart(None) # Автоматически перезапускаем после закрытия диалога
        self.page.update()