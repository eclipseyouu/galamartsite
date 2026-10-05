# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SLATE = "#334155"
LIGHT = "#f1f5f9"
INK = "#0f172a"
GREEN = "#059669"


def node(ax, x, y, w, h, title, sub=None, dark=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.03,rounding_size=0.08", linewidth=1.5,
                 edgecolor=SLATE, facecolor=(SLATE if dark else LIGHT),
                 zorder=2))
    color = "white" if dark else INK
    if sub:
        ax.text(x, y + 0.14, title, ha="center", va="center", fontsize=10,
                fontweight="bold", color=color, zorder=4)
        ax.text(x, y - 0.2, sub, ha="center", va="center", fontsize=8.5,
                color=("white" if dark else "#475569"), zorder=4)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=10,
                fontweight="bold", color=color, zorder=4)


# ---------- Б.1: структура размещения ----------
fig, ax = plt.subplots(figsize=(9.6, 5.2), dpi=150)
ax.set_xlim(0, 12)
ax.set_ylim(0, 6.4)
ax.axis("off")
ax.text(6, 6.05, "Структура размещения проекта «Галамарт Склад»",
        ha="center", va="center", fontsize=13, fontweight="bold", color=INK)

lines = [
    "galamartsite/",
    "  index.html                — разметка страницы, стили, подключение модулей",
    "  database.sql              — эталонная SQL-схема базы данных",
    "  assets/",
    "    js/app.js               — логика приложения (состояние, CRUD, отчёты)",
    "    screens/                — иллюстрации и диаграммы документации",
]
y = 5.2
for ln in lines:
    mono = ln.strip()
    ax.text(1.0, y, ln, ha="left", va="center", fontsize=10, color=INK,
            family="monospace")
    y -= 0.62
fig.savefig(os.path.join(OUT, "file_tree.png"), dpi=150, bbox_inches="tight",
            pad_inches=0.1, facecolor="white")
plt.close(fig)

# ---------- В.1: логическая структура app.js ----------
fig, ax = plt.subplots(figsize=(11.2, 5.6), dpi=150)
ax.set_xlim(0, 14)
ax.set_ylim(0, 7)
ax.axis("off")
ax.text(7, 6.65, "Логическая структура модуля app.js",
        ha="center", va="center", fontsize=13.5, fontweight="bold", color=INK)

node(ax, 7, 5.5, 5.4, 0.95, "Состояние приложения", "товары, заявки, пользователь", dark=True)
node(ax, 2.4, 3.4, 3.6, 1.0, "CRUD товаров", "добавление, правка,\nудаление")
node(ax, 7, 3.4, 3.4, 1.0, "Заявки", "создание, статусы,\nпоступление")
node(ax, 11.6, 3.4, 3.4, 1.0, "Отчёты", "дефицит, экспорт\nXLSX / PDF")
node(ax, 4.7, 1.2, 4.2, 0.95, "Рендеринг интерфейса", "таблицы, панели")
node(ax, 10.4, 1.2, 4.0, 0.95, "localStorage", "save() / load()")

links = [((7, 5.02), (2.4, 3.9)), ((7, 5.02), (7, 3.9)), ((7, 5.02), (11.6, 3.9)),
         ((2.4, 2.9), (4.5, 1.68)), ((7, 2.9), (4.9, 1.68)),
         ((11.6, 2.9), (10.7, 1.68)), ((7, 3.4 - 0.5 + 0.0), (7, 3.9))]
for (x1, y1), (x2, y2) in [((7, 5.02), (2.4, 3.9)), ((7, 5.02), (7, 3.9)),
                           ((7, 5.02), (11.6, 3.9)),
                           ((2.4, 2.9), (4.5, 1.68)), ((7, 2.9), (4.9, 1.68)),
                           ((11.6, 2.9), (10.7, 1.68))]:
    ymid = (y1 + y2) / 2
    ax.add_line(Line2D([x1, x1, x2, x2], [y1, ymid, ymid, y2], color=SLATE,
                lw=1.3, zorder=1))
fig.savefig(os.path.join(OUT, "app_structure.png"), dpi=150,
            bbox_inches="tight", pad_inches=0.1, facecolor="white")
plt.close(fig)
print("done")
