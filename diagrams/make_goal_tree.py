# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D
import os

OUT = os.path.dirname(os.path.abspath(__file__))
SLATE = "#334155"
GREEN = "#059669"
LIGHT = "#f1f5f9"
INK = "#0f172a"

fig, ax = plt.subplots(figsize=(13.6, 6.2), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 7.2)
ax.axis("off")
ax.text(8, 6.8, "Дерево целей и задач разработки",
        ha="center", va="center", fontsize=14.5, fontweight="bold", color=INK)


def node(x, y, w, h, text, dark=False, green=False):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.03,rounding_size=0.08", linewidth=1.5,
                 edgecolor=(GREEN if green else SLATE),
                 facecolor=(GREEN if green else LIGHT), zorder=2))
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5,
            fontweight="bold", color="white" if green else INK, zorder=4)


def link(x1, y1, x2, y2):
    ymid = (y1 + y2) / 2
    ax.add_line(Line2D([x1, x1, x2, x2], [y1, ymid, ymid, y2],
                color=SLATE, lw=1.4, zorder=1))


node(8, 5.55, 7.6, 1.0,
     "Цель: сократить время контроля складских\nостатков и подготовки заявок",
     green=True)

tasks = [
    (1.9, "Вести актуальный\nкаталог товаров"),
    (5.0, "Контролировать\nостатки и дефицит"),
    (8.0, "Автоматизировать\nзаявки поставщикам"),
    (11.0, "Формировать\nотчёты"),
    (14.1, "Разграничить доступ\nпо ролям"),
]
for x, t in tasks:
    node(x, 2.0, 2.7, 1.1, t)
    link(8, 5.05, x, 2.55)

fig.savefig(os.path.join(OUT, "goal_tree.png"), dpi=150, bbox_inches="tight",
            pad_inches=0.1, facecolor="white")
plt.close(fig)
print("done")
