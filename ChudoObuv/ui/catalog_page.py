"""Главная форма: каталог моделей обуви (макет из задания) + ФИО пользователя справа вверху."""
import tkinter as tk
from tkinter import messagebox

import config
import database
import pricing
from ui.image_loader import load_product_image, load_scaled_image


class CatalogPage(tk.Frame):
    def __init__(self, master, user, on_back):
        """user - словарь пользователя или None (гость); on_back - возврат на страницу входа."""
        super().__init__(master, bg=config.COLOR_MAIN_BG)
        self.user = user
        self.on_back = on_back
        self.build_header()
        self.build_list_area()
        self.fill_catalog()

    # ---------- шапка: логотип, кнопка «Назад», ФИО ----------
    def build_header(self):
        header = tk.Frame(self, bg=config.COLOR_EXTRA_BG)
        header.pack(fill="x")

        self.logo = load_scaled_image(config.LOGO_PATH, 60, 60)
        tk.Label(header, image=self.logo, bg=config.COLOR_EXTRA_BG).pack(side="left", padx=10, pady=5)
        tk.Label(header, text="Каталог обуви", bg=config.COLOR_EXTRA_BG,
                 font=(config.FONT_FAMILY, 20, "bold")).pack(side="left", padx=10)

        # ФИО пользователя - в правом верхнем углу
        if self.user:
            full_name = f"{self.user['last_name']} {self.user['first_name']} {self.user['middle_name'] or ''}".strip()
        else:
            full_name = "Гость"
        tk.Label(header, text=full_name, bg=config.COLOR_EXTRA_BG,
                 font=(config.FONT_FAMILY, 14)).pack(side="right", padx=15)
        tk.Button(header, text="Назад", command=self.on_back, bg=config.COLOR_ACCENT,
                  font=(config.FONT_FAMILY, 12, "bold"), relief="flat", width=10).pack(side="right", padx=5)

    # ---------- прокручиваемая область со списком ----------
    def build_list_area(self):
        container = tk.Frame(self, bg=config.COLOR_MAIN_BG)
        container.pack(fill="both", expand=True)
        self.canvas = tk.Canvas(container, bg=config.COLOR_MAIN_BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        self.list_frame = tk.Frame(self.canvas, bg=config.COLOR_MAIN_BG)
        self.window_id = self.canvas.create_window((0, 0), window=self.list_frame, anchor="nw")
        self.list_frame.bind("<Configure>",
                             lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>",
                         lambda event: self.canvas.itemconfigure(self.window_id, width=event.width))
        # прокрутка колесом мыши (Windows/macOS и Linux)
        self.canvas.bind_all("<MouseWheel>", self.scroll_with_wheel)
        self.canvas.bind_all("<Button-4>", lambda event: self.canvas.yview_scroll(-1, "units"))
        self.canvas.bind_all("<Button-5>", lambda event: self.canvas.yview_scroll(1, "units"))

    def scroll_with_wheel(self, event):
        self.canvas.yview_scroll(int(-event.delta / 120), "units")

    # ---------- заполнение каталога ----------
    def fill_catalog(self):
        try:
            products = database.load_catalog()
        except database.DatabaseError as error:
            messagebox.showerror("Ошибка базы данных", str(error))
            return
        if not products:
            tk.Label(self.list_frame, text="Каталог пуст", bg=config.COLOR_MAIN_BG,
                     font=(config.FONT_FAMILY, 14)).pack(pady=20)
        for product in products:
            self.add_product_card(product)

    def add_product_card(self, product):
        """Одна карточка по макету: фото | Производство | Наименование, категория,
        количество, состав | цена."""
        quantity = int(product["total_quantity"])
        # подсветка светло-красным, если суммарное количество <= 3
        background = config.COLOR_LOW_STOCK if quantity <= config.LOW_STOCK_LIMIT else config.COLOR_MAIN_BG
        price = pricing.calculate_price(product["price"], product["had_orders_last_month"])

        card = tk.Frame(self.list_frame, bg=background, highlightbackground="black", highlightthickness=1)
        card.pack(fill="x", padx=15, pady=6)
        card.columnconfigure(1, weight=1)

        photo = load_product_image(product["image_path"], 110, 110)
        image_label = tk.Label(card, image=photo, bg=background)
        image_label.grid(row=0, column=0, rowspan=4, padx=10, pady=8)

        title = f"{product['manufacturer_name']} | {product['product_name']}"
        info = [
            (title, 14, "bold"),
            (f"Категория: {product['category_name']}", 12, "normal"),
            (f"Количество: {quantity}", 12, "normal"),
            (f"Состав: {product['composition'] or '—'}", 10, "normal"),
        ]
        for row, (text, size, weight) in enumerate(info):
            tk.Label(card, text=text, bg=background, anchor="w", justify="left", wraplength=620,
                     font=(config.FONT_FAMILY, size, weight)).grid(row=row, column=1, sticky="w", pady=1)

        # цена: если есть скидка - показываем старую зачёркнутой и новую
        price_text = f"{price:,.2f} ₽".replace(",", " ")
        if price < product["price"]:
            old_text = f"{float(product['price']):,.2f} ₽".replace(",", " ")
            tk.Label(card, text=old_text, bg=background, fg="#555555",
                     font=(config.FONT_FAMILY, 12, "overstrike")).grid(row=0, column=2, padx=20, sticky="e")
        tk.Label(card, text=price_text, bg=background,
                 font=(config.FONT_FAMILY, 16, "bold")).grid(row=1, column=2, rowspan=2, padx=20, sticky="e")
        self.photo_refs = getattr(self, "photo_refs", [])
        self.photo_refs.append(photo)  # держим ссылку на картинку
