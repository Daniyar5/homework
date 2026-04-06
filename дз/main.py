from __future__ import annotations
import asyncio, json
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
import flet as ft

@dataclass
class Task:
    title: str
    priority: str
    done: bool = False
    deadline: str | None = None
    notified: bool = False

    def is_overdue(self) -> bool:
        if self.done or not self.deadline: return False
        try: return date.today() > datetime.fromisoformat(self.deadline).date()
        except ValueError: return False

class TodoApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title, self.page.window_width, self.page.window_height, self.page.padding = "TODO Планировщик", 760, 820, 20
        self.page.scroll = ft.ScrollMode.AUTO
        self.data_file = Path(__file__).with_name("tasks.json")
        self.tasks: list[Task] = []
        self.deadline_dialog = None
        
        self.load_tasks()
        self.build_ui()
        self.refresh_view()
        self.page.run_task(self.deadline_watcher)

    def build_ui(self):
        self.task_input = ft.TextField(label="Задача", expand=True)
        self.priority = ft.Dropdown(label="Приоритет", width=160, options=[ft.dropdown.Option(p) for p in ("Высокий", "Средний", "Низкий")])
        self.deadline_input = ft.TextField(label="Дедлайн (ГГГГ-ММ-ДД)", width=220)
        self.search_input = ft.TextField(label="Поиск задач", prefix_icon=ft.Icons.SEARCH, on_change=lambda e: self.refresh_view())
        self.stats_text, self.file_info_text = ft.Text(size=14, weight=ft.FontWeight.W_500), ft.Text(size=12, color=ft.Colors.GREY_700)
        self.task_list = ft.Column(spacing=10)

        self.page.add(
            ft.Text("Планировщик задач", size=24, weight=ft.FontWeight.BOLD),
            ft.Text("Можно добавлять задачи, отмечать выполненные, искать, смотреть статистику и сохранять всё в JSON-файл.", size=13, color=ft.Colors.GREY_700),
            ft.Row([self.task_input, self.priority], spacing=10),
            ft.Row([self.deadline_input, ft.ElevatedButton("Добавить", icon=ft.Icons.ADD, on_click=self.add_task), 
                    ft.OutlinedButton("Сохранить в файл", icon=ft.Icons.SAVE, on_click=lambda e: self.save_tasks(f"Задачи сохранены: {self.data_file.name}"))], spacing=10, wrap=True),
            self.search_input,
            ft.Container(content=ft.Column([self.stats_text, self.file_info_text], spacing=4), padding=12, bgcolor=ft.Colors.BLUE_50, border_radius=10),
            ft.Divider(), self.task_list,
        )

    def format_deadline(self, d_str: str | None) -> str:
        if not d_str: return "Без дедлайна"
        try: return datetime.fromisoformat(d_str).strftime("%d.%m.%Y")
        except ValueError: return d_str

    def load_tasks(self):
        if not self.data_file.exists(): return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                self.tasks = [Task(**t) for t in json.load(f) if isinstance(t, dict)]
        except Exception: self.tasks = []

    def save_tasks(self, msg: str = None):
        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump([asdict(t) for t in self.tasks], f, ensure_ascii=False, indent=2)
        if msg:
            self.page.snack_bar = ft.SnackBar(content=ft.Text(msg), open=True)
        self.refresh_view()

    def refresh_view(self):
        # Статистика
        tot, comp = len(self.tasks), sum(1 for t in self.tasks if t.done)
        bp = {p: sum(1 for t in self.tasks if t.priority == p) for p in ("Высокий", "Средний", "Низкий")}
        self.stats_text.value = f"Всего: {tot} | Выполнено: {comp} | Активных: {tot - comp} | Просрочено: {sum(1 for t in self.tasks if t.is_overdue())}"
        self.file_info_text.value = f"Высокий: {bp['Высокий']} | Средний: {bp['Средний']} | Низкий: {bp['Низкий']} | Файл: {self.data_file.resolve()}"

        # Список задач
        self.task_list.controls.clear()
        q = (self.search_input.value or "").strip().lower()
        filtered = [(i, t) for i, t in enumerate(self.tasks) if not q or q in f"{t.title} {t.priority} {self.format_deadline(t.deadline)}".lower()]

        if not filtered: self.task_list.controls.append(ft.Text("Ничего не найдено.", color=ft.Colors.GREY_700))
        for i, t in filtered:
            col = {"Высокий": ft.Colors.RED, "Средний": ft.Colors.ORANGE, "Низкий": ft.Colors.GREEN}.get(t.priority, ft.Colors.BLACK)
            info = f"Приоритет: {t.priority} | Дедлайн: {self.format_deadline(t.deadline)}" + (" | ПРОСРОЧЕНО" if t.is_overdue() else "") + (" | Выполнено" if t.done else "")
            
            self.task_list.controls.append(ft.Container(padding=12, border_radius=12, bgcolor=ft.Colors.GREY_50, border=ft.border.all(1, ft.Colors.GREY_300), content=ft.Row([
                ft.Checkbox(value=t.done, on_change=lambda e, idx=i: self.toggle_task(idx, e.control.value)),
                ft.Column([ft.Text(t.title, size=16, color=ft.Colors.GREY_700 if t.done else col, decoration=ft.TextDecoration.LINE_THROUGH if t.done else ft.TextDecoration.NONE, weight=ft.FontWeight.W_600),
                           ft.Text(info, size=12, color=ft.Colors.RED if t.is_overdue() else ft.Colors.GREY_700)], expand=True, spacing=4),
                ft.IconButton(icon=ft.Icons.DELETE, tooltip="Удалить", on_click=lambda e, idx=i: self.delete_task(idx)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.START)))
        self.page.update()

    def add_task(self, e):
        t, p, d = self.task_input.value.strip(), self.priority.value, (self.deadline_input.value or "").strip()
        if not t or not p: return self.save_tasks("Введите задачу и выберите приоритет.")
        try: dl = datetime.strptime(d, "%Y-%m-%d").isoformat() if d else None
        except ValueError: return self.save_tasks("Неверный формат дедлайна. Используйте: ГГГГ-ММ-ДД")
        
        self.tasks.append(Task(title=t, priority=p, deadline=dl))
        self.task_input.value, self.priority.value, self.deadline_input.value = "", None, ""
        self.save_tasks()

    def toggle_task(self, idx: int, val: bool):
        self.tasks[idx].done = val
        if val: self.tasks[idx].notified = True
        self.save_tasks()

    def delete_task(self, idx: int):
        self.tasks.pop(idx)
        self.save_tasks()

    async def deadline_watcher(self):
        while True:
            if not self.deadline_dialog or not self.deadline_dialog.open:
                for t in [task for task in self.tasks if not task.done and not task.notified and task.is_overdue()]:
                    t.notified = True
                    self.save_tasks()
                    self.deadline_dialog = ft.AlertDialog(modal=True, title=ft.Text("Дедлайн истёк"), content=ft.Text(f"У '{t.title}' истёк срок: {self.format_deadline(t.deadline)}"),
                        actions=[ft.TextButton("ОК", on_click=lambda e: self.page.close(self.deadline_dialog))], actions_alignment=ft.MainAxisAlignment.END)
                    self.page.open(self.deadline_dialog)
                    break
            await asyncio.sleep(30)

if __name__ == "__main__":
    ft.app(target=lambda p: TodoApp(p))