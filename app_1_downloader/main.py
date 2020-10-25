from app_1_downloader.login_page.page import LoginPage
from app_1_downloader.deposit_page.page import DepositPage
from  _tech_utils.timer.utils import Timer

# from transactions_downloader.cards.utils import CardsPage


@Timer
def main(driver, v_dates_range):

    loginPage = LoginPage(driver)
    loginPage.login()  # login

    depositPage = DepositPage(driver)

    # cardPage = CardsPage(driver)

    for v_str_date in v_dates_range:
        depositPage.get_deposit_transaction_history(v_str_date=v_str_date)  # get DEPOSIT TRANSACTION HISTORY

    depositPage.enter_cards_page()
    # cardPage.cards_list_into_csv()
