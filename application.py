from flask import Flask, redirect, url_for
import os
from code import gca_dashboard
from code import gca_launchpad
def create_app():
    app = Flask(__name__)
    app.register_blueprint(gca_dashboard.bp)
    app.register_blueprint(gca_launchpad.bp)
    @app.route('/')
    def index():
	    return redirect(url_for('gca-dashboard.render_dash'))
    return app
app = create_app()
app.run()
