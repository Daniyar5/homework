import flet as ft

class UI:
    def __init__(self):
        self.theme_switch = ft.Switch(label='Тёмная тема', value=False)

        self.title = ft.Text('Создание пользователей', size=20, weight=ft.FontWeight.BOLD)
        
        self.name = ft.TextField(label='Имя', width=300)

        self.city = ft.Dropdown(
            label='Город',
            width=300,
            options=[
                ft.dropdown.Option('Бишкек'),
                ft.dropdown.Option('ОШ'),
                ft.dropdown.Option('Токмок'),
            ],
        )

        self.file_picker = ft.FilePicker()
        self.upload_btn = ft.ElevatedButton('Выбрать фото', icon=ft.icons.UPLOAD_FILE)
        self.photo_text = ft.Text('Фото не выбрано', color=ft.colors.RED_400)

        self.age_text = ft.Text('Возраст: 10')
        self.age = ft.Slider(
            min=10,
            max=60,
            divisions=50,
            value=10,
            label="{value}"
        )
        self.skill1 = ft.Checkbox(label='Python')
        self.skill2 = ft.Checkbox(label='Django')
        self.skill3 = ft.Checkbox(label='Flet')

        self.level = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value='Jun', label='Junior'),
                ft.Radio(value='Mid', label='Middle'),
                ft.Radio(value='Sen', label='Senior'),
            ])
        )
        self.level_error = ft.Text('', color=ft.colors.RED, size=12)
        
        self.active = ft.Switch(label='Готов к работе')

        self.button = ft.ElevatedButton('Отправить резюме')

        self.result = ft.Text()
    
    def build(self):
        return [
            self.theme_switch,
            self.title,
            self.name,
            self.city,
            ft.Row([self.upload_btn, self.photo_text]),
            self.age_text,
            self.age,
            ft.Text('Навыки:'),
            self.skill1,
            self.skill2,
            self.skill3,
            ft.Text('Уровень:'),
            self.level,
            self.level_error,
            self.active,
            self.button,
            self.result
        ]