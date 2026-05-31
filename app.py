from flask import Flask, render_template, request
from config import Config
from models import db, Category, Component


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    register_routes(app)
    return app


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


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
