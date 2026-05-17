from playwright.sync_api import expect
import pytest
from src.main.ui.pages.basket_page import BasketPage
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.checkout_page import CheckoutPage


def test_add_item_and_check_in_cart(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    catalog.login("standard_user", "secret_sauce")
    catalog.add_to_cart("Sauce Labs Backpack")
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")

def test_add_items_and_check_in_cart(page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standard_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    catalog.login("standard_user", "secret_sauce")
    # добавляем товары в корзину
    catalog.add_to_cart("Sauce Labs Bolt T-Shirt")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    # заходим в корзину
    basket.open_cart()
    # проверяем совпали ли имена
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.expect_item_in_cart("Sauce Labs Bolt T-Shirt")

def test_remove_item_from_basket(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    basket.remove_item("Sauce Labs Fleece Jacket")
    basket.expect_item_not_in_cart("Sauce Labs Fleece Jacket")


def test_remove_items_from_basket(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Test.allTheThings() T-Shirt (Red)")

    basket.open_cart()
    basket.expect_item_in_cart("Test.allTheThings() T-Shirt (Red)")
    basket.expect_item_in_cart("Sauce Labs Backpack")

    basket.remove_item("Test.allTheThings() T-Shirt (Red)")
    basket.remove_item("Sauce Labs Backpack")

    basket.expect_item_not_in_cart("Test.allTheThings() T-Shirt (Red)")
    basket.expect_item_not_in_cart("Sauce Labs Backpack")

def test_basket_multiple_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckoutPage(page)
    catalog.login("standard_user", "secret_sauce")

    catalog.add_to_cart("Sauce Labs Backpack")
    catalog.add_to_cart("Sauce Labs Fleece Jacket")
    # проверяем товары в корзине
    basket.open_cart()
    basket.expect_item_in_cart("Sauce Labs Backpack")
    basket.expect_item_in_cart("Sauce Labs Fleece Jacket")
    # считаем сумму корзины перед чекаутом
    total_basket = basket.get_item_total_price()

    # переходим в checkout
    basket.checkout()

    checkout.start_checkout(first_name='Test', last_name='Shiyanov', postal_code='1234')

    # проверяем сумму на чекаут
    checkout_total = checkout.get_item_total_after_continue()
    assert checkout_total == total_basket, 'Сумма товаров в чекаут не совпадает с корзиной'

def test_checkout_without_items(page):
    catalog = CatalogPage(page)
    basket = BasketPage(page)
    checkout = CheckoutPage(page)
    catalog.login("standard_user", "secret_sauce")
    basket.open_cart()
    items = basket.get_item_names()
    assert len(items) == 0, 'Корзина не пуста'
    basket.checkout()
    checkout.start_checkout(first_name='Test', last_name='Shiyanov', postal_code='')
    error_text = checkout.get_error_text()
    assert error_text != "", "Ожидалась ошибка при оформлении пустой корзины"





# -----------Тесты до Page Object----------------------
def test_total_price_for_cart_in_basket(auth_page):
    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    # добавляем товар в корзину
    auth_page.locator("[data-test='add-to-cart-sauce-labs-bolt-t-shirt']").click()
    auth_page.locator("[data-test='add-to-cart-sauce-labs-fleece-jacket']").click()
    # переходим в корзину
    auth_page.locator(".shopping_cart_link").click()
    # провeряем что товар в корзине
    bolt = auth_page.locator(".inventory_item_name", has_text = 'Sauce Labs Bolt T-Shirt')
    fleece = auth_page.locator(".inventory_item_name", has_text = 'Sauce Labs Fleece Jacket')
    expect(bolt).to_be_visible()
    expect(fleece).to_be_visible()
    # считаем стоимость товаров
    item_prices = auth_page.locator(".inventory_item_price").all_text_contents()
    price = [float(p.replace("$", "")) for p in item_prices]
    total_price = sum(price)
    # жмем чекаут
    auth_page.locator("#checkout").click()

    # заполняем checkout
    auth_page.get_by_placeholder("First Name").fill("Dmitry")
    auth_page.get_by_placeholder("Last Name").fill("Shiyanov")
    auth_page.get_by_placeholder("Zip/Postal Code").fill("1234")
    # жмем континью
    auth_page.locator("#continue").click()

    item_total = auth_page.locator("[data-test='subtotal-label']").inner_text()
    item_total_value = float(item_total.split("$")[1])
    # сравниваем значения что мы посчитали в total price с тем что забрали с локатора
    assert item_total_value == total_price
    # считаем tax
    tax = auth_page.locator("[data-test='tax-label']").inner_text()
    tax_value = float(tax.split("$")[1])
    # считаем total сумму
    total = auth_page.locator("[data-test='total-label']").inner_text()
    total_value = float(total.split("$")[1])
    # сравниваем значения
    assert total_value == round( item_total_value + tax_value, 2)
    # жмем финиш
    auth_page.locator("[data-test='finish']").click()

    success_message = auth_page.locator(".complete-header")
    expect(success_message).to_have_text("Thank you for your order!")

def test_checkout_without_items(auth_page):
    """ Негативный тест """

    # page.goto("https://www.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("standart_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()

    bolt = auth_page.locator(".inventory_item_name", has_text='Sauce Labs Bolt T-Shirt')
    fleece = auth_page.locator(".inventory_item_name", has_text='Sauce Labs Fleece Jacket')
    expect(bolt).to_be_visible()
    expect(fleece).to_be_visible()

    # жмем чекаут
    auth_page.locator("#checkout").click()

    # заполняем checkout
    auth_page.get_by_placeholder("First Name").fill("Dmitry")
    auth_page.get_by_placeholder("Last Name").fill("Shiyanov")

    auth_page.locator("#continue").click()

    error_message = auth_page.locator("[data-test='error']")
    expect(error_message).to_have_text('Error: Postal Code is required')
