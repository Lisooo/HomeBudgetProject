from app_1_downloader.page.locators import PageLocators
from  _tech_utils.logger.utils import Logger
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


log = Logger("Page").logger()


class Page(object):

    def __init__(self, driver):
        self.class_nm = __class__.__name__
        self.driver = driver
        self.locators = PageLocators
        self.ignored_exceptions = StaleElementReferenceException
        self.delay = WebDriverWait(driver, 30, ignored_exceptions=self.ignored_exceptions)

    def click_element_xpath(self, element_xpath):
        # Another element is covering the element you are to click. You could use execute_script() to click on this.
        self.delay.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
        try:
            element = self.driver.find_element(By.XPATH, element_xpath)
            self.driver.execute_script("arguments[0].click();", element)
        except StaleElementReferenceException:
            element = self.driver.find_element(By.XPATH, element_xpath)
            self.driver.execute_script("arguments[0].click();", element)

    def click_element_result(self, element_xpath):
        try:
            self.driver.find_element(By.XPATH, element_xpath)
            return True
        except:
            return False

    def clear_element_xpath(self, element_xpath):
        self.delay.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
        self.driver.find_element(By.XPATH, element_xpath).clear()

    def sendkeys_element_xpath(self, element_xpath, userpass):
        self.delay.until(EC.element_to_be_clickable((By.XPATH, element_xpath)))
        self.driver.find_element(By.XPATH, element_xpath).send_keys(userpass)

    def get_attr_from_xpath(self, attr, xpath):
        self.delay.until(EC.element_to_be_clickable((By.XPATH, xpath)))
        element = self.driver.find_element(By.XPATH, xpath)
        attr = element.get_attribute(attr)
        return attr

    def enter_deposit_history_page(self):
        v_name = f"#{self.enter_deposit_history_page.__name__}#".upper()
        try:
            self.click_element_xpath(self.locators.start_nav_xpath)
            self.click_element_xpath(self.locators.myProduct_nav_xpath)
            self.click_element_xpath(self.locators.accounts_subnav_xpath)
            self.click_element_xpath(self.locators.account_subnav_item_xpath('PKO Bank Polski', 'KONTO AURUM'))
            # self.click_element_xpath(self.locators.history_link_xpath)    # TIMEOUT EXCEPTION test
            log.info(f"{v_name} executed properly")
        except Exception as e:
            log.error(f"{self.class_nm} there's error in {v_name} method")
            log.error(f"{type(e)} // {e}")
            raise Exception(f"[{self.class_nm}] => {v_name} => {type(e)} => {e}")

    def enter_cards_page(self):
        v_name = f'#{self.enter_cards_page.__name__}#'.upper()
        try:
            self.click_element_xpath(self.locators.myProduct_nav_xpath)
            self.click_element_xpath(self.locators.cards_subnav_xpath)
            log.info(f"{v_name} executed properly")

        except Exception as e:
            log.error(f"{self.class_nm} there's error in {v_name} method")
            log.error(f"{type(e)} // {e}")
            raise Exception(f"[{self.class_nm}] => {v_name} => {type(e)} => {e}")
