"""Расчёт энергопотребления сборки и рекомендация по блоку питания."""


def total_power(components):
    """Сумма TDP всех комплектующих (Вт)."""
    return sum(c.tdp or 0 for c in components)


def recommended_psu(components, reserve=0.3):
    """Рекомендуемая мощность БП с запасом (по умолчанию +30%)."""
    base = total_power(components)
    return round(base * (1 + reserve))
