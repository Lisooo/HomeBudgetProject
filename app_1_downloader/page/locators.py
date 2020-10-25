class PageLocators(object):
    # MAIN NAV
    start_nav_xpath = ".//button/span[text()='Start']"
    myProduct_nav_xpath = ".//button/span[text()='Moje produkty']"

    # SUB NAV
    cards_subnav_xpath = ".//div/a[text()='Karty']"
    accounts_subnav_xpath = ".//div/a[text()='Konta']"

    # SUB NAV ITEMS
    @staticmethod
    def account_subnav_item_xpath(v_bank_nm, v_account_nm):
        return f".//div[@style='position: relative;']/descendant::div[contains(.,'{v_bank_nm}')]/child::a[contains(.,'{v_account_nm}')]/parent::div"

    @staticmethod
    def card_subnav_item_xpath(v_card_tp, v_account_nm, v_card_shrt_nb):
        return f".//div[contains(.,'{v_card_tp}')]/a/child::span[1][contains(.,'{v_account_nm}')]/following-sibling::span[contains(.,'{v_card_shrt_nb}')]/parent::a"

    # OTHERS
    olderRecordsExists_text_xpath = ".//strong[text()='Znaleźliśmy operacje starsze niż 90 dni.']"

