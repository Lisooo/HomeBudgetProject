from _1_downloader.page.locators import PageLocators


class CardPageLocators(PageLocators):

    cardList_xpath = ".//div[contains(.,'Karta')]/a/parent::div"
    # cardItemsNumber = "count(.//div[contains(.,'Karta')]/a/parent::div)"
    # cardInfo_xpath = ".//div[contains(.,'Karta')]/a/span[text()]"
    cardDetails_xpath = ".//a[contains(.,'szczegóły i zarządzanie kartą')]"
