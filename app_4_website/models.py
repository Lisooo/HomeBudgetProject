from app_4_website import db
import datetime


class ProcessLog(db.Model):
    __tablename__ = "PROCESS_LOG"

    process_id = db.Column(db.Integer, primary_key=True)
    process_nm = db.Column(db.String(100), nullable=False)
    process_sts = db.Column(db.String(10), nullable=False)
    import_dt_from = db.Column(db.Date, nullable=False)
    import_dt_to = db.Column(db.Date, nullable=False)
    process_start_dttm = db.Column(db.DateTime(timezone=True), nullable=False)
    process_end_dttm = db.Column(db.DateTime(timezone=True), nullable=True)
    # duration = db.Column(db.DateTime(timezone=True), nullable=False)
    description = db.Column(db.String(500), nullable=True)


class FileLog(db.Model):
    __tablename__ = "FILE_LOG"

    file_id = db.Column(db.Integer, primary_key=True)
    file_nm = db.Column(db.String(40), nullable=True, unique=True)
    file_ext = db.Column(db.String(5), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    transactions_num = db.Column(db.Integer, nullable=False)
    operation_dt = db.Column(db.Date, nullable=False)
    download_dttm = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    process_id = db.Column(db.Integer, db.ForeignKey('PROCESS_LOG.process_id'), nullable=False)


class ImportLog(db.Model):
    __tablename__ = 'IMPORT_LOG'

    file_id = db.Column(db.Integer, primary_key=True)
    file_nm = db.Column(db.String(40), nullable=True, unique=True)
    operation_dt = db.Column(db.Date, nullable=False)
    download_dtm = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.datetime.utcnow)
    download_msg = db.Column(db.String(100), nullable=True)
    import_flg = db.Column(db.String(1), nullable=True, default=' ')
    etl_flg = db.Column(db.String(1), nullable=True, default=' ')

    def __repr__(self):
        return f"ImportLog('{self.file_nm}', '{self.operation_dt}', '{self.download_dtm}', '{self.download_msg}', '{self.import_flg}', '{self.etl_flg}')"


class OperationHistorySrc(db.Model):
    operation_id = db.Column(db.Integer, primary_key=True)
    operation_dt = db.Column(db.String(200), nullable=False)
    operation_tp = db.Column(db.String(200), nullable=False)
    currency_dt = db.Column(db.String(200), nullable=False)
    amount_val = db.Column(db.String(200), nullable=False)
    currency_nm = db.Column(db.String(200), nullable=False)
    account_bal = db.Column(db.String(200), nullable=False)
    operation_desc = db.Column(db.String(300), nullable=False)
    tmp_1 = db.Column(db.String(200), nullable=True)
    tmp_2 = db.Column(db.String(200), nullable=True)
    tmp_3 = db.Column(db.String(200), nullable=True)
    tmp_4 = db.Column(db.String(200), nullable=True)
    tmp_5 = db.Column(db.String(200), nullable=True)
    tmp_6 = db.Column(db.String(200), nullable=True)


# DICT_LIST
class DictList(db.Model):
    __tablename__ = 'dict_list'

    dict_id = db.Column(db.Integer, primary_key=True)
    dict_nm = db.Column(db.String(100), nullable=True, unique=True)
    dict_desc = db.Column(db.String(500), nullable=True)
    dict_tp = db.Column(db.String(10), nullable=True)
    dict_crt_dt = db.Column(db.Date, nullable=True, default=datetime.date.today().strftime('%Y-%m-%d'))


# TEMPLATES


class TmpltDictSmpl(db.Model):
    __tablename__ = 'tmplt_dict_smpl'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.datetime.today().strftime('%Y-%m-%d'))


class TmpltDictConvs(db.Model):
    __tablename__ = 'tmplt_dict_convs'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    rltd_dict_nm_1 = db.Column(db.String(200), nullable=False)
    rltd_dict_val_1 = db.Column(db.Integer, nullable=True, default='-2')
    rltd_dict_nm_2 = db.Column(db.String(200), nullable=True)
    rltd_dict_val_2 = db.Column(db.Integer, nullable=True, default='-2')
    rltd_dict_nm_3 = db.Column(db.String(200), nullable=True)
    rltd_dict_val_3 = db.Column(db.Integer, nullable=True, default='-2')
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.datetime.today().strftime('%Y-%m-%d'))

# SLOWNIKI


class DictOperationCtg(db.Model):
    __tablename__ = 'dict_operation_ctg'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.datetime.today().strftime('%Y-%m-%d'))


class DictCurrencyCd(db.Model):
    __tablename__ = 'dict_currency_cd'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.date.today().strftime('%Y-%m-%d'))


class DictTrnsctnCtg(db.Model):
    __tablename__ = 'dict_trnsctn_ctg'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.date.today().strftime('%Y-%m-%d'))


class DictTrnsctnSctg(db.Model):
    __tablename__ = 'dict_trnsctn_sctg'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False)
    rltd_dict_nm_1 = db.Column(db.String(200), nullable=False)
    rltd_dict_val_1 = db.Column(db.Integer, nullable=True, default='-2')
    rltd_dict_nm_2 = db.Column(db.String(200), nullable=True)
    rltd_dict_val_2 = db.Column(db.Integer, nullable=True, default='-2')
    rltd_dict_nm_3 = db.Column(db.String(200), nullable=True)
    rltd_dict_val_3 = db.Column(db.Integer, nullable=True, default='-2')
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.datetime.today().strftime('%Y-%m-%d'))


class DictPtyTp(db.Model):
    __tablename__ = 'dict_pty_tp'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.date.today().strftime('%Y-%m-%d'))


class DictDictTp(db.Model):
    __tablename__ = 'dict_dict_tp'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.date.today().strftime('%Y-%m-%d'))


class DictMonthNm(db.Model):
    __tablename__ = 'dict_month_nm'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.date.today().strftime('%Y-%m-%d'))


class DictOperationTp(db.Model):
    __tablename__ = 'dict_operation_tp'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.date.today().strftime('%Y-%m-%d'))


# CONVERSION DICTS
class DictOperationTpMap(db.Model):
    __tablename__ = 'dict_operation_tp_map'

    dict_val_id = db.Column(db.Integer, primary_key=True)
    dict_id = db.Column(db.Integer, db.ForeignKey('dict_list.dict_id'), nullable=False)
    dict_val_val = db.Column(db.String(200), nullable=False, unique=True)
    rltd_dict_nm_1 = db.Column(db.String(200), nullable=False)
    rltd_dict_val_1 = db.Column(db.Integer, nullable=True, default='-2')
    rltd_dict_nm_2 = db.Column(db.String(200), nullable=True)
    rltd_dict_val_2 = db.Column(db.Integer, nullable=True, default='-2')
    rltd_dict_nm_3 = db.Column(db.String(200), nullable=True)
    rltd_dict_val_3 = db.Column(db.Integer, nullable=True, default='-2')
    dict_val_crt_dt = db.Column(db.Date, nullable=False, default=datetime.datetime.today().strftime('%Y-%m-%d'))


class Operation(db.Model):
    __tablename__ = 'OPRTN'

    oprtn_id = db.Column(db.Integer, primary_key=True)
    oprtn_dt = db.Column(db.Date, nullable=False)
    oprtn_dttm = db.Column(db.DateTime(timezone=True), nullable=True, default=datetime.datetime.utcnow)
    oprtn_cd = db.Column(db.Integer, db.ForeignKey('dict_operation_tp_map.dict_val_id'), nullable=False)
    trnsctn_dt = db.Column(db.Date, nullable=False)
    trnsctn_val = db.Column(db.Float, nullable=False)
    currency_cd = db.Column(db.Integer, db.ForeignKey('dict_currency_cd.dict_val_id'), nullable=False)
    trnsctn_title = db.Column(db.String(200), nullable=True)
    trnsctn_dtl_desc = db.Column(db.String(100), nullable=True)


class Party(db.Model):
    __tablename__ = 'PTY'

    pty_id = db.Column(db.Integer, primary_key=True)
    pty_nm = db.Column(db.String(100), nullable=False)
    pty_addrss = db.Column(db.String(100), nullable=True)
    pty_city = db.Column(db.String(100), nullable=True)
    pty_ctry = db.Column(db.String(30), nullable=True)
    pty_acn = db.Column(db.String(26), nullable=True)


class PartyOperation(db.Model):
    __tablename__ = 'PTY_OPRTN'

    pty_id = db.Column(db.Integer, primary_key=True)
    oprtn_id = db.Column(db.Integer, primary_key=True)
    oprtn_dt = db.Column(db.Date, nullable=False)


class PartyOperationCodeClassification(db.Model):
    __tablename__ = 'PTY_OPRTN_CD_CLSSFCTN'

    pty_id = db.Column(db.Integer, primary_key=True)
    oprtn_cd = db.Column(db.Integer, primary_key=True)
    oprtn_ctg = db.Column(db.Integer, db.ForeignKey('dict_operation_ctg.dict_val_id'), nullable=False)
    trnsctn_ctg = db.Column(db.Integer, nullable=False, default='-2')
    trnsctn_sctg = db.Column(db.Integer, nullable=False, default='-2')
