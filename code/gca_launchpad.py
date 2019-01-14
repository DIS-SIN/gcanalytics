from flask import (
Blueprint, render_template, request)
bp = Blueprint('gca-launchpad', __name__, url_prefix = '/gca-launchpad')
@bp.route('/launchpad-index', methods = ('GET', 'POST'))
def render_dash():
    if request.method == 'GET':
        return render_template('gca-launchpad/index.html')
