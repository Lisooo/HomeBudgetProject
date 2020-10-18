from flask import Blueprint, render_template
from app.models import Operation

operations = Blueprint('operations', __name__)

@operations.route("/operations")
def operations_list():
    list = Operation.query.filter_by(oprtn_dt='2020-04-01').order_by(Operation.oprtn_dt).all()
    return render_template('operations.html', title='Lista Operacji', list=list)
