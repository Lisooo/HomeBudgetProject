from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

# APP
app = Flask(__name__)
app.config.from_object(config['default'])

db = SQLAlchemy(app)

# ROUTES
from app_4_website.main.routes import main
from app_4_website.operations.routes import operations
from app_4_website.balances.routes import balances
from app_4_website.dictionaries.routes import dicts
from app_4_website.pty_oprtn_cd_clssfctn.routes import pocc

# BLUEPRINTS
app.register_blueprint(main)
app.register_blueprint(operations)
app.register_blueprint(balances)
app.register_blueprint(dicts)
app.register_blueprint(pocc)