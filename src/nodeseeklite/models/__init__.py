from flask import Flask

from nodeseeklite.models.base import db
from nodeseeklite.models.post import Post


def register_models(app: Flask):
    db.init_app(app)
