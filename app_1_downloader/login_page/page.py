from params import LoginParams
from app_1_downloader.page.page import Page
from app_1_downloader.login_page.locators import LoginPageLocators
from  _tech_utils.logger.utils import Logger
import time

log = Logger('LoginPage').logger()


class LoginPage(Page):

    def __init__(self, driver):
        super().__init__(driver)
        self.class_nm = __class__.__name__
        self.locators = LoginPageLocators
        self.username = LoginParams.username
        self.password = LoginParams.password

        log.info(f'Started with params:')
        log.info(f'Username -> {self.username.replace(self.username, "*****")}, Password -> {self.password.replace(self.password, "*****")}')

    def enter_login_param(self, param):
        self.clear_element_xpath(self.locators.userpass_textbox_xpath)
        self.sendkeys_element_xpath(self.locators.userpass_textbox_xpath, param)

    def login(self):
        v_name = f"#{self.login.__name__}#".upper()
        try:
            self.enter_login_param(self.username)
            time.sleep(1)
            self.click_element_xpath(self.locators.next_button_xpath)
            time.sleep(1)
            if self.click_element_result(self.locators.badusername_text_xpath):
                raise ValueError(f"Provided username is wrong")

            self.enter_login_param(self.password)
            time.sleep(1)
            self.click_element_xpath(self.locators.login_button_xpath)
            time.sleep(1)
            if self.click_element_result(self.locators.badpassword_text_xpath):
                raise ValueError(f"Provided password is wrong")

            log.info(f'Logged successfully')

        except Exception as e:
            log.error(f"{self.class_nm} there's error in {v_name} method")
            log.error(f"{type(e)}: {e}")
            raise Exception(f"[{self.class_nm}] => {v_name} // {type(e)}: {e}")

