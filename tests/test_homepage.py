import pytest

from config.config import TestData
from pages.HomePage import HomePage
from tests.BaseTest import BaseTest


class TestHomepage(BaseTest):

    def test_search_asin_code(self):
        self.homepage = HomePage(self.driver)
        flag = self.homepage.do_search_keyword()
        self.homepage.click_first_element_from_result()
        assert flag

    def test_validate_asin_code_of_product(self):
        self.homepage = HomePage(self.driver)
        # get current window handle
        p = self.driver.current_window_handle
        chwd = self.driver.window_handles
        for w in chwd:
            # switch focus to child window
            if (w != p):
                self.driver.switch_to.window(w)
                break
        print("Child window title: " + self.driver.title)
        title = self.driver.title
        actual_title = self.homepage.get_title(title)
        actual_asin_code = self.homepage.get_element_text(self.homepage.ASIN_WEB_ELEMENT)
        assert actual_title == TestData.PRODUCT_TITLE
        assert actual_asin_code in TestData.ASIN_CODE



