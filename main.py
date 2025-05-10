import customtkinter as ctk
from src.app import TodoApp


if __name__ == "__main__":
    root = ctk.CTk()
    app = TodoApp(root)
    root.mainloop()