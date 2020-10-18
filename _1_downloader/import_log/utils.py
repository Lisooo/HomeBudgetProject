from params import DateParams
from app.models import ImportLog as m_ImportLog
from _1_downloader.loggers import Logger
import datetime

logger = Logger('Import_Log').logger()


class ImportLogDatabase(object):

    def __init__(self, db):
        v_name = self.__init__.__name__
        try:
            self.table_nm = 'Import_log'
            self.db = db

            self.start_dt = DateParams.start_dt
            self.current_dt = DateParams.current_dt
            logger.info(f'Started with params:')
            logger.info(f'Start_dt -> {self.start_dt}, Current_dt -> {self.current_dt}')

        except Exception as e:
            logger.error(f"{__class__.__name__} there's error in {v_name} method")
            logger.error(f"{type(e)} // {e}")
            raise Exception(f"[{__class__.__name__}] => {v_name} => {type(e)} => {e}")

    @staticmethod
    def import_log_dates_into_list():
        # get already processed dates
        rslt = m_ImportLog.query.filter_by(etl_flg='N') \
            .with_entities(m_ImportLog.operation_dt) \
            .order_by(m_ImportLog.operation_dt) \
            .all()

        db_date_list = []
        for row in rslt:
            db_date_list.append(row[0])
        return db_date_list

    def insert_into_import_log(self, v_file_nm, v_oprtn_dt, v_download_dttm, v_download_msg, v_import_flg, v_etl_flg):
        # check if transaction date not in import csv log
        if str(v_oprtn_dt) in self.import_log_dates_into_list():
            print("Data transakcji: " + str(v_oprtn_dt) + " jest już w logu")
            pass
        else:
            new_id = self.db.session.query(self.db.func.max(m_ImportLog.file_id)).scalar()  # brak autoincrement dla ORACLE.

            if new_id == 0:  # in case of first record
                new_id = 1
            else:
                new_id = int(new_id[0]) + 1

            dict_values = {"new_id": new_id,
                           "file_nm": v_file_nm,
                           "oprtn_dt": v_oprtn_dt,
                           "download_dttm": v_download_dttm,
                           "download_msg": v_download_msg,
                           "import_flg": v_import_flg,
                           "etl_flg": v_etl_flg}

            rec = m_ImportLog([dict_values['new_id'], dict_values['file_nm'], dict_values['oprtn_dt']
                , dict_values["download_dttm"], dict_values["download_msg"], dict_values["import_flg"]
                , dict_values["etl_flg"]])

            self.db.session.add(rec)
            self.db.session.commit()
            logger.info(f'Record added properly')

    def generate_date_list_to_download(self):
        v_import_csv_dt = self.import_log_dates_into_list()  # list of dates in IMPORT CSV log
        v_final_dt_list = []

        while self.start_dt < self.current_dt:
            v_date = str(self.start_dt)

            if v_date in v_import_csv_dt:
                # print(v_date + ": exists in IMPORT CSV log")
                pass    # date exists in import_log == data downloaded from IPKO
            else:
                v_final_dt_list.append(v_date)
                logger.info(f"{v_date} added into download date list")

            self.start_dt = self.start_dt + datetime.timedelta(days=1)
        if len(v_final_dt_list) == 0:
            logger.info(f"Date list is empty")
            pass

        return v_final_dt_list
