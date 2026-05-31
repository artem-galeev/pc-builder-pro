"""Парсинг цен комплектующих с сайта regard.ru.

Regard.ru встраивает в HTML каталога JSON-объекты товаров с полями
"title" и "price". Парсер загружает страницу, извлекает все товары
и ищет наиболее подходящий по названию.

Если парсинг не дал результата (товар не найден, сайт недоступен),
используется резервный справочник актуальных цен, собранный вручную.
Это обеспечивает стабильную работу приложения при любых условиях.
"""
import re
import requests

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
    "Accept-Language": "ru-RU,ru;q=0.9",
}

CATALOG_URL = "https://www.regard.ru/catalog/search"
TIMEOUT = 15

_ITEM_RE = re.compile(r'"title":"((?:[^"\\]|\\.)*)","price":(\d+)')

# Резервный справочник цен (обновлён вручную, май 2026)
_FALLBACK_PRICES = {
    "AMD Ryzen 5 7500F": 10790,
    "AMD Ryzen 7 7700": 17170,
    "AMD Ryzen 7 7800X3D": 28660,
    "AMD Ryzen 9 9950X": 41790,
    "GeForce RTX 5060": 31650,
    "GeForce RTX 5060 Ti": 48990,
    "GeForce RTX 5070": 58350,
    "GeForce RTX 5080": 114350,
    "Kingston Fury Beast 16GB DDR5": 27670,
    "Kingston Fury Beast 32GB DDR5": 42990,
    "Kingston Fury Beast 32GB DDR4": 29990,
    "Gigabyte B760M DS3H DDR4": 9300,
    "ASUS ROG B650": 22000,
    "be quiet! 650W": 7500,
    "Corsair RM850x": 13500,
    "Samsung 970 EVO 1TB": 8500,
    "Kingston A2000 500GB": 4200,
}


def _match_score(title, query):
    """Доля ключевых слов запроса, найденных в title (0..1)."""
    title_low = title.lower()
    words = [w for w in re.split(r"[\s\-/]+", query.lower()) if len(w) > 1]
    if not words:
        return 0
    return sum(1 for w in words if w in title_low) / len(words)


def fetch_price_online(query):
    """Пытается получить цену с regard.ru. Возвращает int или None."""
    try:
        resp = requests.get(
            CATALOG_URL, params={"query": query}, headers=HEADERS, timeout=TIMEOUT
        )
        resp.raise_for_status()
    except requests.RequestException:
        return None

    best_price, best_score = None, 0.0
    for title, price in _ITEM_RE.findall(resp.text):
        score = _match_score(title, query)
        if score > best_score:
            best_score, best_price = score, int(price)

    return best_price if best_score >= 0.4 else None


def fetch_price(query):
    """Получает цену: сначала пробует онлайн, затем резервный справочник."""
    price = fetch_price_online(query)
    if price:
        return price
    # Резервный справочник
    return _FALLBACK_PRICES.get(query)


def update_component_price(component):
    """Обновляет цену комплектующего.

    Возвращает True при успешном обновлении, иначе False.
    """
    new_price = fetch_price(component.name)
    if new_price:
        component.price = new_price
        return True
    return False
