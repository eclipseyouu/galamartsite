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

XLIM = (-0.6, 13.0)
YLIM = (0.6, 7.4)
BW, BH = 2.2, 1.15
X = [0.9, 3.65, 6.4, 9.15]
Y = [4.8, 3.75, 2.7, 1.65]


def new_fig():
    fig, ax = plt.subplots(figsize=(13.6, 6.8), dpi=150)
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.axis("off")
    return fig, ax


def arrow(ax, p1, p2, color=INK, lw=1.5):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle="-|>", color=color, lw=lw,
                 mutation_scale=12, zorder=3))


def line(ax, p1, p2, color=INK, lw=1.5):
    ax.add_line(Line2D([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw,
                zorder=3))


def elbow(ax, pts, label=None, ly_off=0.16, ha="center", lx=None):
    for a, b in zip(pts, pts[1:-1]):
        line(ax, a, b)
    arrow(ax, pts[-2], pts[-1])
    if label:
        lx = lx if lx is not None else (pts[0][0] + pts[-2][0]) / 2
        ly = pts[0][1] + ly_off if ly_off >= 0 else pts[0][1] + ly_off
        ax.text(lx, ly, label, ha=ha, va="bottom", fontsize=8.5, color=INK)


def box(ax, i, node, label):
    x0, y0 = X[i], Y[i]
    ax.add_patch(FancyBboxPatch((x0, y0), BW, BH,
                 boxstyle="round,pad=0.03,rounding_size=0.07", linewidth=1.5,
                 edgecolor=SLATE, facecolor=LIGHT, zorder=2))
    ax.text(x0 + BW / 2, y0 + BH - 0.22, node, ha="center", va="center",
            fontsize=9, color=SLATE, zorder=4)
    ax.text(x0 + BW / 2, y0 + BH / 2 - 0.14, label, ha="center", va="center",
            fontsize=10, fontweight="bold", color=INK, zorder=4)


def rmid(i):
    return (X[i] + BW, Y[i] + BH / 2)


def lmid(i):
    return (X[i], Y[i] + BH / 2)


def tmid(i, off=0.0):
    return (X[i] + BW / 2 + off, Y[i] + BH)


def bmid(i, off=0.0):
    return (X[i] + BW / 2 + off, Y[i])


def chain(ax, labels):
    for i, lbl in enumerate(labels):
        p0, p1 = rmid(i), lmid(i + 1)
        arrow(ax, p0, p1)
        ax.text(p0[0] + 0.07, p0[1] + 0.14, lbl, ha="left", va="bottom",
                fontsize=8.5, color=INK)


def inp(ax, i, text, dy=0.0):
    y = Y[i] + BH / 2 + dy
    arrow(ax, (X[i] - 0.5, y), (X[i], y))
    ax.text(X[i] - 0.6, y, text, ha="right", va="center", fontsize=8.5,
            color=INK)


def outp(ax, i, text, dy=0.0):
    y = Y[i] + BH / 2 + dy
    x1 = X[i] + BW + 0.45
    arrow(ax, (X[i] + BW, y), (x1, y))
    ax.text(x1 + 0.08, y, text, ha="left", va="center", fontsize=8.5,
            color=INK)


def mech(ax, i, text, off=0.0):
    x = X[i] + BW / 2 + off
    arrow(ax, (x, Y[i] - 0.45), (x, Y[i]))
    ax.text(x, Y[i] - 0.55, text, ha="center", va="top", fontsize=8.5,
            color=INK)


def save(fig, fname):
    fig.savefig(os.path.join(OUT, fname), dpi=150, bbox_inches="tight",
                pad_inches=0.08, facecolor="white")
    plt.close(fig)


# ================= AS-IS =================
fig, ax = new_fig()
ax.text(6.2, 7.05, "Декомпозиция функции А0 складского учёта «как есть»",
        ha="center", va="center", fontsize=13.5, fontweight="bold", color=INK)
for i, (node, lbl) in enumerate([
        ("А1", "Вести журнал\nтоваров"),
        ("А2", "Сверять фактические\nостатки"),
        ("А3", "Формировать заявку\nпоставщику"),
        ("А4", "Составлять\nотчёты")]):
    box(ax, i, node, lbl)
chain(ax, ["Журнал остатков", "Сведения о дефиците", "Согласованная заявка"])
# feedback A4 -> A1
elbow(ax, [tmid(3), (tmid(3)[0], 6.7), (1.2, 6.7), tmid(0, -0.8)])
ax.text(5.7, 6.62, "Ведомость расхождений", ha="center", va="top",
        fontsize=8.5, color=INK)
# inputs
inp(ax, 0, "Данные\nо товарах")
inp(ax, 1, "Фактические\nостатки")
# controls
arrow(ax, (1.55, 6.35), (1.55, Y[0] + BH))
line(ax, (1.55, 6.35), (4.3, 6.35))
arrow(ax, (4.3, 6.35), (4.3, Y[1] + BH))
ax.text(2.9, 6.42, "Учётная политика", ha="center", va="bottom", fontsize=8.5,
        color=INK)
arrow(ax, (7.5, 5.25), (7.5, Y[2] + BH))
ax.text(7.5, 5.32, "Правила минимального запаса", ha="center", va="bottom",
        fontsize=8.5, color=INK)
# mechanisms
mech(ax, 0, "Товаровед", off=-0.6)
mech(ax, 2, "Товаровед")
mech(ax, 3, "Excel / бумажные\nжурналы")
# outputs
outp(ax, 2, "Заявка\nпоставщику")
outp(ax, 3, "Отчёты\n(вручную)")
save(fig, "idef0_asis_decomp.png")

# ================= TO-BE =================
fig, ax = new_fig()
ax.text(6.2, 7.05, "Декомпозиция функции А0 информационной системы",
        ha="center", va="center", fontsize=13.5, fontweight="bold", color=INK)
for i, (node, lbl) in enumerate([
        ("А1", "Вести каталог\nтоваров"),
        ("А2", "Контролировать\nостатки"),
        ("А3", "Формировать заявки\nпоставщикам"),
        ("А4", "Формировать\nотчёты")]):
    box(ax, i, node, lbl)
chain(ax, ["Каталог товаров", "Список дефицитных позиций", "Статусы заявок"])
# feedback A4 -> A2
elbow(ax, [tmid(3), (tmid(3)[0], 6.8), (tmid(1, -0.45)[0], 6.8),
           tmid(1, -0.45)])
ax.text(7.28, 6.72, "Актуальные отчётные данные", ha="center", va="top",
        fontsize=8.5, color=INK)
# inputs
inp(ax, 0, "Данные\nо товарах")
inp(ax, 1, "Остатки")
inp(ax, 2, "Позиции заявок")
# controls
arrow(ax, (1.55, 6.35), (1.55, Y[0] + BH))
line(ax, (1.55, 6.35), (9.8, 6.35))
arrow(ax, (9.8, 6.35), (9.8, Y[3] + BH))
ax.text(3.0, 6.42, "Роли пользователей", ha="center", va="bottom",
        fontsize=8.5, color=INK)
line(ax, (4.45, 5.55), (7.95, 5.55))
arrow(ax, (4.45, 5.55), (4.45, Y[1] + BH))
arrow(ax, (7.95, 5.55), (7.95, Y[2] + BH))
ax.text(6.2, 5.62, "Правила минимального запаса", ha="center", va="bottom",
        fontsize=8.5, color=INK)
# mechanisms
mech(ax, 0, "Веб-приложение\n«Галамарт Склад»", off=-0.6)
mech(ax, 3, "Браузер")
# outputs
outp(ax, 2, "Заявки\nпоставщикам")
outp(ax, 3, "Отчёты\nPDF / XLSX")
save(fig, "idef0_system_decomp.png")

print("done")
