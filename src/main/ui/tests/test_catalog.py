from playwright.sync_api import expect
from src.main.ui.pages.catalog_page import CatalogPage

def test_count_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user","secret_sauce")
    assert catalog.get_products_count() == 6

def test_sorted_by_name(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user","secret_sauce")
    catalog.sort_item("az")
    assert catalog.get_product_names() == sorted(catalog.get_product_names())

    catalog.sort_item("za")
    assert catalog.get_product_names() == sorted(catalog.get_product_names(), reverse=True)

def test_sort_by_price(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user","secret_sauce")
    catalog.sort_item("lohi")
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices())

    catalog.sort_item("hilo")
    assert catalog.get_product_prices() == sorted(catalog.get_product_prices(), reverse=True)

def test_add_to_cart(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user","secret_sauce")

    button = catalog.add_to_cart("Sauce Labs Bike Light")
    expect(button).to_have_text("Remove")
    assert catalog.get_cart_count() == 1

def test_add_and_remove_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user","secret_sauce")
    catalog.add_to_cart("Sauce Labs Onesie")
    assert catalog.get_cart_count() == 1
    catalog.remove_from_cart("Sauce Labs Onesie")
    assert catalog.get_cart_count() == 0

def test_product_details_onesie(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user","secret_sauce")
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price

def test_product_fleece_jacket(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = catalog.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name
    assert price == detail_price

def test_remove_item_from_catalog(page):
    catalog = CatalogPage(page)
    catalog.login("standard_user", "secret_sauce")
    button = catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")
    expect(button).to_have_text("Remove")
    remove_button = catalog.remove_from_cart("Test.allTheThings() T-Shirt (Red)")
    expect(remove_button).to_have_text("Add to cart")
    assert catalog.get_cart_count() == 0




# -------- ТЕСТЫ БЕЗ PAGE OBJECT----------------
def test_count_catalog(auth_page):
    # ------------логинимся (код ниже заменен на фикстуру auth_page)
    page = auth_page
    page.goto("https://www.saucedemo.com/")
    page.get_by_placeholder("Username").fill("standart_user")
    page.get_by_placeholder("Password").fill("secret_sauce")
    page.locator("#login-button").click()
    products = page.locator(".inventory_item") # используем класс т.к. каждая карточка имеет класс
    assert products.count() == 6


def test_sorted_catalog(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    sort_select = auth_page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("az")

    # получаем список название товаров
    names = auth_page.locator(".inventory_item_name").all_text_contents()
    assert names == sorted(names), 'список не отсортирован по A-Z'

def test_sorted_catalog_reversed(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    sort_select = auth_page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("za")

    # получаем список название товаров
    names = auth_page.locator(".inventory_item_name").all_text_contents()
    assert names == sorted(names, reverse=True), 'список не отсортирован по Z-A'

def test_sorted_price_catalog(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    sort_select = auth_page.locator(".product_sort_container")
    expect(sort_select).to_be_visible(timeout=5000)

    sort_select.select_option("lohi")

    prices_text = auth_page.locator(".inventory_item_price").all_text_contents()
    prices = [float(p.replace("$", "")) for p in prices_text]
    assert prices == sorted(prices), 'Товары не отсортированы по цене low -> high'

    sort_select.select_option("hilo")

    prices_text = auth_page.locator(".inventory_item_price").all_text_contents()

    prices = [float(p.replace("$", "")) for p in prices_text]
    assert prices == sorted(prices, reverse=True), 'Товары не отсортированы по high -> low'

def test_add_to_cart(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    # добавляем товар в корзину
    product_card = auth_page.locator("inventory_item", has_text='Sauce Labs Bike Light')
    add_button = product_card.locator("button")
    add_button.click()
    # проверяем что кнопка изменилась на Remove
    expect(add_button).to_have_text("Remove")
    expect(auth_page.locator(".shopping_cart_badge")).to_have_text("1")


def test_add_to_cart_2(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    # добавляем товар в корзину
    product_card = auth_page.locator("inventory_item", has_text='Sauce Labs Onesie')
    add_button = product_card.locator("button")
    add_button.click()
    expect(add_button).to_have_text("Remove")
    # проверяем счетчик корзины
    card_badge = auth_page.locator("shopping_cart_badge")
    expect(card_badge).to_have_text("1")

    add_button.click()
    expect(add_button).to_have_text("Add to cart")
    expect(card_badge).not_to_be_visible()

def test_product_details_onesie(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    # находим карточку товара
    product_card = auth_page.locator("inventory_item", has_text='Sauce Labs Onesie')
    product_name = product_card.locator("[data-test='inventory-item-name']").inner_text()
    product_price = product_card.locator("[data-test='inventory-item-price']").inner_text()

    product_card.locator("[data-test='inventory-item-name']").click()

    detail_name = auth_page.locator("[data-test='inventory-item-name']").inner_text()
    detail_price = auth_page.locator("[data-test='inventory-item-price']").inner_text()
    assert detail_price == product_price
    assert detail_name == product_name

def test_product_details_fleece_jacket(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    # находим карточку товара
    product_card = auth_page.locator("inventory_item", has_text='Fleece Jacket')
    product_name = product_card.locator("[data-test='inventory-item-name']").inner_text()
    product_price = product_card.locator("[data-test='inventory-item-price']").inner_text()

    product_card.locator("[data-test='inventory-item-name']").click()

    detail_name = auth_page.locator("[data-test='inventory-item-name']").inner_text()
    detail_price = auth_page.locator("[data-test='inventory-item-price']").inner_text()
    assert detail_price == product_price, 'цена товара не совпадает'
    assert detail_name == product_name, 'название товара не совпадает'

def test_remove_item_from_catalog(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    product_card = auth_page.locator(".inventory_item", has_text='Test.allTheThings() T-Shirt (Red)')
    product_button = product_card.locator("[data-test='add-to-cart-test.allthethings()-t-shirt-(red)']")
    product_button.click()
    # проверяем что кнопка Remove появилась
    remove_button = product_card.locator("[data-test='remove-test.allthethings()-t-shirt-(red)']")
    assert remove_button.is_visible(), 'Кнопка Remove не появилась'

    remove_button.click()

    add_button = product_card.locator("[data-test='add-to-cart-test.allthethings()-t-shirt-(red)']")

    assert add_button.is_visible(), 'Кнопка add_cart не появилась'

def test_remove_onesie_from_catalog(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    product_card = auth_page.locator(".inventory_item", has_text='Sauce Labs Onesie')
    product_button = product_card.locator("[data-test='add-to-cart-sauce-labs-onesie']")
    product_button.click()
    # проверяем что кнопка Remove появилась
    remove_button = product_card.locator("[data-test='remove-sauce-labs-onesie']")
    assert remove_button.is_visible(), 'Кнопка Remove не появилась'

    remove_button.click()

    add_button = product_card.locator("[data-test='add-to-cart-sauce-labs-onesie']")

    assert add_button.is_visible(), 'Кнопка add_cart не появилась'








