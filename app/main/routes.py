from flask import Blueprint, render_template
from app.balances.utils import YearlyBal, MonthlyBal
from app.import_log.utills import get_last_operation_dt
from datetime import date

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home(p_year=date.today().year, p_month=date.today().month):
    monthly_bal = MonthlyBal(p_year, p_month).summary_all()
    yearly_bal = YearlyBal(p_year).summary()
    v_loaded_operation_dt = get_last_operation_dt()

    return render_template('home.html', monthly_bal=monthly_bal, yearly_bal=yearly_bal, v_loaded_operation_dt=v_loaded_operation_dt)
