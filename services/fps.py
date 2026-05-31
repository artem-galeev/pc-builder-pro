"""Прогноз FPS в играх для связки видеокарта + процессор."""
from models import GameFPS, Component


def predict_fps(gpu_id, cpu_id):
    """Возвращает список (игра, fps) для выбранной связки GPU+CPU.

    Логика:
    1. Если есть точная запись в БД — возвращает её.
    2. Иначе — оценивает FPS по баллам производительности выбранных
       GPU/CPU относительно известных записей в таблице GameFPS.
    """
    if not gpu_id or not cpu_id:
        return []

    # 1. Точное совпадение
    exact = GameFPS.query.filter_by(gpu_id=gpu_id, cpu_id=cpu_id).all()
    if exact:
        return [(r.game, r.fps) for r in exact]

    # 2. Оценка по производительности
    gpu = Component.query.get(gpu_id)
    cpu = Component.query.get(cpu_id)
    if not gpu or not cpu:
        return []

    # Берём все записи FPS и группируем по играм
    all_records = GameFPS.query.all()
    if not all_records:
        return []

    games = {}
    for r in all_records:
        games.setdefault(r.game, []).append(r)

    result = []
    for game, records in games.items():
        # Для каждой игры: средний FPS, средний балл GPU и CPU из записей
        fps_values, gpu_perfs, cpu_perfs = [], [], []
        for r in records:
            ref_gpu = Component.query.get(r.gpu_id)
            ref_cpu = Component.query.get(r.cpu_id)
            if ref_gpu and ref_cpu:
                fps_values.append(r.fps)
                gpu_perfs.append(ref_gpu.performance or 50)
                cpu_perfs.append(ref_cpu.performance or 50)

        if not fps_values:
            continue

        avg_fps = sum(fps_values) / len(fps_values)
        avg_gpu_perf = sum(gpu_perfs) / len(gpu_perfs)
        avg_cpu_perf = sum(cpu_perfs) / len(cpu_perfs)

        # Масштабируем: FPS пропорционален производительности GPU (70%) и CPU (30%)
        gpu_ratio = (gpu.performance or 50) / avg_gpu_perf
        cpu_ratio = (cpu.performance or 50) / avg_cpu_perf
        estimated = avg_fps * (gpu_ratio * 0.7 + cpu_ratio * 0.3)

        result.append((game, round(estimated)))

    return sorted(result, key=lambda x: x[0])
