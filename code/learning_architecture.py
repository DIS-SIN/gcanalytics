from flask import (
    Blueprint, render_template, request)
bp = Blueprint('learning-architecture', __name__,
               url_prefix='/learning-architecture')


@bp.route('/tree', methods=('GET', 'POST'))
def render_dash():
    if request.method == 'GET':
        return render_template('learning-architecture/index.html')
