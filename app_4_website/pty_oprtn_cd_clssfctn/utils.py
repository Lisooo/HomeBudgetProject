from app_4_website import db
from app_4_website.models import PartyOperationCodeClassification, PartyOperation, Party, Operation, DictOperationTpMap, DictTrnsctnSctg, DictTrnsctnCtg, DictOperationCtg
from sqlalchemy import extract


class PtyOprtnClssfctnCdUtils:

    def __init__(self, p_pty_id=None, p_oprtn_cd=None):
        if p_pty_id:
            self.pty_id = p_pty_id

        if p_oprtn_cd:
            self.oprtn_cd = p_oprtn_cd

    def get_pty_oprtn_cd_record(self):
        v_sql_rslt = PartyOperationCodeClassification.query
        v_sql_rslt = v_sql_rslt.filter(PartyOperationCodeClassification.pty_id == self.pty_id)
        v_sql_rslt = v_sql_rslt.filter(PartyOperationCodeClassification.oprtn_cd == self.oprtn_cd)
        v_sql_rslt = v_sql_rslt.first()

        return v_sql_rslt

    def get_pty_oprtn_cd_clssfctn_rows(self, p_year=None, p_month=None, p_notfilled=None, page=1):
        v_sql_rslt = PartyOperationCodeClassification.query
        v_sql_rslt = v_sql_rslt.join(PartyOperation, PartyOperationCodeClassification.pty_id == PartyOperation.pty_id)
        v_sql_rslt = v_sql_rslt.join(Party, Party.pty_id == PartyOperation.pty_id)
        v_sql_rslt = v_sql_rslt.join(Operation,
                                     (PartyOperation.oprtn_id == Operation.oprtn_id) & (PartyOperationCodeClassification.oprtn_cd == Operation.oprtn_cd))
        v_sql_rslt = v_sql_rslt.join(DictOperationTpMap,
                                     PartyOperationCodeClassification.oprtn_cd == DictOperationTpMap.dict_val_id,
                                     isouter=True)
        v_sql_rslt = v_sql_rslt.join(DictOperationCtg,
                                     DictOperationTpMap.rltd_dict_val_1 == DictOperationCtg.dict_val_id,
                                     isouter=True)
        v_sql_rslt = v_sql_rslt.join(DictTrnsctnCtg,
                                     PartyOperationCodeClassification.trnsctn_ctg == DictTrnsctnCtg.dict_val_id,
                                     isouter=True)
        v_sql_rslt = v_sql_rslt.join(DictTrnsctnSctg,
                                     PartyOperationCodeClassification.trnsctn_sctg == DictTrnsctnSctg.dict_val_id,
                                     isouter=True)
        v_sql_rslt = v_sql_rslt.with_entities(Party.pty_id,
                                              Party.pty_nm,
                                              DictOperationTpMap.dict_val_val,
                                              PartyOperationCodeClassification.oprtn_cd,
                                              DictOperationCtg.dict_val_val.label('oprtn_ctg'),
                                              PartyOperationCodeClassification.trnsctn_ctg,
                                              DictTrnsctnCtg.dict_val_val.label('trnsctn_ctg_val'),
                                              PartyOperationCodeClassification.trnsctn_sctg,
                                              DictTrnsctnSctg.dict_val_val.label('trnsctn_sctg_val'))
        if p_year:
            v_sql_rslt = v_sql_rslt.filter(extract('year', Operation.trnsctn_dt) == p_year)
        if p_month:
            v_sql_rslt = v_sql_rslt.filter(extract('month', Operation.trnsctn_dt) == p_month)

        if p_notfilled:
            v_sql_rslt = v_sql_rslt.filter(PartyOperationCodeClassification.trnsctn_sctg == '-2' or PartyOperationCodeClassification.trnsctn_ctg == '-2')

        v_sql_rslt = v_sql_rslt.group_by(Party.pty_id,
                                         Party.pty_nm,
                                         DictOperationTpMap.dict_val_val,
                                         PartyOperationCodeClassification.oprtn_cd,
                                         DictOperationCtg.dict_val_val,
                                         PartyOperationCodeClassification.trnsctn_ctg,
                                         DictTrnsctnCtg.dict_val_val,
                                         PartyOperationCodeClassification.trnsctn_sctg,
                                         DictTrnsctnSctg.dict_val_val)

        v_sql_rslt = v_sql_rslt.order_by(Party.pty_nm,
                                         DictOperationTpMap.dict_val_val)

        v_sql_rslt = v_sql_rslt.paginate(per_page=28, page=page)

        return v_sql_rslt

    def update_pty_oprtn_clssfctn_cd_table(self, p_trnsctn_ctg, p_trnsctn_sctg):
        v_record = self.get_pty_oprtn_cd_record()
        v_record.trnsctn_ctg = p_trnsctn_ctg
        v_record.trnsctn_sctg = p_trnsctn_sctg
        db.session.commit()
