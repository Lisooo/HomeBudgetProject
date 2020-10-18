from app.models import Operation, DictOperationTpMap, DictCurrencyCd, Party, PartyOperation, DictMonthNm, PartyOperationCodeClassification, DictTrnsctnSctg, DictTrnsctnCtg
from sqlalchemy import func, extract


class MonthlyBal:

    def __init__(self, p_year=None, p_month=None):
        self.year = p_year
        self.month = p_month

    def query(self, p_oprtn_ctg=None):

        v_year_lbl = 'year'
        v_month_lbl = 'month'
        v_val_sum_lbl = 'val_sum'

        v_sql = Operation.query
        v_sql = v_sql.with_entities(extract('year', Operation.trnsctn_dt).label(v_year_lbl),
                                              extract('month', Operation.trnsctn_dt).label(v_month_lbl),
                                              func.sum(Operation.trnsctn_val).label(v_val_sum_lbl))
        v_sql = v_sql.join(DictOperationTpMap, Operation.oprtn_cd == DictOperationTpMap.dict_val_id)
        v_sql = v_sql.join(DictMonthNm, extract('month', Operation.trnsctn_dt) == DictMonthNm.dict_val_id)

        if self.year:
            v_sql = v_sql.filter(extract('year', Operation.trnsctn_dt) == self.year)

        if self.month:
            v_sql = v_sql.filter(extract('month', Operation.trnsctn_dt) == self.month)

        if p_oprtn_ctg:
            v_sql = v_sql.filter(DictOperationTpMap.rltd_dict_val_1 == p_oprtn_ctg)

            v_sql = v_sql.group_by(extract('year', Operation.trnsctn_dt).label(v_year_lbl),
                                         extract('month', Operation.trnsctn_dt).label(v_month_lbl))

            v_sql = v_sql.order_by(extract('year', Operation.trnsctn_dt),
                                         extract('month', Operation.trnsctn_dt))

        return v_sql

    def query_result_all(self, p_oprtn_ctg=None):
        return self.query(p_oprtn_ctg).all()

    def summary_all(self):
        v_inc_list = self.query_result_all(1)  # incomes
        v_exp_list = self.query_result_all(2)  # expenses

        if v_inc_list:
            for v_inc_row in v_inc_list:
                v_inc_dict = {"year": v_inc_row.year,
                              "month": v_inc_row.month,
                              "inc_sum": v_inc_row.val_sum}
        else:   # if currently there are no incomes on this month
            v_inc_dict = {"year": self.year,
                          "month": self.month,
                          "inc_sum": 0}

        if v_exp_list:
            for v_exp_row in v_exp_list:
                v_exp_dict = {"year": v_exp_row.year,
                              "month": v_exp_row.month,
                              "exp_sum": v_exp_row.val_sum}

        else:   # if currently there are no expenses on this month
            v_exp_dict = {"year": self.year,
                          "month": self.month,
                          "exp_sum": 0}

        v_rslt = {"year": v_exp_dict["year"],
                  "month": v_exp_dict["month"],
                  "inc_bal": v_inc_dict["inc_sum"],
                  "exp_bal": v_exp_dict["exp_sum"],
                  "diff_bal": round(v_exp_dict["exp_sum"] + v_inc_dict["inc_sum"], 2)}

        return v_rslt


class MonthlyDtlBal:
    def __init__(self, p_year=None, p_month=None):
        self.year = p_year
        self.month = p_month

    def query(self):
        v_sql = Operation.query
        v_sql = v_sql.with_entities(Operation.trnsctn_dt.label('TRANSACTION_DT'),
                                              DictOperationTpMap.dict_val_val.label('OPERATION_TP'),
                                              Operation.trnsctn_val.label('TRANSACTION_VAL'),
                                              DictCurrencyCd.dict_val_val.label('CURRENCY_NM'),
                                              Operation.trnsctn_title.label('TRANSACTION_TITLE'),
                                              Operation.trnsctn_dtl_desc.label('TRANSACTION_DTL_DESC'),
                                              Party.pty_nm.label('PARTY_NM')
                                              )
        v_sql = v_sql.join(DictOperationTpMap, Operation.oprtn_cd == DictOperationTpMap.dict_val_id,
                                     isouter=True)  # left join
        v_sql = v_sql.join(DictCurrencyCd, Operation.currency_cd == DictCurrencyCd.dict_val_id,
                                     isouter=True)  # left join
        v_sql = v_sql.join(PartyOperation, Operation.oprtn_id == PartyOperation.oprtn_id,
                                     isouter=True)  # left join
        v_sql = v_sql.join(Party, PartyOperation.pty_id == Party.pty_id, isouter=True)  # left join
        if self.year:
            v_sql = v_sql.filter(extract('year', Operation.trnsctn_dt) == self.year)

        if self.month:
            v_sql = v_sql.filter(extract('month', Operation.trnsctn_dt) == self.month)

            v_sql = v_sql.order_by(Operation.trnsctn_dt, Party.pty_nm)

        return v_sql

    def query_result_paginated(self, page=1):
        return self.query().paginate(per_page=28, page=page)

    def summary_paginated(self, page):
        return self.query_result_paginated(page)


class MonthlyCtgBal:
    def __init__(self, p_year, p_month):
        self.year = p_year
        self.month = p_month

    def query(self, p_oprtn_ctg, p_detailed):
        v_label_nm_1 = 'GROUP_NM'
        v_label_nm_2 = 'TRNSCTN_SUM'
        v_coalesce_val = 'NIEOKRESLONO'

        v_sql = Operation.query
        v_sql = v_sql.join(PartyOperation, Operation.oprtn_id == PartyOperation.oprtn_id, isouter=True)
        v_sql = v_sql.join(PartyOperationCodeClassification,
                           (PartyOperation.pty_id == PartyOperationCodeClassification.pty_id) & (
                                       Operation.oprtn_cd == PartyOperationCodeClassification.oprtn_cd), isouter=True)
        v_sql = v_sql.join(DictTrnsctnSctg,
                           PartyOperationCodeClassification.trnsctn_sctg == DictTrnsctnSctg.dict_val_id, isouter=True)
        v_sql = v_sql.join(DictTrnsctnCtg, PartyOperationCodeClassification.trnsctn_ctg == DictTrnsctnCtg.dict_val_id,
                           isouter=True)
        v_sql = v_sql.filter(extract('year', Operation.trnsctn_dt) == self.year)
        v_sql = v_sql.filter(extract('month', Operation.trnsctn_dt) == self.month)
        v_sql = v_sql.filter(PartyOperationCodeClassification.oprtn_ctg == p_oprtn_ctg)
        if p_detailed == 'T':
            v_sql = v_sql.with_entities(
                func.coalesce(DictTrnsctnSctg.dict_val_val, v_coalesce_val).label(v_label_nm_1),
                func.sum(Operation.trnsctn_val).label(v_label_nm_2))
            v_sql = v_sql.group_by(DictTrnsctnSctg.dict_val_val)
        else:
            v_sql = v_sql.with_entities(
                func.coalesce(DictTrnsctnCtg.dict_val_val, v_coalesce_val).label(v_label_nm_1),
                func.sum(Operation.trnsctn_val).label(v_label_nm_2))
            v_sql = v_sql.group_by(DictTrnsctnCtg.dict_val_val)

        v_sql = v_sql.order_by(func.sum(Operation.trnsctn_val).asc())

        return v_sql

    def query_result_all(self,  p_oprtn_ctg, p_detailed='N'):
        return self.query(p_oprtn_ctg, p_detailed).all()


class YearlyBal:
    def __init__(self, p_year):
        self.year = p_year

    def query(self):

        v_rslt = Operation.query
        v_rslt = v_rslt.with_entities(extract('year', Operation.trnsctn_dt).label('year'),
                                      func.sum(Operation.trnsctn_val).label('val_sum'))

        v_rslt = v_rslt.filter(extract('year', Operation.trnsctn_dt) == self.year)
        v_rslt = v_rslt.group_by(extract('year', Operation.trnsctn_dt).label('year'))
        v_rslt = v_rslt.order_by(extract('year', Operation.trnsctn_dt).label('year'))

        return v_rslt

    def query_result_first(self):
        return self.query().first()

    def summary(self):
        v_year_bal = self.query_result_first()

        v_rslt = {"year": v_year_bal.year,
                  "diff_bal": round(v_year_bal.val_sum, 2)}

        return v_rslt


class YearlyDtlBal:
    def __init__(self, p_year):
        self.year = p_year

    def query(self):
        v_rslt = Operation.query
        v_rslt = v_rslt.with_entities(extract('month', Operation.trnsctn_dt).label('month'),
                                      func.sum(Operation.trnsctn_val).label('val_sum'))
        v_rslt = v_rslt.filter(extract('year', Operation.trnsctn_dt) == self.year)
        v_rslt = v_rslt.group_by(extract('month', Operation.trnsctn_dt).label('month'))
        v_rslt = v_rslt.order_by(extract('month', Operation.trnsctn_dt).label('month'))

        return v_rslt

    def query_result_all(self):
        return self.query().all()

    def summary_all(self):
        return self.query_result_all()
