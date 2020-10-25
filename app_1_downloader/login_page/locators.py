class LoginPageLocators(object):
    userpass_textbox_xpath = ".//*[contains(@name,'LOGIN')]"
    next_button_xpath = ".//button/span[text()='Dalej']"
    login_button_xpath = ".//button/span[text()='Zaloguj']"

    badusername_text_xpath = ".//p[text()='Wpisz poprawny numer klienta lub login']"
    badpassword_text_xpath = ".//p[text()='Wpisz poprawne hasło']"


    @staticmethod
    def p_text_locator_xpath(text):
        return f".//p[text()='{text}']"
