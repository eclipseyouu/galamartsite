# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, FancyArrowPatch
from matplotlib.lines import Line2D
import os

OUT = r"C:\Users\user\Desktop\практичке\pp11\diagrams"
SLATE = "#334155"
GREEN = "#059669"
LIGHT = "#f1f5f9"
BORDER = "#cbd5e1"
INK = "#0f172a"
MUTED = "#475569"


def new_fig(w=16.0, h=10.0):
    fig, ax = plt.subplots(figsize=(w, h), dpi=150)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 10)
    ax.axis("off")
    return fig, ax


def title(ax, text, y=9.6):
    ax.text(8.0, y, text, ha="center", va="center", fontsize=16,
            fontweight="bold", color=INK)


def arrow(ax, p1, p2, color=INK, lw=1.6, style="-|>", rad=0.0, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, color=color, lw=lw,
                 mutation_scale=14, connectionstyle=f"arc3,rad={rad}",
                 linestyle=ls, zorder=3))


def _spread(n):
    if n == 1:
        return [0.5]
    return [0.15 + 0.70 * i / (n - 1) for i in range(n)]


def idef0(fname, ttl, box_title, inputs, controls, mechanisms, outputs):
    fig, ax = new_fig()
    title(ax, ttl)
    bx0, bx1, by0, by1 = 5.2, 10.8, 4.1, 6.1
    ax.add_patch(FancyBboxPatch((bx0, by0), bx1 - bx0, by1 - by0,
                 boxstyle="round,pad=0.03,rounding_size=0.1", linewidth=1.6,
                 edgecolor=SLATE, facecolor=LIGHT, zorder=2))
    ax.text((bx0 + bx1) / 2, (by0 + by1) / 2, box_title, ha="center",
            va="center", fontsize=12.5, fontweight="bold", color=INK, zorder=4,
            wrap=True)
    # inputs (left)
    n = len(inputs)
    for i, t in enumerate(inputs):
        y = by1 - (by1 - by0) * (i + 1) / (n + 1)
        arrow(ax, (1.4, y), (bx0, y))
        ax.text(1.25, y, t, ha="right", va="center", fontsize=10, color=INK)
    # controls (top)
    for i, t in enumerate(controls):
        x = bx0 + (bx1 - bx0) * _spread(len(controls))[i]
        arrow(ax, (x, 8.5), (x, by1))
        ax.text(x, 8.62, t, ha="center", va="bottom", fontsize=9.5, color=INK)
    # mechanisms (bottom)
    for i, t in enumerate(mechanisms):
        x = bx0 + (bx1 - bx0) * _spread(len(mechanisms))[i]
        arrow(ax, (x, 1.5), (x, by0))
        ax.text(x, 1.38, t, ha="center", va="top", fontsize=9.5, color=INK)
    # outputs (right)
    n = len(outputs)
    for i, t in enumerate(outputs):
        y = by1 - (by1 - by0) * (i + 1) / (n + 1)
        arrow(ax, (bx1, y), (14.6, y))
        ax.text(14.75, y, t, ha="left", va="center", fontsize=10, color=INK)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


def stick(ax, x, y, label):
    ax.add_patch(Ellipse((x, y + 0.62), 0.30, 0.30, facecolor="white",
                 edgecolor=SLATE, lw=1.6, zorder=4))
    ax.add_line(Line2D([x, x], [y + 0.47, y + 0.05], color=SLATE, lw=1.6, zorder=4))
    ax.add_line(Line2D([x - 0.22, x + 0.22], [y + 0.36, y + 0.36], color=SLATE, lw=1.6, zorder=4))
    ax.add_line(Line2D([x, x - 0.18], [y + 0.05, y - 0.28], color=SLATE, lw=1.6, zorder=4))
    ax.add_line(Line2D([x, x + 0.18], [y + 0.05, y - 0.28], color=SLATE, lw=1.6, zorder=4))
    ax.text(x, y - 0.45, label, ha="center", va="top", fontsize=10.5,
            fontweight="bold", color=INK)


def usecase(fname, ttl, actors, cases):
    fig, ax = new_fig()
    title(ax, ttl)
    bx0, bx1, by0, by1 = 5.2, 10.8, 0.9, 8.6
    ax.add_patch(Rectangle((bx0, by0), bx1 - bx0, by1 - by0, linewidth=1.6,
                 edgecolor=SLATE, facecolor="#f8fafc", zorder=1))
    ax.text((bx0 + bx1) / 2, by1 - 0.35, "Галамарт Склад", ha="center",
            va="center", fontsize=12.5, fontweight="bold", color=SLATE, zorder=4)
    cx = (bx0 + bx1) / 2
    # cases: dict name -> (y, [actor names])
    ys = [7.7, 6.85, 6.0, 5.15, 4.3, 3.45, 2.6, 1.75]
    pos = {}
    for i, (name, acc) in enumerate(cases):
        y = ys[i]
        pos[name] = (cx, y)
        ax.add_patch(Ellipse((cx, y), 4.4, 0.62, facecolor="white",
                     edgecolor=GREEN, lw=1.4, zorder=3))
        ax.text(cx, y, name, ha="center", va="center", fontsize=10, color=INK, zorder=4)
    # actors
    ax_pos = {}
    for name, side, y in actors:
        x = 2.0 if side == "left" else 14.0
        ax_pos[name] = (x, y)
        stick(ax, x, y, name)
    # links
    for name, acc in cases:
        ccx, ccy = pos[name]
        for a in acc:
            axx, ayy = ax_pos[a]
            x0 = axx + (0.35 if axx < ccx else -0.35)
            x1 = ccx + (-2.25 if axx < ccx else 2.25)
            arrow(ax, (x0, ayy + 0.15), (x1, ccy), color=MUTED, lw=1.1,
                  style="-", rad=0.0)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


def sequence(fname, ttl, lifelines, messages):
    fig, ax = new_fig(h=9.5)
    title(ax, ttl, y=9.2)
    xs = {}
    for i, name in enumerate(lifelines):
        x = 2.2 + i * 3.9
        xs[name] = x
        ax.add_patch(FancyBboxPatch((x - 1.5, 8.15), 3.0, 0.55,
                     boxstyle="round,pad=0.02,rounding_size=0.08",
                     linewidth=1.4, edgecolor=SLATE, facecolor=SLATE, zorder=3))
        ax.text(x, 8.42, name, ha="center", va="center", fontsize=10.5,
                fontweight="bold", color="white", zorder=4)
        ax.add_line(Line2D([x, x], [1.0, 8.15], color=BORDER, lw=1.2,
                    linestyle=(0, (4, 3)), zorder=1))
    y = 7.55
    dy = 0.72
    for frm, to, text, ret in messages:
        y0 = y - len([m for m in messages[:messages.index((frm, to, text, ret))]]) * 0
    # draw in order
    yy = 7.55
    for idx, (frm, to, text, ret) in enumerate(messages):
        x0, x1 = xs[frm], xs[to]
        if frm == to:
            arrow(ax, (x0, yy), (x0 + 1.1, yy), color=MUTED, lw=1.3, style="-")
            arrow(ax, (x0 + 1.1, yy), (x0 + 1.1, yy - 0.22), color=MUTED, lw=1.3, style="-")
            arrow(ax, (x0 + 1.1, yy - 0.22), (x0, yy - 0.22), color=MUTED, lw=1.3)
            ax.text(x0 + 1.2, yy - 0.11, text, ha="left", va="center", fontsize=9.5, color=INK)
        else:
            style = "-->" if ret else "->"
            arrow(ax, (x0, yy), (x1, yy), color=(MUTED if ret else INK),
                  lw=1.3, style="-|>", ls=("--" if ret else "-"))
            mx = (x0 + x1) / 2
            ax.text(mx, yy + 0.12, text, ha="center", va="bottom", fontsize=9.5,
                    color=INK)
        yy -= dy
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, fname), dpi=150, bbox_inches="tight",
                facecolor="white")
    plt.close(fig)


# ---- 1.1 IDEF0 «как есть» ----
idef0("idef0_asis.png",
      "Процесс складского учёта «как есть» (A-0)",
      "Учёт складских\nостатков (вручную)",
      ["Данные о товарах", "Фактические остатки"],
      ["Правила минимального запаса", "Учётная политика"],
      ["Товаровед", "Excel / бумажные журналы"],
      ["Заявка поставщику", "Отчёты (вручную)"])

# ---- 2.1 IDEF0 системы ----
idef0("idef0_system.png",
      "Функциональная модель системы (A-0)",
      "Управление\nскладскими остатками",
      ["Данные о товарах", "Остатки", "Позиции заявок"],
      ["Правила минимального запаса", "Роли пользователей"],
      ["Веб-приложение «Галамарт Склад»", "Браузер"],
      ["Актуальный каталог", "Заявки поставщикам", "Отчёты PDF / XLSX"])

# ---- 2.2 Use Case ----
actors = [("Администратор", "left", 7.4),
          ("Товаровед", "left", 4.0),
          ("Директор", "right", 4.6)]
cases = [
    ("Войти в систему", ["Администратор", "Товаровед", "Директор"]),
    ("Управлять пользователями", ["Администратор"]),
    ("Вести каталог товаров", ["Товаровед"]),
    ("Контролировать остатки", ["Товаровед"]),
    ("Формировать заявку", ["Товаровед"]),
    ("Получать поставку", ["Товаровед"]),
    ("Формировать отчёты", ["Директор"]),
]
usecase("usecase.png", "Диаграмма вариантов использования", actors, cases)

# ---- 2.3 Sequence ----
lifelines = ["Товаровед", "Веб-приложение", "Хранилище", "Поставщик"]
messages = [
    ("Товаровед", "Веб-приложение", "Выбрать дефицитные товары", False),
    ("Веб-приложение", "Хранилище", "Запрос остатков", False),
    ("Хранилище", "Веб-приложение", "Список позиций", True),
    ("Веб-приложение", "Веб-приложение", "Сформировать заявку", False),
    ("Веб-приложение", "Поставщик", "Отправить заявку (status = sent)", False),
    ("Поставщик", "Веб-приложение", "Поставка (status = received)", True),
    ("Веб-приложение", "Хранилище", "Обновить остатки", False),
    ("Веб-приложение", "Товаровед", "Остатки обновлены", True),
]
sequence("sequence.png", "Диаграмма последовательности: оформление заявки",
         lifelines, messages)

print("done")
