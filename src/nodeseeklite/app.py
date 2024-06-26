import logging
import os

from flask import Flask

from nodeseeklite.blueprints import register_blueprints
from nodeseeklite.config import config
from nodeseeklite.models import db
from nodeseeklite.models import register_models

logging.basicConfig(format=config.LOGGING_FORMAT, level=config.LOGGING_LEVEL)
logger = logging.getLogger(__name__)

app = Flask(__name__, instance_path=os.getcwd())
app.config.update(config.model_dump())

app.json.ensure_ascii = False
app.json.mimetype = "application/json; charset=utf-8"

register_models(app)
register_blueprints(app)

with app.app_context():
    db.create_all()
