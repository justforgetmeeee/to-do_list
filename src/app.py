import json
import os
import customtkinter as ctk
from tkinter import messagebox

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Todo List App")
        self.root.geometry("900x700")
        
        ctk.set_appearance_mode("dark") # 'dark', 'white', 'system'
        ctk.set_default_color_theme("blue") # 'blue', 'green', 'dark-blue'
        
        self.tasks = self.load_tasks()
        
        self.create_widgets()
    
    def load_tasks(self):
        try:
            if os.path.exists("src\\todo.json"):
                with open("src\\todo.json", "r", encoding="utf-8") as f:
                    return json.load(f)
            return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить задачи: {e}")
            return
    
    def save_tasks(self):
        try:
            with open("src\\todo.json", "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=4)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить задачи: {e}")
    
    def create_widgets(self):
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Список задач",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=10)
        
        self.create_control_panel()
        
        self.tasks_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.tasks_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.display_tasks()
    
    def create_control_panel(self): # Кнопка добавления
        add_button = ctk.CTkButton(
            self.main_frame,
            text="Добавить задачу",
            command=self.add_task_dialog
        )
        add_button.pack(side="top", anchor="w", padx=5, pady=(0, 10))
        
        # Кнопка обновления
        refresh_button = ctk.CTkButton(
            self.main_frame,
            text="Обновить",
            command=self.refresh_tasks
        )
        refresh_button.pack(side="top", anchor="w", padx=5, pady=(0, 10))
        
        filter_frame = ctk.CTkFrame(self.main_frame)
        filter_frame.pack(side="top", fill="x", padx=5, pady=(0, 10))
        
        ctk.CTkLabel(filter_frame, text="Фильтры:").pack(side="left", padx=5)
        
        self.filter_var = ctk.StringVar(value="all")
        
        ctk.CTkRadioButton(
            filter_frame, 
            text="Все", 
            variable=self.filter_var, 
            value="all",
            command=lambda: self.filter_tasks("all")
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            filter_frame, 
            text="Активные", 
            variable=self.filter_var, 
            value="active",
            command=lambda: self.filter_tasks("active")
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            filter_frame, 
            text="Завершенные", 
            variable=self.filter_var, 
            value="completed",
            command=lambda: self.filter_tasks("completed")
        ).pack(side="left", padx=5)
    
    def add_filters(self, parent_frame): # Фильтр задач
        filter_frame = ctk.CTkFrame(parent_frame)
        filter_frame.pack(side="right", padx=5)
        
        ctk.CTkLabel(filter_frame, text="Фильтры:").pack(side="left", padx=5)
        
        self.filter_var = ctk.StringVar(value="all")
        
        ctk.CTkRadioButton(
            filter_frame, 
            text="Все", 
            variable=self.filter_var, 
            value="all",
            command=lambda: self.filter_tasks("all")
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            filter_frame, 
            text="Активные", 
            variable=self.filter_var, 
            value="active",
            command=lambda: self.filter_tasks("active")
        ).pack(side="left", padx=5)
        
        ctk.CTkRadioButton(
            filter_frame, 
            text="Завершенные", 
            variable=self.filter_var, 
            value="completed",
            command=lambda: self.filter_tasks("completed")
        ).pack(side="left", padx=5)
    
    def display_tasks(self, tasks=None):
        tasks_to_display = tasks if tasks is not None else self.tasks
        
        # Очистка текущего списка
        for widget in self.tasks_frame.winfo_children():
            widget.destroy()
        
        # Если задач нет
        if not tasks_to_display:
            empty_label = ctk.CTkLabel(
                self.tasks_frame, 
                text="Нет задач для отображения",
                font=ctk.CTkFont(size=14)
            )
            empty_label.pack(pady=20)
            return
        
        # Отображение каждой задачи
        for task in tasks_to_display:
            self.create_task_widget(task)
    
    def create_task_widget(self, task): # Виджет для одной задачи
        task_frame = ctk.CTkFrame(self.tasks_frame)
        task_frame.pack(fill="x", pady=5, padx=5)
        
        # Чекбокс выполнения
        done_var = ctk.BooleanVar(value=task.get("completed", False))
        done_check = ctk.CTkCheckBox(
            task_frame, 
            text="", 
            variable=done_var,
            command=lambda t=task, v=done_var: self.toggle_task(t, v)
        )
        done_check.pack(side="left", padx=5)
        
        # Описание задачи
        task_text = f"{task.get('title', 'Без названия')}"
        if "description" in task and task["description"]:
            task_text += f": {task['description']}"
        
        # Изменение стиля для завершенных задач
        text_color = "#888888" if task.get("completed", False) else "#ffffff"
        
        task_label = ctk.CTkLabel(
            task_frame,
            text=task_text,
            font=ctk.CTkFont(size=14),
            anchor="w",
            text_color=text_color
        )
        task_label.pack(side="left", fill="x", expand=True, padx=5)
        
        # Приоритет (если есть)
        if "priority" in task:
            priority_label = ctk.CTkLabel(
                task_frame,
                text=f"Приоритет: {task['priority']}",
                font=ctk.CTkFont(size=12),
                text_color=self.get_priority_color(task['priority'])
            )
            priority_label.pack(side="left", padx=5)
        
        # Дата (если есть)
        if "due_date" in task and task["due_date"]:
            date_label = ctk.CTkLabel(
                task_frame,
                text=f"Срок: {task['due_date']}",
                font=ctk.CTkFont(size=12)
            )
            date_label.pack(side="left", padx=5)
        
        # Кнопка удаления
        self.add_delete_button(task_frame, task)
    
    def add_delete_button(self, task_frame, task): # Кнопка удаления задачи
        delete_btn = ctk.CTkButton(
            task_frame,
            text="Удалить",
            width=30,
            fg_color="#ff5555",
            hover_color="#ff3333",
            command=lambda: self.delete_task(task)
        )
        delete_btn.pack(side="right", padx=5)
    
    def get_priority_color(self, priority):
        priority = str(priority).lower()
        if priority in ["high", "высокий"]:
            return "#ff5555"  # Красный
        elif priority in ["medium", "средний"]:
            return "#ffaa00"  # Оранжевый
        elif priority in ["low", "низкий"]:
            return "#55aa55"  # Зеленый
        return "#ffffff"  # Белый (по умолчанию)
    
    def toggle_task(self, task, done_var): # Изменение статуса задачи
        task["completed"] = done_var.get()
        self.save_tasks()
        current_filter = self.filter_var.get()
        self.filter_tasks(current_filter)
    
    def delete_task(self, task):
        self.tasks.remove(task)
        self.save_tasks()
        current_filter = self.filter_var.get()
        self.filter_tasks(current_filter)
    
    def refresh_tasks(self):
        self.tasks = self.load_tasks()
        current_filter = self.filter_var.get()
        self.filter_tasks(current_filter)
    
    def filter_tasks(self, filter_type):
        if filter_type == "all":
            filtered_tasks = self.tasks
        elif filter_type == "active":
            filtered_tasks = [task for task in self.tasks if not task.get("completed", False)]
        else:
            filtered_tasks = [task for task in self.tasks if task.get("completed", False)]
        
        self.display_tasks(filtered_tasks)
    
    def add_task_dialog(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Добавить задачу")
        dialog.geometry("400x350")
        dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="Название:").pack(pady=5)
        title_entry = ctk.CTkEntry(dialog, width=300)
        title_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Описание:").pack(pady=5)
        desc_entry = ctk.CTkEntry(dialog, width=300)
        desc_entry.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Приоритет:").pack(pady=5)
        priority_var = ctk.StringVar(value="medium")
        priority_menu = ctk.CTkOptionMenu(
            dialog, 
            variable=priority_var,
            values=["high", "medium", "low"]
        )
        priority_menu.pack(pady=5)
        
        ctk.CTkLabel(dialog, text="Срок выполнения:").pack(pady=5)
        date_entry = ctk.CTkEntry(dialog, width=300, placeholder_text="YYYY-MM-DD")
        date_entry.pack(pady=5)
        
        def save_task():
            if not title_entry.get():
                messagebox.showerror("Ошибка", "Название задачи обязательно!")
                return
                
            new_task = {
                "title": title_entry.get(),
                "description": desc_entry.get(),
                "priority": priority_var.get(),
                "due_date": date_entry.get() if date_entry.get() else None,
                "completed": False
            }
            self.tasks.append(new_task)
            self.save_tasks()
            
            current_filter = self.filter_var.get()
            self.filter_tasks(current_filter)
            
            dialog.destroy()
        
        button_frame = ctk.CTkFrame(dialog)
        button_frame.pack(pady=10)
        
        ctk.CTkButton(
            button_frame,
            text="Сохранить",
            command=save_task
        ).pack(side="left", padx=10)
        
        ctk.CTkButton(
            button_frame,
            text="Отмена",
            command=dialog.destroy
        ).pack(side="right", padx=10)
