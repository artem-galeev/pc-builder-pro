"""Наполнение базы данных начальными данными."""
from app import create_app
from models import db, Category, Component, GameFPS

app = create_app()

CATEGORIES = ["CPU", "GPU", "RAM", "Motherboard", "PSU", "Storage"]

# (категория, название, цена, tdp, сокет, балл производительности)
COMPONENTS = [
    ("CPU", "Intel Core i5-12400F", 12000, 65, "LGA1700", 70),
    ("CPU", "Intel Core i7-13700K", 32000, 125, "LGA1700", 92),
    ("CPU", "AMD Ryzen 5 5600", 11000, 65, "AM4", 68),
    ("CPU", "AMD Ryzen 7 7800X3D", 38000, 120, "AM5", 95),
    ("GPU", "NVIDIA RTX 3060", 28000, 170, None, 65),
    ("GPU", "NVIDIA RTX 4070", 55000, 200, None, 85),
    ("GPU", "NVIDIA RTX 4090", 180000, 450, None, 100),
    ("GPU", "AMD RX 7600", 30000, 165, None, 63),
    ("RAM", "Kingston Fury 16GB DDR4", 4000, 8, None, 50),
    ("RAM", "Corsair Vengeance 32GB DDR5", 9000, 10, None, 75),
    ("Motherboard", "ASUS PRIME B660", 13000, 25, "LGA1700", 60),
    ("Motherboard", "MSI B550 TOMAHAWK", 14000, 25, "AM4", 62),
    ("Motherboard", "ASUS ROG B650", 22000, 30, "AM5", 80),
    ("PSU", "be quiet! 650W", 7000, 0, None, 60),
    ("PSU", "Corsair RM850x", 12000, 0, None, 85),
    ("Storage", "Samsung 970 EVO 1TB", 8000, 6, None, 80),
    ("Storage", "Kingston A2000 500GB", 4500, 5, None, 65),
]

# (игра, название GPU, название CPU, fps)
GAME_FPS = [
    ("Cyberpunk 2077", "NVIDIA RTX 3060", "Intel Core i5-12400F", 55),
    ("Cyberpunk 2077", "NVIDIA RTX 4070", "Intel Core i7-13700K", 95),
    ("Cyberpunk 2077", "NVIDIA RTX 4090", "AMD Ryzen 7 7800X3D", 160),
    ("CS2", "NVIDIA RTX 3060", "Intel Core i5-12400F", 240),
    ("CS2", "NVIDIA RTX 4070", "Intel Core i7-13700K", 400),
    ("CS2", "NVIDIA RTX 4090", "AMD Ryzen 7 7800X3D", 600),
    ("GTA V", "NVIDIA RTX 3060", "Intel Core i5-12400F", 110),
    ("GTA V", "NVIDIA RTX 4070", "Intel Core i7-13700K", 165),
    ("GTA V", "NVIDIA RTX 4090", "AMD Ryzen 7 7800X3D", 240),
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
