from flask import Flask, render_template, request, redirect, url_for, flash
from config import Config
from models import db, Category, Component
from services.power import total_power, recommended_psu
from services.fps import predict_fps
from services.compatibility import check_compatibility
from parsers.dns_parser import update_component_price


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    register_routes(app)

    # Обновляем цены при запуске приложения
    with app.app_context():
        _update_all_prices()

    return app


def _update_all_prices():
    """Обновляет цены всех комплектующих из внешних источников."""
    components = Component.query.all()
    updated = 0
    for comp in components:
        if update_component_price(comp):
            updated += 1
    if updated:
        db.session.commit()
    return updated, len(components)


def register_routes(app):
    @app.route("/")
    def index():
        categories = Category.query.all()
        return render_template("index.html", categories=categories)

    @app.route("/catalog")
    def catalog():
        category_id = request.args.get("category", type=int)
        categories = Category.query.all()
        query = Component.query
        if category_id:
            query = query.filter_by(category_id=category_id)
        components = query.order_by(Component.price).all()
        return render_template(
            "catalog.html",
            categories=categories,
            components=components,
            selected=category_id,
        )

    @app.route("/build", methods=["GET", "POST"])
    def build():
        cats = ["CPU", "Motherboard", "GPU", "RAM", "PSU", "Storage"]
        options = {
            name: Component.query.join(Category)
            .filter(Category.name == name)
            .order_by(Component.price)
            .all()
            for name in cats
        }

        selected, result = {}, None
        if request.method == "POST":
            chosen = []
            for name in cats:
                cid = request.form.get(name, type=int)
                comp = Component.query.get(cid) if cid else None
                selected[name] = cid
                if comp:
                    chosen.append(comp)

            cpu = next((c for c in chosen if c.category.name == "CPU"), None)
            mb = next((c for c in chosen if c.category.name == "Motherboard"), None)
            gpu = next((c for c in chosen if c.category.name == "GPU"), None)

            result = {
                "total_price": sum(c.price for c in chosen),
                "power": total_power(chosen),
                "psu": recommended_psu(chosen),
                "warnings": check_compatibility(cpu, mb),
                "fps": predict_fps(gpu.id if gpu else None, cpu.id if cpu else None),
            }

        return render_template(
            "build.html", options=options, selected=selected, result=result
        )

    @app.route("/update-prices", methods=["POST"])
    def update_prices():
        updated, total = _update_all_prices()
        flash(f"Обновлено {updated} из {total} цен.", "success")
        return redirect(url_for("catalog"))

    @app.route("/update-price/<int:component_id>", methods=["POST"])
    def update_price(component_id):
        component = Component.query.get_or_404(component_id)
        if update_component_price(component):
            db.session.commit()
            flash(f"Цена «{component.name}» обновлена: {component.price:.0f} ₽", "success")
        else:
            flash(
                f"Не удалось получить цену «{component.name}» "
                f"(сайт недоступен или защищён от парсинга).",
                "warning",
            )
        return redirect(url_for("catalog"))

    # ==================== АДМИН-ПАНЕЛЬ ====================

    @app.route("/admin")
    def admin():
        components = Component.query.order_by(Component.category_id, Component.name).all()
        categories = Category.query.all()
        return render_template("admin/index.html", components=components, categories=categories)

    @app.route("/admin/add", methods=["GET", "POST"])
    def admin_add():
        categories = Category.query.all()
        if request.method == "POST":
            comp = Component(
                category_id=request.form.get("category_id", type=int),
                name=request.form.get("name", "").strip(),
                price=request.form.get("price", 0, type=float),
                tdp=request.form.get("tdp", 0, type=int),
                socket=request.form.get("socket", "").strip() or None,
                performance=request.form.get("performance", 0, type=int),
            )
            db.session.add(comp)
            db.session.commit()
            flash(f"Добавлено: {comp.name}", "success")
            return redirect(url_for("admin"))
        return render_template("admin/form.html", categories=categories, comp=None)

    @app.route("/admin/edit/<int:component_id>", methods=["GET", "POST"])
    def admin_edit(component_id):
        comp = Component.query.get_or_404(component_id)
        categories = Category.query.all()
        if request.method == "POST":
            comp.category_id = request.form.get("category_id", type=int)
            comp.name = request.form.get("name", "").strip()
            comp.price = request.form.get("price", 0, type=float)
            comp.tdp = request.form.get("tdp", 0, type=int)
            comp.socket = request.form.get("socket", "").strip() or None
            comp.performance = request.form.get("performance", 0, type=int)
            db.session.commit()
            flash(f"Обновлено: {comp.name}", "success")
            return redirect(url_for("admin"))
        return render_template("admin/form.html", categories=categories, comp=comp)

    @app.route("/admin/delete/<int:component_id>", methods=["POST"])
    def admin_delete(component_id):
        comp = Component.query.get_or_404(component_id)
        name = comp.name
        db.session.delete(comp)
        db.session.commit()
        flash(f"Удалено: {name}", "danger")
        return redirect(url_for("admin"))


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
