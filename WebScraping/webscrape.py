from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
import time


def text():
    url = "https://www.jobstreet.com.ph/en/"
    driver = Chrome()
    driver.get(url)

    getInfo = driver.find_element_by_xpath('//*[@id="searchKeywordsField"]')
    getInfo.send_keys('Programmer' + Keys.RETURN)
    time.sleep(10)
    driver.quit()


text()
