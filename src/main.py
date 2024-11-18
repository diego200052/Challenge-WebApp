from flask import Flask
from views.dashboard import dashboard
from views.expenses import expenses
from views.payments import payments
from core.config import settings
from utils.filters import format_currency

app = Flask(__name__, static_folder="assets")
app.config.from_object("core.config.Settings")
app.secret_key = settings.SECRET_KEY
app.jinja_env.globals.update(zip=zip)

app.register_blueprint(dashboard, url_prefix="/")
app.register_blueprint(expenses, url_prefix="/")
app.register_blueprint(payments, url_prefix="/")

app.template_filter("currency")(format_currency)
