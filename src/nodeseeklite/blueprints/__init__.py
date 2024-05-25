from flask import Flask

from nodeseeklite.blueprints import main
from nodeseeklite.blueprints import setting


def register_blueprints(app: Flask):
    app.register_blueprint(main.blueprint)
    app.register_blueprint(setting.blueprint)
