"""Парсинг цен комплектующих с внешних сайтов.

ВНИМАНИЕ: DNS-shop и подобные магазины защищены анти-бот системами
(Cloudflare, проверка JS), поэтому прямой парсинг через requests часто
блокируется. Функции написаны с устойчивой обработкой ошибок: при сбое
возвращается None, и приложение продолжает работать на данных из БД.
"""
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9",
}

TIMEOUT = 10


def _extract_price(text):
    """Извлекает число цены из строки вида '12 999 ₽'."""
    digits = re.sub(r"[^\d]", "", text)
    return int(digits) if digits else None


def fetch_price(query):
    """Пытается найти цену товара по названию через поиск DNS.

    Возвращает int (цена в рублях) или None при неудаче.
    """
    url = "https://www.dns-shop.ru/search/"
    try:
        resp = requests.get(
            url, params={"q": query}, headers=HEADERS, timeout=TIMEOUT
        )
        resp.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    tag = soup.select_one(".product-buy__price")
    if tag:
        return _extract_price(tag.get_text())
    return None


def update_component_price(component):
    """Обновляет цену комплектующего, если парсинг удался.

    Возвращает True при успешном обновлении, иначе False.
    """
    new_price = fetch_price(component.name)
    if new_price:
        component.price = new_price
        return True
    return False
