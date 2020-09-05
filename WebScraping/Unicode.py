import time
from selenium.webdriver import Chrome


def main():
    url = "https://www.novelupdates.com/series/the-death-mage-who-doesnt-want-a-fourth-time/"
    driver = Chrome()
    driver.get(url)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.implicitly_wait(20)
    elemet = driver.find_element_by_class_name("my_popupreading_open")
    elemet.click()
    time.sleep(5)
    holdelements = driver.find_element_by_xpath(
        '//*[@id="my_popupreading"]/ol')
    listelem = holdelements.find_elements_by_xpath('//a[@data-id]')
    dictelem = {}
    for x in listelem:
        elemTitle = x.find_element_by_xpath('./span')
        dictelem[elemTitle.text] = f"{x.get_attribute('href')}"
        pass
    print(driver.title)
    print(dictelem)
    print('done')
    driver.find_element
    driver.quit()


if __name__ == '__main__':
    main()
