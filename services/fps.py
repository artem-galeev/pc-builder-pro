"""Прогноз FPS в играх для связки видеокарта + процессор."""
from models import GameFPS


def predict_fps(gpu_id, cpu_id):
    """Возвращает список (игра, fps) для выбранной связки GPU+CPU.

    Если точной записи нет, оценивает FPS по ближайшей записи для этой GPU.
    """
    if not gpu_id or not cpu_id:
        return []

    exact = GameFPS.query.filter_by(gpu_id=gpu_id, cpu_id=cpu_id).all()
    if exact:
        return [(r.game, r.fps) for r in exact]

    # запасной вариант: усреднить по GPU и срезать 15% за неоптимальный CPU
    by_gpu = GameFPS.query.filter_by(gpu_id=gpu_id).all()
    result = {}
    for r in by_gpu:
        result.setdefault(r.game, []).append(r.fps)
    return [(game, round(sum(v) / len(v) * 0.85)) for game, v in result.items()]
