"""Наполнение базы данных начальными данными."""
from app import create_app
from models import db, Category, Component, GameFPS

app = create_app()

CATEGORIES = ["CPU", "GPU", "RAM", "Motherboard", "PSU", "Storage"]

# (категория, название, цена, tdp, сокет, балл производительности)
COMPONENTS = [
    # CPU
    ("CPU", "AMD Ryzen 5 7500F", 11000, 65, "AM5", 70),
    ("CPU", "AMD Ryzen 5 7600X", 14000, 105, "AM5", 75),
    ("CPU", "AMD Ryzen 7 7700", 17000, 65, "AM5", 82),
    ("CPU", "AMD Ryzen 7 7800X3D", 29000, 120, "AM5", 95),
    ("CPU", "AMD Ryzen 9 9900X", 35000, 120, "AM5", 93),
    ("CPU", "AMD Ryzen 9 9950X", 42000, 170, "AM5", 98),
    ("CPU", "Intel Core i5-13400F", 13000, 65, "LGA1700", 72),
    ("CPU", "Intel Core i5-14600K", 22000, 125, "LGA1700", 80),
    ("CPU", "Intel Core i7-14700K", 33000, 125, "LGA1700", 90),
    ("CPU", "Intel Core i9-14900K", 45000, 253, "LGA1700", 97),
    # GPU
    ("GPU", "GeForce RTX 4060", 30000, 115, None, 62),
    ("GPU", "GeForce RTX 4060 Ti", 40000, 160, None, 70),
    ("GPU", "GeForce RTX 4070", 50000, 200, None, 78),
    ("GPU", "GeForce RTX 4070 Ti Super", 70000, 285, None, 85),
    ("GPU", "GeForce RTX 5060", 32000, 150, None, 72),
    ("GPU", "GeForce RTX 5060 Ti", 49000, 180, None, 80),
    ("GPU", "GeForce RTX 5070", 58000, 220, None, 88),
    ("GPU", "GeForce RTX 5080", 114000, 300, None, 95),
    ("GPU", "AMD Radeon RX 7600", 25000, 165, None, 60),
    ("GPU", "AMD Radeon RX 7800 XT", 45000, 263, None, 76),
    # RAM
    ("RAM", "Kingston Fury Beast 16GB DDR4", 3500, 5, None, 45),
    ("RAM", "Kingston Fury Beast 32GB DDR4", 30000, 8, None, 60),
    ("RAM", "Kingston Fury Beast 16GB DDR5", 27000, 8, None, 65),
    ("RAM", "Kingston Fury Beast 32GB DDR5", 43000, 10, None, 80),
    ("RAM", "Corsair Vengeance 16GB DDR5", 5500, 8, None, 63),
    ("RAM", "Corsair Vengeance 32GB DDR5", 9500, 10, None, 78),
    ("RAM", "G.Skill Trident Z5 32GB DDR5", 12000, 10, None, 85),
    # Motherboard
    ("Motherboard", "Gigabyte B760M DS3H DDR4", 9300, 25, "LGA1700", 55),
    ("Motherboard", "MSI PRO B760-P DDR5", 13000, 25, "LGA1700", 65),
    ("Motherboard", "ASUS TUF GAMING B760", 16000, 30, "LGA1700", 70),
    ("Motherboard", "ASUS ROG B650", 22000, 30, "AM5", 80),
    ("Motherboard", "MSI MAG B650 TOMAHAWK", 19000, 30, "AM5", 75),
    ("Motherboard", "Gigabyte B650 AORUS Elite", 17000, 28, "AM5", 73),
    # PSU
    ("PSU", "be quiet! System Power 550W", 5000, 0, None, 45),
    ("PSU", "be quiet! 650W", 7000, 0, None, 60),
    ("PSU", "Corsair RM750x", 10000, 0, None, 75),
    ("PSU", "Corsair RM850x", 13500, 0, None, 85),
    ("PSU", "Seasonic Focus GX-1000", 16000, 0, None, 92),
    # Storage
    ("Storage", "Kingston A2000 500GB", 4500, 5, None, 55),
    ("Storage", "Samsung 970 EVO 1TB", 8000, 6, None, 75),
    ("Storage", "Samsung 980 PRO 1TB", 10000, 7, None, 85),
    ("Storage", "WD Black SN850X 1TB", 9500, 7, None, 83),
    ("Storage", "Kingston KC3000 2TB", 14000, 7, None, 90),
    ("Storage", "Crucial P3 Plus 1TB", 6000, 5, None, 68),
]

# (игра, название GPU, название CPU, fps)
GAME_FPS = [
    # Cyberpunk 2077
    ("Cyberpunk 2077", "GeForce RTX 4060", "Intel Core i5-13400F", 50),
    ("Cyberpunk 2077", "GeForce RTX 4070", "Intel Core i7-14700K", 85),
    ("Cyberpunk 2077", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 65),
    ("Cyberpunk 2077", "GeForce RTX 5070", "AMD Ryzen 7 7700", 110),
    ("Cyberpunk 2077", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 160),
    ("Cyberpunk 2077", "AMD Radeon RX 7800 XT", "AMD Ryzen 7 7700", 70),
    # CS2
    ("CS2", "GeForce RTX 4060", "Intel Core i5-13400F", 220),
    ("CS2", "GeForce RTX 4070", "Intel Core i7-14700K", 380),
    ("CS2", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 280),
    ("CS2", "GeForce RTX 5070", "AMD Ryzen 7 7700", 450),
    ("CS2", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 600),
    ("CS2", "AMD Radeon RX 7800 XT", "AMD Ryzen 7 7700", 300),
    # GTA V
    ("GTA V", "GeForce RTX 4060", "Intel Core i5-13400F", 100),
    ("GTA V", "GeForce RTX 4070", "Intel Core i7-14700K", 150),
    ("GTA V", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 120),
    ("GTA V", "GeForce RTX 5070", "AMD Ryzen 7 7700", 180),
    ("GTA V", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 240),
    ("GTA V", "AMD Radeon RX 7800 XT", "AMD Ryzen 7 7700", 130),
    # Elden Ring
    ("Elden Ring", "GeForce RTX 4060", "Intel Core i5-13400F", 55),
    ("Elden Ring", "GeForce RTX 5060", "AMD Ryzen 5 7500F", 60),
    ("Elden Ring", "GeForce RTX 5070", "AMD Ryzen 7 7700", 60),
    ("Elden Ring", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 60),
    # Hogwarts Legacy
    ("Hogwarts Legacy", "GeForce RTX 4060", "Intel Core i5-13400F", 45),
    ("Hogwarts Legacy", "GeForce RTX 4070", "Intel Core i7-14700K", 75),
    ("Hogwarts Legacy", "GeForce RTX 5070", "AMD Ryzen 7 7700", 95),
    ("Hogwarts Legacy", "GeForce RTX 5080", "AMD Ryzen 7 7800X3D", 140),
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
