from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# APP
app = Flask(__name__)
app.config.from_object(config['default'])

db = SQLAlchemy(app)

# ROUTES
from app.main.routes import main
from app.operations.routes import operations
from app.balances.routes import balances
from app.dictionaries.routes import dicts
from app.pty_oprtn_cd_clssfctn.routes import pocc

# BLUEPRINTS
app.register_blueprint(main)
app.register_blueprint(operations)
app.register_blueprint(balances)
app.register_blueprint(dicts)
app.register_blueprint(pocc)