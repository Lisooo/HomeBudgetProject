from flask import Blueprint, render_template, jsonify, request, redirect, flash, url_for
from app.pty_oprtn_cd_clssfctn.utils import PtyOprtnClssfctnCdUtils
from app.pty_oprtn_cd_clssfctn.forms import PtyOprtnCdClssfctnForm
from app.pty.utils import Pty
from app.common.utils import redirect_url
from app.dictionaries.utils import DictTrnsctnSctgUtils, DictOperationTpMapUtils
from datetime import datetime

pocc = Blueprint('pocc', __name__)


@pocc.route("/pty_oprtn_cd_clssfctn", methods=['GET', 'POST'])
@pocc.route("/pty_oprtn_cd_clssfctn/yearly_<int:p_year>", methods=['GET', 'POST'])
@pocc.route("/pty_oprtn_cd_clssfctn/<int:p_year>_<int:p_month>", methods=['GET', 'POST'])
@pocc.route("/pty_oprtn_cd_clssfctn/notfilled_<int:p_notfilled>", methods=['GET', 'POST'])
def pty_oprtn_cd_clssfctn(p_year=None, p_month=None, p_notfilled=None):
    page = request.args.get('page', 1, type=int)
    v_pagination_list = PtyOprtnClssfctnCdUtils().get_pty_oprtn_cd_clssfctn_rows(p_year=p_year, p_month=p_month, p_notfilled=p_notfilled, page=page)

    if request.method == 'POST':
        a = request.form.get('pocc_select')

        if a == 'monthly':
            return redirect(url_for('pocc.pty_oprtn_cd_clssfctn', p_year=datetime.today().year, p_month=datetime.today().month))
        elif a == 'yearly':
            return redirect(url_for('pocc.pty_oprtn_cd_clssfctn', p_year=2020))
        elif a == 'all':
            return redirect(url_for('pocc.pty_oprtn_cd_clssfctn'))
        elif a == 'notfilled':
            return redirect(url_for('pocc.pty_oprtn_cd_clssfctn', p_notfilled=1))

    return render_template("pty_oprtn_cd_clssfctn.html", title="KATEGORYZACJA TRANSAKCJI",
                           v_val_list=v_pagination_list,
                           p_year=p_year,
                           p_month=p_month,
                           p_notfilled=p_notfilled)


@pocc.route("/pty_oprtn_cd_clssfctn_edit/<int:p_pty_id>_<int:p_oprtn_cd>", methods=['GET', 'POST'])
def pty_oprtn_cd_clsfctn_edit(p_pty_id, p_oprtn_cd):
    form = PtyOprtnCdClssfctnForm()

    v_oprtn_ctg = DictOperationTpMapUtils().get_oprtn_cd_oprnt_ctg_id(p_oprtn_cd)
    v_oprtn_ctg = v_oprtn_ctg.oprtn_ctg_id

    v_trnsctn_ctg_vals = DictTrnsctnSctgUtils().get_trnsctn_ctg_list(None, v_oprtn_ctg)
    form.trnsct_ctg.choices = [(Item.dict_val_id, Item.dict_val_val) for Item in v_trnsctn_ctg_vals]

    v_pty_data = Pty(p_pty_id).get_pty_data()

    v_data = {"pty_nm": v_pty_data.pty_nm,
              "pty_address": v_pty_data.pty_addrss,
              "pty_city": v_pty_data.pty_city,
              "pty_ctry": v_pty_data.pty_ctry,
              "pty_acn": v_pty_data.pty_acn,
              "oprtn_ctg": v_oprtn_ctg
              }

    if request.method == 'POST':
        v_trnsctn_ctg = form.trnsct_ctg.data
        v_trnsctn_sctg = form.trnsct_sctg.data

        PtyOprtnClssfctnCdUtils(p_pty_id, p_oprtn_cd).update_pty_oprtn_clssfctn_cd_table(v_trnsctn_ctg, v_trnsctn_sctg)
        flash("Poprawnie zaktualizowano wpis", 'success')
        return redirect(redirect_url())

    return render_template("pty_oprtn_cd_clssfctn_edit.html", title="KLASYFIKACJA", v_data=v_data, form=form)


@pocc.route("/pty_oprtn_cd_clssfctn_edit/get_trnsctn_sctg_list/<p_trnsctn_ctg_id>_<p_oprtn_ctg>")
def get_trnsctn_sctg_list(p_trnsctn_ctg_id, p_oprtn_ctg):
    dict_array = []

    dict_vals = DictTrnsctnSctgUtils().get_trnsctn_sctg_list(p_trnsctn_ctg_id, p_oprtn_ctg)

    for item in dict_vals:
        dictObj = {}
        dictObj['dict_val_id'] = item.dict_val_id
        dictObj['dict_val_val'] = item.dict_val_val
        dict_array.append(dictObj)

    return jsonify({'dict_values': dict_array})
