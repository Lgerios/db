"""Точка входа: окно приложения и переключение страниц (вход <-> каталог)."""
import os
import tkinter as tk

import config
from ui.catalog_page import CatalogPage
from ui.login_page import LoginPage


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x700")
        self.minsize(850, 500)
        self.configure(bg=config.COLOR_MAIN_BG)
        self.set_icon()
        self.current_page = None
        self.show_login()

    def set_icon(self):
        """Иконка приложения из ресурсов (.ico работает в Windows, иначе используем png)."""
        try:
            self.iconbitmap(config.ICON_PATH)
        except tk.TclError:
            self.icon_image = tk.PhotoImage(file=config.LOGO_PATH)
            self.iconphoto(True, self.icon_image)

    def show_page(self, page, title):
        """Заменяет текущую страницу и ставит заголовок окна (содержит название компании)."""
        if self.current_page is not None:
            self.current_page.destroy()
        self.current_page = page
        self.current_page.pack(fill="both", expand=True)
        self.title(f"{config.APP_NAME} — {title}")

    def show_login(self):
        self.show_page(LoginPage(self, on_login=self.show_catalog), "Вход в систему")

    def show_catalog(self, user):
        self.show_page(CatalogPage(self, user, on_back=self.show_login), "Каталог обуви")


if __name__ == "__main__":
    App().mainloop()
