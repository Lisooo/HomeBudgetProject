class InsertQueries:

    def __init__(self, p_dict_nm):
        self.dict_nm = p_dict_nm
        self.sql_query = "INSERT INTO #V_DICT_NM# VALUES (#V_DICT_VALUES#)"

    @staticmethod
    def prepare_value_list(p_data):
        i = 0
        for item in p_data:
            if type(p_data[item]) == str:
                p_data[item] = "'" + p_data[item] + "'"

            elif type(p_data[item]) == int:
                p_data[item] = str(p_data[item])

            if i == 0:
                v_values_list = p_data[item]
            else:
                v_values_list = v_values_list + ", " + p_data[item]

            i += 1
        return v_values_list

    def insert_query_builder(self, p_data):
        self.sql_query = self.sql_query.replace('#V_DICT_NM#', self.dict_nm)
        dict_values = self.prepare_value_list(p_data)
        self.sql_query = self.sql_query.replace('#V_DICT_VALUES#', dict_values)

        return self.sql_query


# class CreateQueries:
#
#     def __init(self, p_dict_nm):
#         self.dict_nm = p_dict_nm
#         self.dict_id = get_dict_id(self.dict_nm)
#         self.dict_data = get_dict_values(self.dict_id)
#         self.dict_tp = self.dict_data.dict_tp
#
#         self.smpl_dict_tmplt_nm = "TMPLT_DICT_SMPL"
#         self.convs_dict_tmplt_nm = "TMPLT_DICT_CONVS"
#         self.sql_query = "CREATE #V_DICT_NM# AS SELECT * FROM #TMPLT_NM#"