from _1_downloader.page.locators import PageLocators


class DepositPageLocators(PageLocators):

    history_link_xpath = ".//span[text()='Historia']"
    deposit_history_label_xpath = ".//h2[text()='Operacje']"
    dateFrom_xpath = ".//input[contains(@name,'dateFrom')]"
    dateTo_xpath = ".//input[contains(@name,'dateTo')]"
    download_xpath = ".//div[text()='Pobierz']"
    no_results_div_xpath = ".//div[text()[contains(.,'Brak wyników')]]"
    nextMonth_xpath = ".//button/span[text()='Następny miesiąc']"
    prevMonth_xpath = ".//button/span[text()='Poprzedni miesiąc']"
    nextYear_xpath = ".//button/span[text()='Następny rok']"
    prevYear_xpath = ".//button/span[text()='Poprzedni rok']"

    @staticmethod
    def file_format_xpath(v_file_format):
        return f".//div/a[text()= {v_file_format} ]"

    @staticmethod
    def date_text_xpath(v_month, v_year):
        return f".//div[@class!='last_login' and @class!='copyright' and text()[contains(.,'{v_month} {v_year}')]]"

    @staticmethod
    def day_xpath(v_day):
        return f".//div/label/div[text()={v_day}]"

    @staticmethod
    def year_text_xpath(v_year):
        return f".//div[@class!='last_login' and @class!='copyright' and text()[contains(.,'{v_year}')]]"

    @staticmethod
    def month_name_xpath(v_month_nm):
        return f".//div[text()[contains(.,'{v_month_nm}')]]"
