import datetime
from _tech_utils.logger.utils import Logger
from app_4_website.models import ProcessLog as m_ProcessLog

log = Logger('ProcessLog').logger()


class ProcessLog:

    def __init__(self, db):
        self.class_nm = __class__.__name__
        self.table_nm = 'process_log'
        self.db = db
        self.process_id = self.set_process_id()

        # SQL QUERIES
        # self.insert_query = f"INSERT INTO {self.table_nm} (process_id, process_nm, process_sts, import_dt_from, import_dt_to, process_start_dttm, process_end_dttm, description)" \
        #     f" VALUES (:process_id, :process_nm, :process_sts, :import_dt_from, :import_dt_to, :process_start_dttm, :process_end_dttm, :description)"

        # self.finish_update_query = f'UPDATE {self.table_nm} SET process_sts = :process_sts, process_end_dttm = :process_end_dttm, description = :description ' \
        #     f'WHERE process_id = :process_id'

        self.alter_duration_query = f"ALTER TABLE {self.table_nm} ADD (duration as (fnc_process_log_duration({self.table_nm}.process_start_dttm, {self.table_nm}.process_end_dttm)))"

    def set_process_id(self):
        new_id = self.db.session.query(self.db.func.max(m_ProcessLog.process_id)).scalar()
        if new_id is None:  # in case of first record
            new_id = 1
        else:
            new_id = int(new_id) + 1

        return new_id

    # def get_process_start_dttm(self):
    #     process_start_dttm = self.cursor.execute(f"SELECT process_start_dttm from {self.table_nm} WHERE process_id = {self.process_id}").fetchone()
    #     return process_start_dttm[0]

    def start(self, process_nm, import_dt_from, import_dt_to):
        v_name = f'#{self.start.__name__}#'
        try:
            process_start_dttm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            rec = m_ProcessLog(process_id=self.process_id, process_nm=process_nm, process_sts='RUNNING', import_dt_from=import_dt_from, import_dt_to=import_dt_to,
                               process_start_dttm=process_start_dttm, process_end_dttm=None, description='')
            self.db.session.add(rec)
            self.db.session.commit()
        except Exception as e:
            log.error(f"{self.class_nm} there's error in {v_name} method")
            log.error(f"{type(e)} // {e}")
            raise Exception(f"[{self.class_nm}] => {v_name} => {type(e)} => {e}")

    def finish(self, process_sts, description=None):
        v_name = f'#{self.finish.__name__}#'
        try:
            process_end_dttm = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            rec = m_ProcessLog.query.filter_by(process_id=self.process_id).first()
            rec.process_sts = process_sts
            rec.process_end_dttm = process_end_dttm
            rec.description = description
            self.db.session.commit()

        except Exception as e:
            log.error(f"{self.class_nm} there's error in {v_name} method")
            log.error(f"{type(e)} // {e}")
            raise Exception(f"[{self.class_nm}] => {v_name} => {type(e)} => {e}")

