from app_4_website.models import ImportLog
from sqlalchemy import func


def get_last_operation_dt():
    v_sql_result = ImportLog.query
    v_sql_result = v_sql_result.with_entities(func.max(ImportLog.operation_dt).label('operation_dt'))
    v_sql_result = v_sql_result.filter(ImportLog.etl_flg == 'T')
    v_sql_result = v_sql_result.first()

    return v_sql_result.operation_dt
