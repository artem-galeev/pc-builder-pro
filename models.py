from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Category(db.Model):
    """Категория комплектующих: CPU, GPU, RAM, и т.д."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    components = db.relationship("Component", backref="category", lazy=True)

    def __repr__(self):
        return f"<Category {self.name}>"


class Component(db.Model):
    """Комплектующее (деталь ПК)."""
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    price = db.Column(db.Float, default=0)        # цена, ₽
    tdp = db.Column(db.Integer, default=0)         # потребление, Вт
    socket = db.Column(db.String(30))              # сокет (для совместимости CPU/мать)
    performance = db.Column(db.Integer, default=0)  # условный балл производительности

    def __repr__(self):
        return f"<Component {self.name}>"


class GameFPS(db.Model):
    """Ожидаемый FPS в игре для связки GPU + CPU."""
    id = db.Column(db.Integer, primary_key=True)
    game = db.Column(db.String(80), nullable=False)
    gpu_id = db.Column(db.Integer, db.ForeignKey("component.id"), nullable=False)
    cpu_id = db.Column(db.Integer, db.ForeignKey("component.id"), nullable=False)
    fps = db.Column(db.Integer, default=0)

    gpu = db.relationship("Component", foreign_keys=[gpu_id])
    cpu = db.relationship("Component", foreign_keys=[cpu_id])
