from src.main.ui.pages.catalog_page import CatalogPage
from src.main.ui.steps.catalog_steps import CatalogSteps
from src.main.ui.steps.login_steps import LoginSteps

def test_auth(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    # проверяем что мы на странице каталога после логина
    catalog_page = CatalogPage(page)
    assert catalog_page.get_products_count() > 0 , 'Ожидаем товары на странице'

def test_login_locked_user(page):
    steps = LoginSteps(page)
    steps.open_login_page().login("standard_user", "secret_sauce")
    # получаем текст ошибки
    error_text = steps.get_error_text()
    assert "locked out" in error_text, 'Ожидаем сообщение о заблокированном пользователе'

def test_logout(page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)
    login_steps.open_login_page().login("standard_user", "secret_sauce")
    assert catalog_steps.get_products_count() > 0, "Ожидаем товары в каталоге"
    catalog_steps.logout()
    assert page.url == login_steps.LOGIN_URL, "Ожидаем возврат на страницу логина"


def test_logout_visual_user(page):
    login_steps = LoginSteps(page)
    catalog_steps = CatalogSteps(page)
    login_steps.open_login_page().login("visual_user", "secret_sauce")
    assert catalog_steps.get_products_count() > 0, "Ожидаем товары в каталоге"
    catalog_steps.logout()
    assert page.url == login_steps.LOGIN_URL, "Ожидаем возврат на страницу логина"

