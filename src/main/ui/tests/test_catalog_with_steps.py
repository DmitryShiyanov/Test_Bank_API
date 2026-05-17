from playwright.sync_api import expect, Page
from src.main.ui.steps.catalog_steps import CatalogSteps

def test_count_catalog(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    assert step.get_products_count() == 6

def test_sorted_by_name(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")

    step.sort_items("az")
    assert step.get_product_names() == sorted(step.get_product_names())

    step.sort_items("za")
    assert step.get_product_names() == sorted(step.get_product_names(), reverse=True)

def test_sort_by_price(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    step.sort_items("lohi")
    assert step.get_product_prices() == sorted(step.get_product_prices())

    step.sort_items("hilo")
    assert step.get_product_prices() == sorted(step.get_product_prices(), reverse=True)

def test_add_to_cart(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    step.add_to_cart("Sauce Labs Bike Light")
    assert step.get_cart_count() == 1

def test_add_and_remove_onesie(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    step.add_to_cart("Sauce Labs Onesie")
    assert step.get_cart_count() == 1
    step.remove_from_cart("Sauce Labs Onesie")
    assert step.get_cart_count() == 0

def test_product_details_onesie(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    name, price, detail_name, detail_price = step.open_product_details("Sauce Labs Onesie")
    assert name == detail_name
    assert price == detail_price

def test_product_details_fleece_jacket(page):
    step = CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    name, price, detail_price, detail_name = step.open_product_details("Sauce Labs Fleece Jacket")
    assert name == detail_name
    assert price == detail_price

def test_remove_item_from_catalog(page):
    step =  CatalogSteps(page)
    step.login("standard_user", "secret_sauce")
    step.add_to_cart("Sauce Labs Fleece Jacket")
    step.remove_from_cart("Sauce Labs Fleece Jacket")



