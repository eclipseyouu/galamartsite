# -*- coding: utf-8 -*-
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
from matplotlib.lines import Line2D

FIG_W, FIG_H = 16.0, 10.5
fig, ax = plt.subplots(figsize=(FIG_W, FIG_H), dpi=150)
ax.set_xlim(0, 16)
ax.set_ylim(0, 11)
ax.axis("off")

HEAD_H = 0.46
ROW_H = 0.34
BOX_W = 4.3

def draw_box(x, y_top, title, fields):
    """fields: list of (name, tag) where tag in {'PK','FK','UQ',''}"""
    h = HEAD_H + ROW_H * len(fields)
    y0 = y_top - h
    # shadow
    ax.add_patch(FancyBboxPatch((x + 0.04, y0 - 0.04), BOX_W, h,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 linewidth=0, facecolor="#c9d2dc", zorder=1))
    # body
    ax.add_patch(FancyBboxPatch((x, y0), BOX_W, h,
                 boxstyle="round,pad=0.02,rounding_size=0.08",
                 linewidth=1.4, edgecolor="#334155", facecolor="white", zorder=2))
    # header
    ax.add_patch(Rectangle((x, y_top - HEAD_H), BOX_W, HEAD_H,
                 linewidth=0, facecolor="#334155", zorder=3))
    ax.text(x + BOX_W / 2, y_top - HEAD_H / 2, title, ha="center", va="center",
            color="white", fontsize=13, fontweight="bold", zorder=4)
    # fields
    for i, (name, tag) in enumerate(fields):
        cy = y_top - HEAD_H - ROW_H * (i + 0.5)
        label = name
        style = {}
        if tag == "PK":
            style = dict(fontweight="bold")
        elif tag == "FK":
            style = dict(fontstyle="italic")
        ax.text(x + 0.18, cy, label, ha="left", va="center",
                fontsize=10.5, color="#0f172a", zorder=4, **style)
        if tag:
            ax.text(x + BOX_W - 0.18, cy, tag, ha="right", va="center",
                    fontsize=9, color="#059669", fontweight="bold", zorder=4)
    return dict(x=x, y0=y0, y_top=y_top, w=BOX_W, h=h,
                left=x, right=x + BOX_W, top=y_top, bottom=y0,
                cx=x + BOX_W / 2, cy=(y_top + y0) / 2)

def connect(a, b, la, lb, label="1:N", color="#0f172a", lw=1.5, rad=0.0):
    x1, y1 = a
    x2, y2 = b
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-", color=color, lw=lw,
                                connectionstyle=f"arc3,rad={rad}"), zorder=1)
    ax.text(la[0], la[1], "1", ha="center", va="center", fontsize=11,
            fontweight="bold", color=color,
            bbox=dict(boxstyle="circle,pad=0.12", fc="white", ec=color, lw=1.1), zorder=5)
    ax.text(lb[0], lb[1], "N", ha="center", va="center", fontsize=11,
            fontweight="bold", color=color,
            bbox=dict(boxstyle="circle,pad=0.12", fc="white", ec=color, lw=1.1), zorder=5)
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    ax.text(mx, my, label, ha="center", va="center", fontsize=9.5,
            color="#475569", bbox=dict(boxstyle="round,pad=0.18", fc="#f1f5f9",
            ec="#cbd5e1", lw=0.8), zorder=6)

# --- boxes ---
categories = draw_box(0.35, 10.55, "categories", [("id", "PK"), ("name", "UQ")])
users = draw_box(5.85, 10.55, "users",
                 [("id", "PK"), ("login", "UQ"), ("password_hash", ""),
                  ("name", ""), ("role", ""), ("status", ""), ("created_at", "")])
suppliers = draw_box(11.35, 10.55, "suppliers",
                     [("id", "PK"), ("name", ""), ("contact", ""),
                      ("phone", ""), ("created_at", "")])
products = draw_box(5.85, 6.75, "products",
                    [("id", "PK"), ("sku", "UQ"), ("name", ""),
                     ("category_id", "FK"), ("supplier_id", "FK"),
                     ("unit", ""), ("location", ""), ("min_stock", ""),
                     ("price", ""), ("created_at", "")])
stock = draw_box(0.9, 3.45, "stock",
                 [("id", "PK"), ("product_id", "FK"), ("quantity", ""),
                  ("updated_at", "")])
orders = draw_box(11.35, 6.75, "orders",
                  [("id", "PK"), ("supplier_id", "FK"), ("status", ""),
                   ("comment", ""), ("created_at", "")])
order_items = draw_box(11.35, 3.45, "order_items",
                       [("id", "PK"), ("order_id", "FK"), ("product_id", "FK"),
                        ("qty", ""), ("price", "")])

# --- connections ---
# categories -> products
connect((categories["right"], categories["cy"] - 0.4),
        (products["left"], products["top"] - 1.0),
        (categories["right"] + 0.28, categories["cy"] - 0.4),
        (products["left"] - 0.28, products["top"] - 1.0),
        "1:N", rad=0.18)
# suppliers -> products
connect((suppliers["left"], suppliers["cy"] - 0.6),
        (products["right"], products["top"] - 1.0),
        (suppliers["left"] - 0.28, suppliers["cy"] - 0.6),
        (products["right"] + 0.28, products["top"] - 1.0),
        "1:N", rad=-0.18)
# suppliers -> orders
connect((suppliers["cx"] + 1.2, suppliers["bottom"]),
        (orders["cx"] + 1.2, orders["top"]),
        (suppliers["cx"] + 1.2, suppliers["bottom"] - 0.22),
        (orders["cx"] + 1.2, orders["top"] + 0.22),
        "1:N")
# orders -> order_items
connect((orders["cx"] + 1.2, orders["bottom"]),
        (order_items["cx"] + 1.2, order_items["top"]),
        (orders["cx"] + 1.2, orders["bottom"] - 0.22),
        (order_items["cx"] + 1.2, order_items["top"] + 0.22),
        "1:N")
# products -> stock
connect((products["left"] + 0.5, products["bottom"]),
        (stock["right"], stock["top"] - 0.3),
        (products["left"] + 0.5, products["bottom"] - 0.22),
        (stock["right"] + 0.28, stock["top"] - 0.3),
        "1:1", rad=0.12)
# products -> order_items
connect((products["right"] - 0.6, products["bottom"]),
        (order_items["left"], order_items["cy"]),
        (products["right"] - 0.6, products["bottom"] - 0.22),
        (order_items["left"] - 0.28, order_items["cy"]),
        "1:N", rad=-0.15)

# --- users note ---
ax.text(users["cx"], users["bottom"] - 0.18,
        "аутентификация (без связей с другими таблицами)",
        ha="center", va="top", fontsize=9, color="#64748b", fontstyle="italic")

# --- title ---
ax.text(8.0, 10.9, "ER-диаграмма базы данных «Галамарт Склад»",
        ha="center", va="center", fontsize=16, fontweight="bold", color="#0f172a")

# legend
leg = [Line2D([0], [0], color="#0f172a", lw=1.5),
       Line2D([0], [0], marker="o", color="w", markerfacecolor="white",
              markeredgecolor="#0f172a", markersize=10)]
ax.text(0.35, 0.55, "PK — первичный ключ     FK — внешний ключ     UQ — уникальное поле",
        ha="left", va="center", fontsize=9.5, color="#475569")

plt.tight_layout()
out = r"C:\Users\user\Desktop\практичке\pp11\diagrams\er_database.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
print("saved", out)
