from playwright.sync_api import expect
import pytest
from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.pages.login_page import LoginPage


def test_auth(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standart_user", "secret_sauce")

    expect(page).to_have_url("https://wwww.saucedemo.com/inventory.html")
    # или так
    assert page.url == "https://wwww.saucedemo.com/inventory.html"

def test_auth_locked_out_user(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("locked_out_user","secret_sauce")
    expect(page).to_have_url(LoginPage.URL)
    error_text = login_page.get_error_text()
    assert 'locked_out' in error_text

    #-------------------- старый кусок кода
    page.locator("#login-button").click()
    # -------проверяем что url не изменился
    expect(page).to_have_url("https://wwww.saucedemo.com/")
    # -------находим локатор ошибки
    error = page.locator("h3[data-test='error']")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Epic sadface: Username and password do not match any user in this service")


def test_logout(page):
    # ---------логинимся  (этот код заменили фикстурой auth_page)
    #page.goto("https://wwww.saucedemo.com/")
    #page.get_by_placeholder("Username").fill("standart_user")
    #page.get_by_placeholder("Password").fill("secret_sauce")
    #page.locator("#login-button").click()
    # ---------проверяем страницу логина

    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")

    catalog = CatalogPage(page)
    # проверяем что мы на странице каталога
    assert catalog.get_products_count() > 0

    # лог аут
    catalog.logout()
    expect(page).to_have_url(LoginPage.URL)

def test_logout_visual_user(page):

    # page.goto("https://wwww.saucedemo.com/")
    # page.get_by_placeholder("Username").fill("visual_user")
    # page.get_by_placeholder("Password").fill("secret_sauce")
    # page.locator("#login-button").click()
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("visual_user","secret_sauce")

    catalog = CatalogPage(page)
    # проверяем что мы на странице каталога
    assert catalog.get_products_count() > 0

    # лог аут
    catalog.logout()
    # проверяем что мы на странице логина
    expect(page).to_have_url(LoginPage.URL)
