"""Проверка совместимости комплектующих сборки."""


def check_compatibility(cpu, motherboard):
    """Проверяет совместимость CPU и материнской платы по сокету.

    Возвращает список предупреждений (пустой = всё совместимо).
    """
    warnings = []
    if cpu and motherboard:
        if cpu.socket and motherboard.socket and cpu.socket != motherboard.socket:
            warnings.append(
                f"Сокет процессора ({cpu.socket}) не совпадает с сокетом "
                f"материнской платы ({motherboard.socket})."
            )
    return warnings
