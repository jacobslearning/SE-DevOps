import os
import logging
from flask import Flask, redirect
from database import db
from routes.assets import assets_blueprint
from routes.auth import auth_blueprint
from routes.dashboard import dashboard_blueprint
from routes.departments import departments_blueprint
from routes.users import users_blueprint
from routes.logs import logs_blueprint
from dotenv import load_dotenv
load_dotenv()

# app create for tests and prod


def create_app(config_object=None):
    app = Flask(__name__)

    app.logger.setLevel(logging.INFO)
    app.secret_key = "test"

    if config_object:
        app.config.from_object(config_object)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
            "SQLALCHEMY_DATABASE_URI"
        )

    db.init_app(app)

    # register blueprints
    app.register_blueprint(assets_blueprint)
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(dashboard_blueprint)
    app.register_blueprint(departments_blueprint)
    app.register_blueprint(users_blueprint)
    app.register_blueprint(logs_blueprint)

    @app.errorhandler(404)
    def page_not_found(e):
        return redirect("/")

    return app


app = create_app()


if __name__ == '__main__':
    app = create_app()
    host = os.getenv("FLASK_HOST", "127.0.0.1")
    port = int(os.getenv("FLASK_PORT", 5000))
    app.run(host=host, port=port)
