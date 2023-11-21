from allure_commons._allure import step

from config.config import TestData
from pages.BasePage import BasePage
from selenium.webdriver.common.by import By
import time


class HomePage(BasePage):
    """ Locators """
    SEARCH_BAR = (By.ID, "twotabsearchtextbox")
    BUTTON_SEARCH = (By.ID, "nav-search-submit-button")
    FIRST_ELEMENT = (By.XPATH, '(//span[@class="a-size-base-plus a-color-base a-text-normal"])[1]')
    ASIN_WEB_ELEMENT = (By.XPATH, '//*[@id="productDetails_detailBullets_sections1"]/tbody/tr[1]/td')

    def __init__(self, driver):
        super().__init__(driver)
        self.driver.maximize_window()
        time.sleep(2)
        self.driver.delete_all_cookies()
        self.driver.get(TestData.BASE_URL)


    @step
    def do_search_keyword(self):
        self.send_keys(self.SEARCH_BAR, TestData.ASIN_CODE)
        self.do_click(self.BUTTON_SEARCH)
        flag = self.is_visible_by_locator(self.FIRST_ELEMENT)
        return flag

    @step
    def click_first_element_from_result(self):
        time.sleep(2)
        self.do_click(self.FIRST_ELEMENT)
        time.sleep(2)
