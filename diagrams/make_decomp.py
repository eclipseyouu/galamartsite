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
BW, BH = 2.9, 1.5
AX1, AY1 = 1.7, 6.9
AX2, AY2 = 5.1, 5.3
AX3, AY3 = 8.5, 3.7
AX4, AY4 = 11.9, 2.1


def new_fig(w=16.0, h=10.0):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    return fig, ax


def arrow(ax, p1, p2, color=INK, lw=1.5):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", color=color, lw=lw,
                 mutation_scale=13, zorder=3))


def line(ax, p1, p2, color=INK, lw=1.5):
    ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw,
                zorder=3))


def elbow(ax, pts, label=None, lx=None, ly=None):
    for a, b in zip(pts, pts[1:-1]):
        line(ax, a, b)
    arrow(ax, pts[-2], pts[-1])
    if label:
        ax.text(lx if lx is not None else (pts[0][0] + pts[-2][0]) / 2,
                ly if ly is not None else pts[0][1] + 0.18, label,
                ha="center", va="bottom", fontsize=9.5, color=INK)


def box(ax, x0, y0, node, label):
    ax.add_patch(FancyBboxPatch((x0, y0), BW, BH,
                 boxstyle="round,pad=0.03,rounding_size=0.08", linewidth=1.6,
                 edgecolor=SLATE, facecolor=LIGHT, zorder=2))
    ax.text(x0 + BW / 2, y0 + BH - 0.28, node, ha="center", va="center",
            fontsize=10, color=SLATE, zorder=4)
    ax.text(x0 + BW / 2, y0 + BH / 2 - 0.16, label, ha="center", va="center",
            fontsize=10.5, fontweight="bold", color=INK, zorder=4)


def cbl(x, y):
    return (x, y + BH / 2)


def cbr(x, y):
    return (x + BW, y + BH / 2)


def cbt(x, y):
    return (x + BW / 2, y + BH)


def save(fig, fname):
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


CHAIN = [(AX1, AY1), (AX2, AY2), (AX3, AY3), (AX4, AY4)]


def draw_chain(ax, labels):
    for (x0, y0), (x1, y1), lbl in zip(CHAIN, CHAIN[1:], labels):
        p0 = cbr(x0, y0)
        p3 = cbl(x1, y1)
        pm = (p3[0], p0[1])
        line(ax, p0, pm)
        arrow(ax, pm, p3)
        ax.text((p0[0] + pm[0]) / 2, p0[1] + 0.18, lbl, ha="center",
                va="bottom", fontsize=9.5, color=INK)


def draw_title(ax, text):
    ax.text(8.0, 9.55, text, ha="center", va="center", fontsize=15,
            fontweight="bold", color=INK)


# ================= AS-IS =================
fig, ax = new_fig()
draw_title(ax, "Декомпозиция функции А0 складского учёта «как есть»")
for node, label, x, y in [
        ("А1", "Вести журнал\nтоваров", AX1, AY1),
        ("А2", "Сверять фактические\nостатки", AX2, AY2),
        ("А3", "Формировать заявку\nпоставщику", AX3, AY3),
        ("А4", "Составлять\nотчёты", AX4, AY4)]:
    box(ax, x, y, node, label)
draw_chain(ax, ["Журнал остатков", "Сведения о дефиците",
                "Согласованная заявка"])
# feedback A4 -> A1
fb_y = 8.75
elbow(ax, [cbt(AX4, AY4), (cbt(AX4, AY4)[0], fb_y),
           (cbt(AX1, AY1)[0], fb_y), cbt(AX1, AY1)],
      "Ведомость расхождений", ly=fb_y + 0.12)
# inputs
arrow(ax, (0.4, AY1 + 0.75), (AX1, AY1 + 0.75))
ax.text(0.3, AY1 + 0.75, "Данные о товарах", ha="right", va="center",
        fontsize=9.5, color=INK)
arrow(ax, (0.4, AY2 + 0.75), (AX2, AY2 + 0.75))
ax.text(0.3, AY2 + 0.75, "Фактические остатки", ha="right", va="center",
        fontsize=9.5, color=INK)
# controls
c1x, c2x, c3x = cbt(AX1, AY1)[0] - 0.8, cbt(AX2, AY2)[0] - 0.8, cbt(AX3, AY3)[0]
c4x = cbt(AX4, AY4)[0]
# rail 1: учётная политика -> A1, A2
arrow(ax, (c1x, 9.3), (c1x, AY1 + BH))
ax.text(c1x, 9.4, "Учётная политика", ha="center", va="bottom", fontsize=9.5,
        color=INK)
line(ax, (c1x, 9.3), (c2x, 9.3))
arrow(ax, (c2x, 9.3), (c2x, AY2 + BH))
# rail 2: правила минимального запаса -> A3
arrow(ax, (c3x, 8.3), (c3x, AY3 + BH))
ax.text(c3x, 8.4, "Правила минимального запаса", ha="center", va="bottom",
        fontsize=9.5, color=INK)
arrow(ax, (AX1 + BW / 2, 0.9), (AX1 + BW / 2, AY1))
ax.text(AX1 + BW / 2, 0.75, "Товаровед", ha="center", va="top", fontsize=9.5,
        color=INK)
arrow(ax, (AX3 + BW / 2, 0.9), (AX3 + BW / 2, AY3))
ax.text(AX3 + BW / 2, 1.6, "Товаровед", ha="center", va="bottom", fontsize=9.5,
        color=INK)
arrow(ax, (AX4 + BW / 2, 0.9), (AX4 + BW / 2, AY4))
ax.text(AX4 + BW / 2, 0.75, "Excel / бумажные журналы", ha="center", va="top",
        fontsize=9.5, color=INK)
# outputs
p3, p4 = cbr(AX3, AY3), cbr(AX4, AY4)
arrow(ax, p3, (15.4, p3[1]))
ax.text(15.5, p3[1], "Заявка\nпоставщику", ha="left", va="center",
        fontsize=9.5, color=INK)
arrow(ax, p4, (15.4, p4[1]))
ax.text(15.5, p4[1], "Отчёты\n(вручную)", ha="left", va="center",
        fontsize=9.5, color=INK)
save(fig, "idef0_asis_decomp.png")

# ================= TO-BE =================
fig, ax = new_fig()
draw_title(ax, "Декомпозиция функции А0 информационной системы")
for node, label, x, y in [
        ("А1", "Вести каталог\nтоваров", AX1, AY1),
        ("А2", "Контролировать\nостатки", AX2, AY2),
        ("А3", "Формировать заявки\nпоставщикам", AX3, AY3),
        ("А4", "Формировать\nотчёты", AX4, AY4)]:
    box(ax, x, y, node, label)
draw_chain(ax, ["Каталог товаров", "Список дефицитных позиций",
                "Статусы заявок"])
# feedback A4 -> A2
fb_y = 8.75
elbow(ax, [cbt(AX4, AY4), (cbt(AX4, AY4)[0], fb_y),
           (cbt(AX2, AY2)[0], fb_y), cbt(AX2, AY2)],
      "Актуальные отчётные данные", ly=fb_y + 0.12)
# inputs
arrow(ax, (0.4, AY1 + 0.75), (AX1, AY1 + 0.75))
ax.text(0.3, AY1 + 0.75, "Данные о товарах", ha="right", va="center",
        fontsize=9.5, color=INK)
arrow(ax, (0.4, AY2 + 0.75), (AX2, AY2 + 0.75))
ax.text(0.3, AY2 + 0.75, "Остатки", ha="right", va="center", fontsize=9.5,
        color=INK)
arrow(ax, (0.4, AY3 + 0.75), (AX3, AY3 + 0.75))
ax.text(0.3, AY3 + 0.75, "Позиции заявок", ha="right", va="center",
        fontsize=9.5, color=INK)
# controls
c1x, c2x, c3x = cbt(AX1, AY1)[0] - 0.8, cbt(AX2, AY2)[0] - 0.8, cbt(AX3, AY3)[0]
c4x = cbt(AX4, AY4)[0]
# rail 1: роли пользователей -> A1, A4
arrow(ax, (c1x, 9.3), (c1x, AY1 + BH))
ax.text(c1x, 9.4, "Роли пользователей", ha="center", va="bottom", fontsize=9.5,
        color=INK)
line(ax, (c1x, 9.3), (c4x, 9.3))
arrow(ax, (c4x, 9.3), (c4x, AY4 + BH))
# rail 2: правила минимального запаса -> A2, A3
line(ax, (c2x, 8.3), (c3x, 8.3))
arrow(ax, (c2x, 8.3), (c2x, AY2 + BH))
arrow(ax, (c3x, 8.3), (c3x, AY3 + BH))
ax.text((c2x + c3x) / 2, 8.4, "Правила минимального запаса", ha="center",
        va="bottom", fontsize=9.5, color=INK)
# mechanisms
arrow(ax, (AX1 + BW / 2, 0.9), (AX1 + BW / 2, AY1))
ax.text(AX1 + BW / 2, 0.75, "Веб-приложение\n«Галамарт Склад»", ha="center",
        va="top", fontsize=9.5, color=INK)
arrow(ax, (AX4 + BW / 2, 0.9), (AX4 + BW / 2, AY4))
ax.text(AX4 + BW / 2, 0.75, "Браузер", ha="center", va="top", fontsize=9.5,
        color=INK)
# outputs
p3, p4 = cbr(AX3, AY3), cbr(AX4, AY4)
arrow(ax, p3, (15.4, p3[1]))
ax.text(15.5, p3[1], "Заявки\nпоставщикам", ha="left", va="center",
        fontsize=9.5, color=INK)
arrow(ax, p4, (15.4, p4[1]))
ax.text(15.5, p4[1], "Отчёты\nPDF / XLSX", ha="left", va="center",
        fontsize=9.5, color=INK)
save(fig, "idef0_system_decomp.png")

print("done")
