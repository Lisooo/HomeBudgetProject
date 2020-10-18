from _1_downloader.page.page import Page
from _1_downloader.deposit_page.locators import DepositPageLocators
from _1_downloader.loggers import Logger
from _1_downloader.csv_files.utils import FileUtils
from _1_downloader.common.utils import DateUtils
from params import FileParams

import time

log = Logger('DepositPage').logger()


class DepositPage(Page):

    def __init__(self, driver):
        super().__init__(driver)
        self.class_nm = __class__.__name__
        self.locators = DepositPageLocators
        self.file_format = FileParams.file_format

        log.info(f'Started with params:')
        log.info(f'Fileformat -> {self.file_format}')

    def get_date_from_input(self, v_fieldtype):
        v_name = f'#{self.get_date_from_input.__name__}#'
        try:
            v_input_date = ''
            if v_fieldtype == 1:
                v_input_date = self.get_attr_from_xpath("value", self.locators.dateTo_xpath)
            elif v_fieldtype == 2:
                v_input_date = self.get_attr_from_xpath("value", self.locators.dateFrom_xpath)
            return v_input_date

        except Exception as e:
            log.error(f"{self.class_nm} there's error in {v_name} method")
            log.error(f"{type(e)} // {e}")
            raise Exception(f"[{self.class_nm}] => {v_name} => {type(e)} => {e}")

    def click_input_field(self, v_fieldtype):
        v_name = f'#{self.click_input_field.__name__}#'.upper()

        if v_fieldtype == 1:
            self.click_element_xpath(self.locators.dateTo_xpath)
        elif v_fieldtype == 2:
            self.click_element_xpath(self.locators.dateFrom_xpath)
        else:
            log.error(f"{v_name} Something went wrong")
            quit()

    def set_date_into_input_field(self, v_day, v_month, v_year, v_fieldtype):
        v_input_date = self.get_date_from_input(v_fieldtype)

        v_month_name = DateUtils.get_month_name_from_dict(v_month)
        v_input_year = int(v_input_date[6:10])
        v_input_month = int(v_input_date[3:5])

        l_oday_xpath = self.locators.day_xpath(v_day)
        l_year_text_xpath = self.locators.year_text_xpath(v_year)
        l_date_text_xpath = self.locators.date_text_xpath(v_month_name, v_year)

        year_rslt = self.click_element_result(l_year_text_xpath)
        if int(v_year) == int(v_input_year):
            date_rslt = self.click_element_result(l_date_text_xpath)
            while date_rslt is False:
                if int(v_month) < int(v_input_month):
                    self.click_element_xpath(self.locators.prevMonth_xpath)
                    time.sleep(2)
                else:
                    self.click_element_xpath(self.locators.nextMonth_xpath)
                    time.sleep(2)

                date_rslt = self.click_element_result(l_date_text_xpath)
            else:
                self.click_element_xpath(l_oday_xpath)

        if int(v_year) > int(v_input_year):
            while year_rslt is False:
                self.click_element_xpath(self.locators.nextMonth_xpath)
                year_rslt = self.click_element_result(l_year_text_xpath)
            else:
                date_rslt = self.click_element_result(l_date_text_xpath)
                while date_rslt is False:
                    if int(v_month) < int(v_input_month):
                        self.click_element_xpath(self.locators.prevMonth_xpath)
                    else:
                        self.click_element_xpath(self.locators.nextMonth_xpath)
                    date_rslt = self.click_element_result(l_date_text_xpath)
                else:
                    self.click_element_xpath(l_oday_xpath)

        if int(v_year) < int(v_input_year):
            while year_rslt is False:
                self.click_element_xpath(self.locators.prevMonth_xpath)
                year_rslt = self.click_element_result(l_year_text_xpath)
            else:
                date_rslt = self.click_element_result(l_date_text_xpath)
                while date_rslt is False:
                    if int(v_month) < int(v_input_month):
                        self.click_element_xpath(self.locators.nextMonth_xpath)
                    else:
                        self.click_element_xpath(self.locators.prevMonth_xpath)
                    date_rslt = self.click_element_result(l_date_text_xpath)
                else:
                    self.click_element_xpath(l_oday_xpath)

    def set_date_input(self, v_date, v_fieldtype):
        v_name = f'#{self.set_date_input.__name__}#'.upper()

        if v_fieldtype in (1, 2):
            v_choice = str(v_fieldtype).replace('1', 'to').replace('2', 'from')
            v_day, v_month, v_year = DateUtils().get_variables_from_date(v_date)
            self.click_input_field(v_fieldtype)
            self.set_date_into_input_field(v_day, v_month, v_year, v_fieldtype)
            time.sleep(2)
            log.info(f"{v_name} sets date_{v_choice} {v_date} properly ")
        else:
            log.error(f"{v_name} Wrong v_fieldtype (only 1 or 2): {v_fieldtype}")
            quit()

    def download_file(self):
        rslt = self.click_element_result(self.locators.no_results_div_xpath)
        if rslt is False:
            self.click_element_xpath(self.locators.download_xpath)
            self.click_element_xpath(self.locators.file_format_xpath(self.file_format))
            time.sleep(2)
            log.info(f'File downloaded properly')
            return True, ' ', DateUtils.get_current_dttm()
        else:
            log.info(f'There was no transaction on that day')
            return False, 'There was no transaction on that day', None

    def get_deposit_transaction_history(self, v_str_date):
        # if already in deposit history then pass
        if self.click_element_result(self.locators.deposit_history_label_xpath):
            pass
        # else go to deposit history page
        else:
            self.enter_deposit_history_page()

        # set data range in calendar (always one day)
        self.set_date_input(v_str_date, 1)    # set dateTo
        self.set_date_input(v_str_date, 2)    # set dateFrom

        if self.click_element_result(self.locators.olderRecordsExists_text_xpath):
            log.warning(f'Tried to download records older than 90 days. Skipped.')
            pass
        else:
            pass
            # v_sts, v_msg, v_download_dttm = self.download_file()
            # if v_sts:
            #     v_new_file_nm = FileUtils().change_file_nm(v_str_date)  # changing FILE_NM
            #     v_import_flg = 'N'
            #     v_etl_flg = 'N'
            # else:
            #     v_new_file_nm = None
            #     v_import_flg = None
            #     v_etl_flg = None
            #
            # import_log_func.insert_into_import_log(v_new_file_nm, v_str_date, v_download_dttm, v_msg, v_import_flg, v_etl_flg)
