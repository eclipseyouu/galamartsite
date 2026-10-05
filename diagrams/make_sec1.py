# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from matplotlib.lines import Line2D
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SLATE = "#334155"
LIGHT = "#f1f5f9"
INK = "#0f172a"


def arrow(ax, p1, p2, color=INK, lw=1.4, rad=0.0, style="-|>"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, color=color, lw=lw,
                 mutation_scale=12, connectionstyle=f"arc3,rad={rad}",
                 zorder=3))


# ---------- 1. Организационная структура ----------
fig, ax = plt.subplots(figsize=(12.8, 5.6), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 7)
ax.axis("off")
ax.text(8, 6.6, "Организационная структура магазина «Галамарт»",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=INK)


def node(x, y, w, h, title, sub=None, dark=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.03,rounding_size=0.08", linewidth=1.5,
                 edgecolor=SLATE, facecolor=(SLATE if dark else LIGHT),
                 zorder=2))
    color = "white" if dark else INK
    if sub:
        ax.text(x, y + 0.16, title, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=color, zorder=4)
        ax.text(x, y - 0.24, sub, ha="center", va="center", fontsize=8.5,
                color=("white" if dark else "#475569"), zorder=4)
    else:
        ax.text(x, y, title, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color=color, zorder=4)


def link(x1, y1, x2, y2):
    ax.add_line(Line2D([x1, x1, x2, x2], [y1, (y1 + y2) / 2, (y1 + y2) / 2, y2],
                color=SLATE, lw=1.4, zorder=1))


node(8, 5.5, 3.0, 0.8, "Директор магазина", dark=True)
node(3.2, 3.7, 3.4, 0.9, "Администратор", "учётные записи, доступ")
node(8, 3.7, 3.4, 0.9, "Товаровед", "каталог, остатки, заявки")
node(12.8, 3.7, 3.4, 0.9, "Бухгалтер", "финансы, отчётность")
node(3.2, 1.7, 3.4, 0.9, "Продавцы-кассиры", "продажи, касса")
node(8, 1.7, 3.4, 0.9, "Кладовщик", "приёмка, хранение")

link(8, 5.1, 3.2, 4.15)
link(8, 5.1, 8, 4.15)
link(8, 5.1, 12.8, 4.15)
link(3.2, 3.25, 3.2, 2.15)
link(8, 3.25, 8, 2.15)

fig.savefig(os.path.join(OUT, "orgchart.png"), dpi=150, bbox_inches="tight",
            pad_inches=0.1, facecolor="white")
plt.close(fig)

# ---------- 2. Внешнее взаимодействие ----------
fig, ax = plt.subplots(figsize=(12.8, 6.4), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 8)
ax.axis("off")
ax.text(8, 7.6, "Диаграмма внешнего взаимодействия магазина «Галамарт»",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=INK)

node(8, 4.0, 4.2, 1.3, "Магазин «Галамарт»", "складской учёт", dark=True)
node(1.9, 5.9, 3.0, 0.85, "Поставщики")
node(1.9, 2.1, 3.0, 0.85, "Покупатели")
node(14.1, 5.9, 3.0, 0.85, "Банк")
node(14.1, 2.1, 3.0, 0.85, "Налоговая инспекция")

arrow(ax, (3.4, 5.65), (6.6, 4.55), rad=0.12)
ax.text(4.0, 5.5, "товары, накладные", ha="left", va="center", fontsize=9,
        color=INK)
arrow(ax, (6.6, 3.6), (3.4, 2.35), rad=0.12)
ax.text(4.0, 2.6, "спрос, продажи", ha="left", va="center", fontsize=9,
        color=INK)
arrow(ax, (9.4, 4.6), (12.6, 5.65), rad=0.12)
ax.text(11.9, 5.5, "платежи", ha="right", va="center", fontsize=9, color=INK)
arrow(ax, (9.4, 3.55), (12.6, 2.35), rad=0.12)
ax.text(11.9, 2.6, "отчётность", ha="right", va="center", fontsize=9,
        color=INK)

fig.savefig(os.path.join(OUT, "interaction.png"), dpi=150, bbox_inches="tight",
            pad_inches=0.1, facecolor="white")
plt.close(fig)
print("done")
