from _1_downloader.page.page import Page
from _1_downloader.cards_page.locators import CardPageLocators
from params import FileParams

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import csv
import datetime


class CardsPage(Page):

    def __init__(self, driver):
        super().__init__(driver)
        self.class_nm = __class__.__name__
        self.locators = CardPageLocators
        self.file_nm = f'cards_csv_{datetime.datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        self.file_path = f'{FileParams.files_dir}/{self.file_nm}'

    def get_info_from_cards_list(self):
        self.delay.until(EC.element_to_be_clickable((By.XPATH, CardPageLocators.cardList_xpath)))
        return self.driver.find_elements(By.XPATH, CardPageLocators.cardList_xpath)

    def cards_list_into_csv(self):
        cards_list = []
        for item in self.get_info_from_cards_list():
            item = item.text    # get text returned by xpath
            item = item.split('\n')
            cards_list.append(item)

        with open(self.file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Typ Karty", "Nazwa Karty", "Skrócony numer karty", "Właściciel karty"])
            writer.writerows(cards_list)

