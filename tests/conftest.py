import pytest
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
import time

@pytest.fixture(params=["chrome"], scope='class')
def init_driver(request):
    if request.param == "chrome":
        web_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    if request.param == "firefox":
        web_driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    request.cls.driver = web_driver
    yield
    web_driver.close()
