from homebudget.models import DictList, DictDictTp, DictMonthNm, DictCurrencyCd, DictOperationTpMap, DictOperationCtg,\
    DictOperationTp, DictPtyTp


class DictNames(object):

    dict_currency_cd_tbl_nm = DictCurrencyCd.__tablename__.upper()
    dict_dict_tp_tbl_nm = DictDictTp.__tablename__.upper()
    dict_list_tbl_nm = DictList.__tablename__.upper()
    dict_month_nm_tbl_nm = DictMonthNm.__tablename__.upper()
    dict_operation_ctg_tbl_nm = DictOperationCtg.__tablename__.upper()
    dict_operation_tp_tbl_nm = DictOperationTp.__tablename__.upper()
    dict_operation_tp_map_tbl_nm = DictOperationTpMap.__tablename__.upper()
    dict_pty_tp_tbl_nm = DictPtyTp.__tablename__.upper()

