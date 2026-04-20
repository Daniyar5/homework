import flet as ft
from ui import UI

class ProfileApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Анкеты'
        self.page.window_width = 500
        self.page.window_height = 500

        self.ui = UI()

        self.build_event()
        self.page.add(*self.ui.build())
    
    def build_event(self):
        self.ui.button.on_click = self.create_profile
        self.ui.age.on_change = self.update_age
    
    def update_age(self, e):
        self.ui.age_text.value = f'Возраст: {int(self.ui.age.value)}'
        self.page.update()
    
    def create_profile(self, e):
        skills = []

        if self.ui.skill1.value:
            skills.append("Python")
        if self.ui.skill2.value:
            skills.append("Django")
        if self.ui.skill3.value:
            skills.append("Flet")
        
        self.ui.result.value = (
            f'Имя: {self.ui.name.value}\n'
            f'Город: {self.ui.city.value}\n'
            f'Возраст: {self.ui.age.value}\n'
            f'Навыки: {", ".join(skills)}\n'
            f'Уровень: {self.ui.level.value}\n'
            f'Готов к работе: {"Да" if self.ui.active.value else "Нет"}'
        )

        self.page.update()