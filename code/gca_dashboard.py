from flask import (
Blueprint, render_template, request)
bp = Blueprint('gca-dashboard', __name__, url_prefix = '/gca-dashboard' )
@bp.route('/dashboard-index', methods = ('GET', 'POST'))
def render_dash():
    if request.method == 'GET':
        return render_template('gca-dashboard/index.html')
@bp.route('/get-involved', methods = ('GET', 'POST'))
def render_get_involved():
    if request.method == 'GET':
        return render_template('gca-dashboard/get-involved.html')
