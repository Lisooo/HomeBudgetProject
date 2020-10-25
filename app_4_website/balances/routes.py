from flask import Blueprint, render_template, request
from app_4_website.balances.utils import MonthlyDtlBal, YearlyDtlBal, MonthlyCtgBal
from datetime import datetime

balances = Blueprint('balances', __name__)


@balances.route("/monthly_dtl_bal")
@balances.route("/monthly_dtl_bal_<int:p_year>_<int:p_month>")
def monthly_dtl_bal(p_year=datetime.today().year, p_month=datetime.today().month):
    page = request.args.get('page', 1, type=int)

    colors = [
        "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
        "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
        "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

    v_list = MonthlyDtlBal(p_year, p_month).summary_paginated(page=page)
    v_ctg_chart_data = MonthlyCtgBal(p_year, p_month).query_result_all('2', 'N')    # only expenses - 2; not detailed - N
    # v_sctg_chart_data = MonthlyCtgBal(p_year, p_month).query_result_all('2', 'T')

    v_ctg_label_list = []
    v_ctg_value_list = []

    for item in v_ctg_chart_data:
        v_ctg_label_list.append(item.GROUP_NM)
        v_ctg_value_list.append(item.TRNSCTN_SUM)

    return render_template('monthly_dtl_bal.html', title='PODSUMOWANIE MIESIĄCA', p_year=p_year, p_month=p_month, v_list=v_list, labels=v_ctg_label_list, values=v_ctg_value_list, colors=colors)


@balances.route("/yearly_dtl_bal")
def yearly_dtl_bal(p_year=datetime.today().year):
    return render_template('yearly_dtl_bal.html', title='YEARLY DETAIL BAL', v_list=YearlyDtlBal(p_year).summary_all())
