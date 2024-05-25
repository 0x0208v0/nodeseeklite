from flask import Blueprint
from flask import render_template

blueprint = Blueprint('setting', __name__)


@blueprint.get('/setting')
def index():
    return render_template(
        'setting/index.html',
    )
