import flet as ft

class UI:
    def __init__(self):
        self.title = ft.Text('Создание пользователей')
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
        
        self.active = ft.Switch(label='Готов к работе')

        self.button = ft.ElevatedButton('Отправить резюме')

        self.result = ft.Text()  # Исправлено: создаем экземпляр
    
    def build(self):
        return [
            self.title,
            self.name,
            self.city,
            self.age_text,
            self.age,
            ft.Text('Навыки:'),
            self.skill1,
            self.skill2,
            self.skill3,
            ft.Text('Уровень:'),
            self.level,
            self.active,
            self.button,
            self.result
        ]