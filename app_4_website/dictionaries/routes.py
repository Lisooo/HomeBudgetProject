from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from app_4_website.dictionaries.utils import get_dict_list, get_dict_values, get_dict_cols_nm, add_to_dict_list, create_dict_table, get_dict_data, set_dict_val_id, add_to_dict_table, \
    delete_dict_db, delete_from_dict_list, remove_from_dict_table

from app_4_website.dictionaries.forms import DictForm, ConvsDictForm, SmplDictForm
from app_4_website.models import DictList
from app_4_website import db
from datetime import datetime

dicts = Blueprint('dicts', __name__)


@dicts.route("/dict_list")
def dict_list():
    v_list = get_dict_list()
    return render_template('dict_list.html', list=v_list, title="Lista Słowników")


@dicts.route("/dict_details/<int:p_dict_id>", methods=['GET'])
def dict_details(p_dict_id):
    v_val_list = get_dict_values(p_dict_id)
    v_dict_data = get_dict_data(p_dict_id)
    v_dict_tp = v_dict_data.dict_tp

    return render_template('dict_details.html', v_dict_id=p_dict_id, v_val_list=v_val_list, v_dict_tp=v_dict_tp, title="Szczegóły słownika")


# @dicts.route("/create_dict", methods=['GET', 'POST'])
# def create_dict():
#     form = DictForm()
#     v_dict_id = db.session.query(
#         db.func.max(DictList.dict_id)).scalar() + 1  # brak autoincrement dla ORACLE. TMP obejscie
#     v_dict_crt_dt = str(datetime.today().strftime('%Y-%m-%d'))
#
#     if form.validate_on_submit():
#         v_dict_nm = str(form.dict_nm.data.upper())
#         option = request.form.get('dict_tp')
#         option = str(option)
#         v_exists = DictList.query.filter_by(dict_nm=v_dict_nm).first()
#
#         if v_exists:
#             flash("Slownik: " + v_dict_nm + " już istnieje", 'warning')
#
#         else:
#             v_form_data = {"dict_id": v_dict_id,
#                       "dict_nm": form.dict_nm.data.upper(),
#                       "dict_desc": form.dict_desc.data,
#                       "dict_tp": option}
#
#             create_dict_file(v_dict_nm, v_form_data)     # CREATE dict file, ADD to DICT LIST file
#             add_to_dict_list(v_form_data)    # ADD to DICT_LIST table
#             create_dict_table(v_dict_nm, v_form_data['dict_tp'])
#
#             flash("Utworzono: " + v_dict_nm, 'success')
#
#         return redirect(url_for('dicts.dict_list'))
#
#     return render_template('create_dict.html', dict_id=v_dict_id, dict_crt_dt=v_dict_crt_dt, form=form,  title="Utwórz słownik")


# @dicts.route("/add_dict_value/<int:p_dict_id>", methods=['GET', 'POST'])
# def add_dict_value(p_dict_id):
#     v_dict = get_dict_data(p_dict_id)  # getting DICT data
#     v_dict_nm = v_dict.dict_nm  # setting DICT_NM
#     v_dict_tp = v_dict.dict_tp  # setting DICT_TP
#     v_dict_val_id = set_dict_val_id(v_dict_nm)  # setting DICT_VAL_ID
#     v_dict_val_crt_dt = str(datetime.today().strftime('%Y-%m-%d'))  # setting DICT_VAL_CRT_DT
#
#     v_data = {"dict_id": p_dict_id,
#               "dict_tp": v_dict_tp,
#               "dict_val_id": v_dict_val_id,
#               "dict_val_crt_dt": v_dict_val_crt_dt
#               }
#
#     if v_dict_tp == '1':
#         form = SmplDictForm()
#
#     elif v_dict_tp == '2':
#         form = ConvsDictForm()
#         v_dict_list = get_dict_list(1)  # SMPL dicts list
#
#         form.rltd_dict_nm_1.choices = [(DictItem.dict_id, DictItem.dict_nm) for DictItem in v_dict_list]
#         form.rltd_dict_nm_2.choices = [(DictItem.dict_id, DictItem.dict_nm) for DictItem in v_dict_list]
#         form.rltd_dict_nm_3.choices = [(DictItem.dict_id, DictItem.dict_nm) for DictItem in v_dict_list]
#
#     else:
#         flash("Błędny typ słownika: " + v_dict_tp, 'danger')
#         return redirect(url_for('dicts.dict_details', p_dict_id=p_dict_id))
#
#     if request.method == 'POST':
#         v_dict_val_val = form.dict_val_val.data
#
#         if v_dict_tp == '1':
#             v_file_data = {'dict_val_id': v_dict_val_id,
#                            'dict_val_val': v_dict_val_val
#             }
#
#             v_table_data = {'dict_val_id': v_dict_val_id,
#                             'dict_id': p_dict_id,
#                             'dict_val_val': v_dict_val_val,
#                             'dict_val_crt_dt': v_dict_val_crt_dt
#                             }
#
#         else:
#
#             v_rltd_dict_data_1 = get_dict_data(form.rltd_dict_nm_1.data)
#             v_rltd_dict_data_2 = get_dict_data(form.rltd_dict_nm_2.data)
#             v_rltd_dict_data_3 = get_dict_data(form.rltd_dict_nm_3.data)
#
#             v_rltd_dict_nm_1 = v_rltd_dict_data_1.dict_nm
#             v_rltd_dict_nm_2 = v_rltd_dict_data_2.dict_nm
#             v_rltd_dict_nm_3 = v_rltd_dict_data_3.dict_nm
#
#             if form.rltd_dict_nm_1.data == '-3':
#                 v_rltd_dict_val_1 = '-2'
#             else:
#                 v_rltd_dict_val_1 = form.rltd_dict_val_1.data
#
#             if form.rltd_dict_nm_2.data == '-3':
#                 v_rltd_dict_val_2 = '-2'
#             else:
#                 v_rltd_dict_val_2 = form.rltd_dict_val_2.data
#
#             if form.rltd_dict_nm_3.data == '-3':
#                 v_rltd_dict_val_3 = '-2'
#             else:
#                 v_rltd_dict_val_3 = form.rltd_dict_val_3.data
#
#             v_file_data = {'dict_val_id': v_dict_val_id,
#                            'dict_val_val': v_dict_val_val,
#                            'rltd_dict_nm_1': v_rltd_dict_nm_1,
#                            'rltd_dict_val_1': v_rltd_dict_val_1,
#                            'rltd_dict_nm_2': v_rltd_dict_nm_2,
#                            'rltd_dict_val_2': v_rltd_dict_val_2,
#                            'rltd_dict_nm_3': v_rltd_dict_nm_3,
#                            'rltd_dict_val_3': v_rltd_dict_val_3
#                            }
#
#             v_table_data = {'dict_val_id': v_dict_val_id,
#                             'dict_id': p_dict_id,
#                             'dict_val_val': v_dict_val_val,
#                             'rltd_dict_nm_1': v_rltd_dict_nm_1,
#                             'rltd_dict_val_1': v_rltd_dict_val_1,
#                             'rltd_dict_nm_2': v_rltd_dict_nm_2,
#                             'rltd_dict_val_2': v_rltd_dict_val_2,
#                             'rltd_dict_nm_3': v_rltd_dict_nm_3,
#                             'rltd_dict_val_3': v_rltd_dict_val_3,
#                             'dict_val_crt_dt': v_dict_val_crt_dt
#                             }
#
#         add_to_dict_file(v_dict_nm, v_file_data)
#         add_to_dict_table(v_dict_nm, v_table_data)
#         flash("Poprawnie dodano dane dla słownika: " + v_dict_nm, 'success')
#         return redirect(url_for('dicts.dict_details', p_dict_id=p_dict_id))
#
#     return render_template('add_dict_value.html', data=v_data, form=form, title=v_dict_nm + ": dodaj wpis")


# @dicts.route("/dict_list/<int:p_dict_id>/delete", methods=['GET', 'POST'])
# def delete_dict(p_dict_id):
#     v_dict_val = get_dict_data(p_dict_id)
#     v_dict_nm = v_dict_val.dict_nm
#     delete_dict_file(v_dict_nm)     # delete dict FILE
#     delete_dict_db(v_dict_nm)   # DROP TABLE
#     delete_from_dict_list(v_dict_nm)    # remove from dict_list TABLE
#     remove_from_dict_file("DICT_LIST", v_dict_nm)   # remove from dict_list FILE
#
#     flash("Poprawnie usunięto słownik", 'success')
#
#     return redirect(url_for('dicts.dict_list'))


# @dicts.route("/remove_value/<int:p_dict_id>/<int:p_dict_val_id>", methods=['GET','POST'])
# def remove_dict_value(p_dict_id, p_dict_val_id):
#     v_dict_val = get_dict_data(p_dict_id)
#     v_dict_nm = v_dict_val.dict_nm
#     remove_from_dict_file(v_dict_nm, p_dict_val_id)
#     remove_from_dict_table(v_dict_nm, p_dict_val_id)
#
#     flash("Poprawnie usunięto wartość słownikową: " + str(p_dict_val_id) + " ze słownika")
#     return redirect(url_for('dicts.dict_details', p_dict_id=p_dict_id))


@dicts.route("/add_dict_value/get_dict_values/<p_dict_id>")
def dict_values(p_dict_id):
    dict_array = []

    if p_dict_id == '-3':
        dictObj = {}
        dictObj['dict_val_id'] = '-2'
        dictObj['dict_val_val'] = ''
        dict_array.append(dictObj)

    else:
        dict_vals = get_dict_values(p_dict_id)

        for item in dict_vals:
            dictObj = {}
            dictObj['dict_val_id'] = item.dict_val_id
            dictObj['dict_val_val'] = item.dict_val_val
            dict_array.append(dictObj)

    return jsonify({'dict_values' : dict_array})
