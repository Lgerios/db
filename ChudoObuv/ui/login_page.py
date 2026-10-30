"""Страница входа: вход только по логину (без пароля) или как гость."""
import tkinter as tk
from tkinter import messagebox

import config
import database
from ui.image_loader import load_scaled_image


class LoginPage(tk.Frame):
    def __init__(self, master, on_login):
        """on_login(user) - функция приложения; user = None означает гостя."""
        super().__init__(master, bg=config.COLOR_MAIN_BG)
        self.on_login = on_login
        self.build_widgets()

    def build_widgets(self):
        card = tk.Frame(self, bg=config.COLOR_EXTRA_BG, padx=40, pady=30)
        card.place(relx=0.5, rely=0.5, anchor="center")

        self.logo = load_scaled_image(config.LOGO_PATH, 160, 160)
        tk.Label(card, image=self.logo, bg=config.COLOR_EXTRA_BG).pack(pady=(0, 10))
        tk.Label(card, text="Вход в систему", bg=config.COLOR_EXTRA_BG,
                 font=(config.FONT_FAMILY, 20, "bold")).pack()
        tk.Label(card, text="Введите логин (пароль не требуется)", bg=config.COLOR_EXTRA_BG,
                 font=(config.FONT_FAMILY, 12)).pack(pady=(5, 10))

        self.login_entry = tk.Entry(card, font=(config.FONT_FAMILY, 14), width=24, justify="center")
        self.login_entry.pack(pady=5)
        self.login_entry.focus_set()
        self.login_entry.bind("<Return>", lambda event: self.handle_login())

        tk.Button(card, text="Войти", command=self.handle_login, bg=config.COLOR_ACCENT,
                  font=(config.FONT_FAMILY, 13, "bold"), width=22, relief="flat").pack(pady=(10, 5))
        tk.Button(card, text="Войти как гость", command=self.handle_guest,
                  bg=config.COLOR_MAIN_BG, font=(config.FONT_FAMILY, 12), width=22,
                  relief="flat").pack(pady=5)

    def handle_login(self):
        login = self.login_entry.get().strip()
        if not login:
            messagebox.showwarning("Логин не указан", "Введите логин и нажмите «Войти».\n"
                                   "Или выберите «Войти как гость» для просмотра каталога.")
            return
        try:
            user = database.find_user_by_login(login)
        except database.DatabaseError as error:
            messagebox.showerror("Ошибка базы данных", str(error))
            return
        if user is None:
            messagebox.showerror("Пользователь не найден",
                                 f"Логин «{login}» отсутствует в системе.\n"
                                 "Проверьте раскладку и написание логина и попробуйте снова.")
            return
        self.on_login(user)

    def handle_guest(self):
        self.on_login(None)
