from logging import getLogger, NullHandler, CRITICAL

from flask import Flask, render_template, request
from flask.logging import default_handler

from .auth import login_manager
from .data import db
import flask_tracking.errors as errors
import flask_tracking.logger as logger
from .tracking.views import tracking
from .users.views import users

#print(log)

getLogger('werkzeug').disabled = True
getLogger(__name__).addHandler(NullHandler())

app = Flask(__name__)
#app.config.from_object('config.DevelopmentConfiguration')
app.config.from_object('config.ProductionConfiguration')

db.init_app(app)
login_manager.init_app(app)
errors.init_app(app)

logger.init_app(app, app.logger.level) if\
    app.logger.level != 0 else\
    logger.init_app(app, app.logger.parent.level)

app.register_blueprint(tracking)
app.register_blueprint(users)


@app.before_request
def log_it():
    app.logger.info("Handling Request")


@app.context_processor
def provide_constants():
    return {"constants": {"TUTORIAL_PART": 2}}
