import flet as ft
import smtplib
from email.mime.text import MIMEText
from ui import UI

class ProfileApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = 'Анкеты'
        self.page.window_width = 500
        self.page.window_height = 800 
        self.page.theme_mode = ft.ThemeMode.LIGHT 
        self.page.scroll = "auto" 

        self.ui = UI()

        self.page.overlay.append(self.ui.file_picker)

        self.build_event()
        self.page.add(*self.ui.build())
    
    def build_event(self):
        self.ui.button.on_click = self.create_profile
        self.ui.age.on_change = self.update_age
        
        self.ui.theme_switch.on_change = self.change_theme
        self.ui.upload_btn.on_click = lambda _: self.ui.file_picker.pick_files(allow_multiple=False)
        self.ui.file_picker.on_result = self.on_file_picked

    def change_theme(self, e):
        """Меняет тему приложения при переключении свитча"""
        self.page.theme_mode = (
            ft.ThemeMode.DARK 
            if self.ui.theme_switch.value 
            else ft.ThemeMode.LIGHT
        )
        self.page.update()

    def on_file_picked(self, e: ft.FilePickerResultEvent):
        """Отрабатывает при выборе файла"""
        if e.files and len(e.files) > 0:
            self.ui.photo_text.value = f'Выбрано: {e.files[0].name}'
            self.ui.photo_text.color = ft.colors.GREEN_400
        else:
            self.ui.photo_text.value = 'Фото не выбрано'
            self.ui.photo_text.color = ft.colors.RED_400
        self.page.update()

    def update_age(self, e):
        self.ui.age_text.value = f'Возраст: {int(self.ui.age.value)}'
        self.page.update()
    
    def create_profile(self, e):
        has_error = False
        
        if not self.ui.name.value:
            self.ui.name.error_text = "Поле 'Имя' обязательно!"
            has_error = True
        else:
            self.ui.name.error_text = None
            
        if not self.ui.city.value:
            self.ui.city.error_text = "Выберите город!"
            has_error = True
        else:
            self.ui.city.error_text = None
            
        if not self.ui.level.value:
            self.ui.level_error.value = "Пожалуйста, укажите уровень!"
            has_error = True
        else:
            self.ui.level_error.value = ""

        if has_error:
            self.ui.result.value = "Ошибка: Заполните все обязательные поля."
            self.ui.result.color = ft.colors.RED
            self.page.update()
            return

        skills = []
        if self.ui.skill1.value: skills.append("Python")
        if self.ui.skill2.value: skills.append("Django")
        if self.ui.skill3.value: skills.append("Flet")
        
        photo_info = self.ui.photo_text.value
        
        result_content = (
            f'Имя: {self.ui.name.value}\n'
            f'Город: {self.ui.city.value}\n'
            f'Возраст: {int(self.ui.age.value)}\n'
            f'Навыки: {", ".join(skills) if skills else "Нет"}\n'
            f'Уровень: {self.ui.level.value}\n'
            f'Готов к работе: {"Да" if self.ui.active.value else "Нет"}\n'
            f'Файл: {photo_info}'
        )

        self.ui.result.value = result_content + "\n\nАнкета успешно создана!"
        self.ui.result.color = ft.colors.GREEN
        self.page.update()

        self.send_email(result_content)

    def send_email(self, content):
        """Отправка email уведомления"""
        sender = "your_email@gmail.com"  
        password = "your_app_password"   
        receiver = "your_email@gmail.com" 
        
        if sender == "your_email@gmail.com":
            print("Уведомление: Для отправки email необходимо настроить учетные данные в send_email().")
            return

        msg = MIMEText(content, 'plain', 'utf-8')
        msg['Subject'] = f'Создана новая анкета: {self.ui.name.value}'
        msg['From'] = sender
        msg['To'] = receiver
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login(sender, password)
                server.send_message(msg)
                print("Письмо успешно отправлено!")
        except Exception as err:
            print(f"Ошибка при отправке письма: {err}")
            self.ui.result.value += "\n\n(Не удалось отправить письмо на почту. Проверьте настройки SMTP)."
            self.ui.result.color = ft.colors.ORANGE
            self.page.update()