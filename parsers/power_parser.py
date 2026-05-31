"""Парсинг энергопотребления (TDP) комплектующих.

Многие технические сайты также защищены, поэтому используется справочная
таблица типовых значений TDP как надёжный источник, а парсинг — как
дополнение. При неудаче парсинга возвращается значение из справочника.
"""
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    ),
}

TIMEOUT = 10


def fetch_tdp_from_web(query):
    """Пытается найти TDP в Вт по названию через поиск.

    Возвращает int или None при неудаче.
    """
    try:
        resp = requests.get(
            "https://www.google.com/search",
            params={"q": f"{query} TDP watt"},
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        resp.raise_for_status()
    except requests.RequestException:
        return None

    soup = BeautifulSoup(resp.text, "html.parser")
    match = re.search(r"(\d{2,3})\s*(?:W|Вт|watt)", soup.get_text(), re.IGNORECASE)
    return int(match.group(1)) if match else None


def update_component_tdp(component):
    """Обновляет TDP комплектующего, если парсинг удался.

    Возвращает True при успешном обновлении, иначе False.
    """
    tdp = fetch_tdp_from_web(component.name)
    if tdp:
        component.tdp = tdp
        return True
    return False
