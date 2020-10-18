from app.models import DictList, DictTrnsctnCtg, DictTrnsctnSctg, DictOperationTpMap, DictOperationCtg
from app import db
# from app.loader.utils import DictsUtils
from app.dictionaries.queries import InsertQueries


def create_dict_query(p_dict_nm, p_dict_tp):
    p_dict_tp = str(p_dict_tp)
    v_sql = "CREATE TABLE" + " "
    v_sql = v_sql + p_dict_nm + " "
    v_sql = v_sql + "as" + " "
    v_sql = v_sql + "SELECT * FROM" + " "
    if p_dict_tp == '1':    # slownik prosty
        v_sql = v_sql + "TMPLT_DICT_SMPL"
    elif p_dict_tp == '2':
        v_sql = v_sql + "TMPLT_DICT_CONVS"
    else:
        print("WRONG DICT_TP")
        quit()
    return v_sql


def dict_val_query(p_dict, p_dict_val_id):
    v_sql = "SELECT dict_val_val" + " "
    v_sql = v_sql + "FROM " + p_dict.dict_nm + " "
    v_sql = v_sql + "WHERE dict_val_id = " + p_dict_val_id
    v_sql = v_sql + "ORDER BY dict_val_val asc"

    return v_sql


def dict_vals_query(p_dict):
    v_sql = "SELECT" + " "
    v_sql = v_sql + "to_char(dict_val_crt_dt,'YYYY-MM-DD') as dict_val_crt_dt, dict_val_id as dict_val_id, dict_val_val as dict_val_val" + " "
    if p_dict.dict_tp == '2':   # słownik konwersji (DICT_TP=2)
        v_sql = v_sql + ", rltd_dict_nm_1" \
                        ", rltd_dict_val_1" \
                        ", rltd_dict_nm_2" \
                        ", rltd_dict_val_2" \
                        ", rltd_dict_nm_3" \
                        ", rltd_dict_val_3" + " "
    v_sql = v_sql + "FROM " + p_dict.dict_nm + " "
    v_sql = v_sql + "ORDER BY dict_val_id asc"

    return v_sql


def delete_dict_table_query(p_dict_nm):
    v_sql = "DROP TABLE " + p_dict_nm
    return v_sql


def delete_from_dict_list_query(p_dict_nm):
    v_sql = "DELETE FROM DICT_LIST WHERE 1=1 AND DICT_NM = '" + p_dict_nm + "'"
    return v_sql


def delete_from_dict_table_query(p_dict_nm, p_value):
    v_sql = "DELETE FROM " + p_dict_nm + " WHERE 1=1 and dict_val_id = '" + str(p_value) + "'"
    return v_sql


def get_dict_id(p_dict_nm):
    v_data = DictList.query.filter_by(dict_nm=p_dict_nm).first()
    return v_data.dict_id


def get_dict_list(p_dict_tp=None):
    v_list = DictList.query

    if p_dict_tp:
        v_list = v_list.filter(DictList.dict_tp == p_dict_tp)
    else:
        pass

    v_list = v_list.order_by(DictList.dict_id)
    v_list = v_list.all()

    return v_list


def set_dict_val_id(p_dict_nm):
    v_dict_val_id = db.session.execute(
        "Select nvl(max(dict_val_id),0) + 1 as new_id FROM " + p_dict_nm + "").first()  # Wyznaczenie nowego ID na podstawie maksymalnego ID
    v_dict_val_id = v_dict_val_id.new_id

    return v_dict_val_id


def get_dict_data(p_dict_id):
    v_list = DictList.query.get_or_404(p_dict_id)
    return v_list


def get_dict_values(p_dict_id, p_dict_val_id=None):
    v_dict = get_dict_data(p_dict_id)
    if p_dict_val_id:
        v_sql = dict_val_query(v_dict, p_dict_val_id)
        v_dict_vals = db.session.execute(v_sql).first()
    else:
        v_sql = dict_vals_query(v_dict)
        v_dict_vals = db.session.execute(v_sql)

    return v_dict_vals


def get_dict_cols_nm(p_dict_id):
    v_dict = get_dict_data(p_dict_id)
    v_dict_cols = db.session.execute(
        "Select column_name from ALL_TAB_COLS where 1=1 and table_name = upper('" + v_dict.dict_nm + "') order by column_name asc")

    return v_dict_cols


def add_to_dict_list(p_data):
    v_data = DictList(dict_id=p_data['dict_id'], dict_nm=p_data['dict_nm'], dict_desc=p_data['dict_desc'], dict_tp=p_data['dict_tp'])
    db.session.add(v_data)
    db.session.commit()


# CREATE DICT
# def create_dict_file(p_dict_nm, p_data):
#     v_dict_list_nm = "DICT_LIST"
#     DictsUtils(p_dict_nm).create_dict_file()  # create dict json file
#     DictsUtils(v_dict_list_nm).append_to_dict_file(v_dict_list_nm, p_data)  # add to DICT_LIST json file


def create_dict_table(p_dict_nm, p_dict_tp):
    v_sql = create_dict_query(p_dict_nm, p_dict_tp)
    db.session.execute(v_sql)
    db.session.commit()


# DELETE DICT
# def delete_dict_file(p_dict_nm):
#     DictsUtils(p_dict_nm).delete_dict_file() # delete dict json file


# def remove_from_dict_file(p_dict_nm, p_value):
#     DictsUtils(p_dict_nm).remove_from_dict_file(p_value)


def remove_from_dict_table(p_dict_nm, p_value):
    v_sql = delete_from_dict_table_query(p_dict_nm, p_value)
    db.session.execute(v_sql)
    db.session.commit()


def delete_dict_db(p_dict_nm):
    v_sql = delete_dict_table_query(p_dict_nm)
    db.session.execute(v_sql)
    db.session.commit()


def delete_from_dict_list(p_dict_nm):
    v_sql = delete_from_dict_list_query(p_dict_nm)
    db.session.execute(v_sql)
    db.session.commit()


# ADD TO DICT
# def add_to_dict_file(p_dict_nm, p_data):
#     DictsUtils(p_dict_nm).append_to_dict_file(p_dict_nm, p_data)    # add data to DICT file


def add_to_dict_table(p_dict_nm, p_data):
    v_sql = InsertQueries(p_dict_nm).insert_query_builder(p_data)
    db.session.execute(v_sql)
    db.session.commit()


class DictTrnsctnCtgUtils:
    def __init__(self):
        self.dict_nm = DictTrnsctnCtg.__tablename__.upper()
        self.dict_id = get_dict_id(self.dict_nm)

    def get_dict_values(self):
        v_sql_rslt = DictTrnsctnCtg.query
        v_sql_rslt = v_sql_rslt.all()

        return v_sql_rslt


class DictTrnsctnSctgUtils:
    def __init__(self):
        self.dict_nm = DictTrnsctnSctg.__tablename__.upper()
        self.dict_id = get_dict_id(self.dict_nm)

    def get_dict_values(self):
        v_sql_rslt = get_dict_values(self.dict_id)

        return v_sql_rslt

    def get_trnsctn_ctg_list(self, p_rltd_dict_val_1=None, p_rltd_dict_val_2=None):
        v_sql_rslt = DictTrnsctnSctg.query
        v_sql_rslt = v_sql_rslt.join(DictTrnsctnCtg, DictTrnsctnSctg.rltd_dict_val_1 == DictTrnsctnCtg.dict_val_id)
        v_sql_rslt = v_sql_rslt.with_entities(DictTrnsctnCtg.dict_val_id, DictTrnsctnCtg.dict_val_val)
        if p_rltd_dict_val_1:
            v_sql_rslt = v_sql_rslt.filter(DictTrnsctnSctg.rltd_dict_val_1 == p_rltd_dict_val_1)

        if p_rltd_dict_val_2:
            v_sql_rslt = v_sql_rslt.filter(DictTrnsctnSctg.rltd_dict_val_2 == p_rltd_dict_val_2)

        v_sql_rslt = v_sql_rslt.group_by(DictTrnsctnCtg.dict_val_id, DictTrnsctnCtg.dict_val_val)
        v_sql_rslt = v_sql_rslt.order_by(DictTrnsctnCtg.dict_val_val)
        v_sql_rslt = v_sql_rslt.all()

        return v_sql_rslt

    def get_trnsctn_sctg_list(self, p_ctg, p_oprtn_ctg):
        v_sql_rslt = DictTrnsctnSctg.query
        v_sql_rslt = v_sql_rslt.filter(DictTrnsctnSctg.rltd_dict_val_1 == p_ctg)
        v_sql_rslt = v_sql_rslt.filter(DictTrnsctnSctg.rltd_dict_val_2 == p_oprtn_ctg)
        v_sql_rslt = v_sql_rslt.order_by(DictTrnsctnSctg.dict_val_val)
        v_sql_rslt = v_sql_rslt.all()

        return v_sql_rslt


class DictOperationTpMapUtils:
    def __init__(self):
        self.dict_nm = DictOperationTpMap.__tablename__.upper()
        self.dict_id = get_dict_id(self.dict_nm)

    def get_oprtn_cd_oprnt_ctg_id(self, p_oprtn_cd):
        v_sql_rslt = DictOperationTpMap.query
        v_sql_rslt = v_sql_rslt.join(DictOperationCtg, DictOperationCtg.dict_val_id == DictOperationTpMap.rltd_dict_val_1)
        v_sql_rslt = v_sql_rslt.with_entities(DictOperationCtg.dict_val_id.label('oprtn_ctg_id'))
        v_sql_rslt = v_sql_rslt.filter(DictOperationTpMap.dict_val_id == p_oprtn_cd)
        v_sql_rslt = v_sql_rslt.first()

        return v_sql_rslt
