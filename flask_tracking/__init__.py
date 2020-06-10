import logging
from logging import NullHandler

from flask import Flask, render_template, request
from flask.logging import default_handler

from .auth import login_manager
from .data import db
import flask_tracking.errors as errors
import flask_tracking.logging as logging
from .tracking.views import tracking
from .users.views import users


log = logging.getLogger('werkzeug')
log.disabled = True
logging.getLogger(__name__).addHandler(NullHandler())

app = Flask(__name__)

#app.config.from_object('config.BaseConfiguration')
app.config.from_object('config.DebugConfiguration')
#app.logger.removeHandler(default_handler)


db.init_app(app)
login_manager.init_app(app)
errors.init_app(app)
logging.init_app(app)


app.register_blueprint(tracking)
app.register_blueprint(users)


@app.before_request
def log_it():
    app.logger.debug("Handling Request")


@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 2}}