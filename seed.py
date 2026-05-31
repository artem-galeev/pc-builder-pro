"""Наполнение базы данных начальными данными."""
from app import create_app
from models import db, Category, Component, GameFPS

app = create_app()

CATEGORIES = ["CPU", "GPU", "RAM", "Motherboard", "PSU", "Storage"]

# (категория, название, цена, tdp, сокет, балл производительности)
COMPONENTS = [
    ("CPU", "AMD Ryzen 5 7500F", 11000, 65, "AM5", 70),
    ("CPU", "AMD Ryzen 7 7700", 17000, 65, "AM5", 82),
    ("CPU", "AMD Ryzen 7 7800X3D", 29000, 120, "AM5", 95),
    ("CPU", "AMD Ryzen 9 9950X", 42000, 170, "AM5", 98),
    ("GPU", "GeForce RTX 5060", 32000, 150, None, 70),
    ("GPU", "GeForce RTX 5060 Ti", 49000, 180, None, 80),
    ("GPU", "GeForce RTX 5070", 58000, 220, None, 88),
    ("GPU", "GeForce RTX 5080", 114000, 300, None, 95),
    ("RAM", "Kingston Fury Beast 16GB DDR5", 27000, 8, None, 65),
    ("RAM", "Kingston Fury Beast 32GB DDR5", 43000, 10, None, 80),
    ("RAM", "Kingston Fury Beast 32GB DDR4", 30000, 8, None, 60),
    ("Motherboard", "Gigabyte B760M DS3H DDR4", 9300, 25, "LGA1700", 55),
    ("Motherboard", "ASUS ROG B650", 22000, 30, "AM5", 80),
    ("PSU", "be quiet! 650W", 7000, 0, None, 60),
    ("PSU", "Corsair RM850x", 12000, 0, None, 85),
    ("Storage", "Samsung 970 EVO 1TB", 8000, 6, None, 80),
    ("Storage", "Kingston A2000 500GB", 4500, 5, None, 65),
]

# (игра, название GPU, название CPU, fps)
GAME_FPS = [
    ("Cyberpunk 2077", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 65),
    ("Cyberpunk 2077", "GeForce RTX 5070", "AMD Ryzen 7 7700", 110),
    ("Cyberpunk 2077", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 160),
    ("CS2", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 280),
    ("CS2", "GeForce RTX 5070", "AMD Ryzen 7 7700", 450),
    ("CS2", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 600),
    ("GTA V", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 120),
    ("GTA V", "GeForce RTX 5070", "AMD Ryzen 7 7700", 180),
    ("GTA V", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 240),
]


def seed():
    db.drop_all()
    db.create_all()

    cats = {name: Category(name=name) for name in CATEGORIES}
    db.session.add_all(cats.values())
    db.session.commit()

    comps = {}
    for cat_name, name, price, tdp, socket, perf in COMPONENTS:
        c = Component(
            category_id=cats[cat_name].id, name=name, price=price,
            tdp=tdp, socket=socket, performance=perf,
        )
        db.session.add(c)
        comps[name] = c
    db.session.commit()

    for game, gpu_name, cpu_name, fps in GAME_FPS:
        db.session.add(GameFPS(
            game=game, gpu_id=comps[gpu_name].id,
            cpu_id=comps[cpu_name].id, fps=fps,
        ))
    db.session.commit()
    print(f"Готово: {len(CATEGORIES)} категорий, {len(COMPONENTS)} комплектующих, {len(GAME_FPS)} записей FPS.")


if __name__ == "__main__":
    with app.app_context():
        seed()
