# -*- coding: utf-8 -*-
"""Снимает скриншоты интерфейса «Галамарт Склад» для отчёта ПМ.11.
Запуск: сначала `python -m http.server 8000` в корне pp11, затем этот скрипт.
"""
import sys
from pathlib import Path

import pymupdf
from playwright.sync_api import sync_playwright

BASE = "http://127.0.0.1:8000/index.html"
OUT = Path(r"C:\Users\user\Desktop\практичке\pp11\diagrams\screens")
OUT.mkdir(parents=True, exist_ok=True)

ADMIN_ID = 1
DESKTOP = (1440, 1000)
MOBILE = (375, 812)


def init_script(session_id):
    js = "try{localStorage.setItem('galamart_onboard_hidden','1');}catch(e){}"
    if session_id is None:
        js += "try{localStorage.removeItem('galamart_session');}catch(e){}"
    else:
        js += f"try{{localStorage.setItem('galamart_session','{session_id}');}}catch(e){{}}"
    return js


def open_page(browser, session_id, viewport):
    ctx = browser.new_context(
        viewport={"width": viewport[0], "height": viewport[1]},
        device_scale_factor=2,
        locale="ru-RU",
    )
    ctx.add_init_script(init_script(session_id))
    page = ctx.new_page()
    page.goto(BASE, wait_until="networkidle", timeout=90000)
    page.evaluate("document.fonts && document.fonts.ready")
    page.wait_for_timeout(900)
    return ctx, page


def scroll_to(page, selector, offset=80):
    page.evaluate(
        """(a)=>{const el=document.querySelector(a.s);if(el){const y=el.getBoundingClientRect().top+window.scrollY-a.o;window.scrollTo(0,y);}}""",
        {"s": selector, "o": offset},
    )
    page.wait_for_timeout(500)


def shot(page, name):
    path = OUT / name
    page.screenshot(path=str(path))
    print("saved", path.name)


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(channel="msedge", headless=True)

        # 3.1 Дашборд (главный экран), админ
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        scroll_to(pg, "#dashboard")
        shot(pg, "fig_3_1_dashboard.png")
        ctx.close()

        # 3.2 Товары
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        scroll_to(pg, "#products")
        shot(pg, "fig_3_2_products.png")
        ctx.close()

        # 3.3 Заявки
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        scroll_to(pg, "#orders")
        shot(pg, "fig_3_3_orders.png")
        ctx.close()

        # 3.4 Адаптив 375px — карточки товаров
        ctx, pg = open_page(browser, ADMIN_ID, MOBILE)
        scroll_to(pg, "#products", 60)
        shot(pg, "fig_3_4_mobile.png")
        ctx.close()

        # 4.1 Окно входа (без сессии)
        ctx, pg = open_page(browser, None, DESKTOP)
        pg.wait_for_selector("#authOverlay:not(.hidden)")
        shot(pg, "fig_4_1_login.png")
        ctx.close()

        # 4.2 Дашборд после входа (в шапке — админ)
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        scroll_to(pg, "#dashboard", 0)
        shot(pg, "fig_4_2_dashboard_admin.png")
        ctx.close()

        # 4.3 Добавление товара
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        pg.click("#btnAddProduct")
        pg.wait_for_selector("#productModal:not(.hidden)")
        pg.wait_for_timeout(400)
        shot(pg, "fig_4_3_product_add.png")
        ctx.close()

        # 4.4 Формирование заявки
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        pg.click("#btnNewOrder")
        pg.wait_for_selector("#orderModal:not(.hidden)")
        pg.wait_for_timeout(500)
        shot(pg, "fig_4_4_order_form.png")
        ctx.close()

        # 4.5 Отчёт о дефицитных товарах
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        scroll_to(pg, "#reports")
        shot(pg, "fig_4_5_deficit_report.png")
        ctx.close()

        # 4.6 Выгрузка PDF — генерируем и рендерим первую страницу
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        with pg.expect_download() as dl:
            pg.click("#btnPdfDeficit")
        pdf_path = OUT / "_deficit.pdf"
        dl.value.save_as(str(pdf_path))
        doc = pymupdf.open(str(pdf_path))
        pix = doc[0].get_pixmap(matrix=pymupdf.Matrix(3, 3))
        pix.save(str(OUT / "fig_4_6_pdf_export.png"))
        doc.close()
        pdf_path.unlink(missing_ok=True)
        print("saved fig_4_6_pdf_export.png")
        ctx.close()

        # 4.7 Валидация формы — убираем required, показываем toast приложения
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        pg.click("#btnAddProduct")
        pg.wait_for_selector("#productModal:not(.hidden)")
        pg.evaluate("document.querySelectorAll('#productForm [required]').forEach(e=>e.removeAttribute('required'))")
        pg.click("#productForm button[type=submit]")
        pg.wait_for_timeout(150)
        shot(pg, "fig_4_7_validation.png")
        ctx.close()

        # А.1 Порядок входа — заполненные поля
        ctx, pg = open_page(browser, None, DESKTOP)
        pg.wait_for_selector("#authOverlay:not(.hidden)")
        pg.fill("#loginLogin", "admin")
        pg.fill("#loginPass", "123")
        shot(pg, "fig_A_1_login_steps.png")
        ctx.close()

        # А.2 Порядок создания заявки — поставщик выбран, позиции отмечены
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        pg.evaluate("openOrderModal(1)")
        pg.wait_for_selector("#orderModal:not(.hidden)")
        pg.wait_for_timeout(500)
        shot(pg, "fig_A_2_order_steps.png")
        ctx.close()

        # Г.1 Карточка входных данных — редактирование товара (заполнено)
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        pg.evaluate("openProductModal(101)")
        pg.wait_for_selector("#productModal:not(.hidden)")
        pg.wait_for_timeout(400)
        shot(pg, "fig_G_1_input_card.png")
        ctx.close()

        # Г.2 Пример отчётных данных — карточка отчёта «Дефицит»
        ctx, pg = open_page(browser, ADMIN_ID, DESKTOP)
        pg.locator("#reports .card").first.screenshot(
            path=str(OUT / "fig_G_2_report_data.png")
        )
        print("saved fig_G_2_report_data.png")
        ctx.close()

        browser.close()
    print("ALL DONE")


if __name__ == "__main__":
    sys.exit(main())
