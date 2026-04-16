import flet as ft
from app import RouletteApp

def main(page: ft.Page):
    RouletteApp(page)

if __name__ == "__main__":
    ft.app(target=main)