from selenium.webdriver import Chrome
import time
from urllib import request
import os


def main():
    url = "https://www.reddit.com/r/Hololewd/"
    imgDir = "Images"
    driver = Chrome()
    driver.get(url)
    driver.implicitly_wait(5)
    YesButton = driver.find_element_by_xpath(
        '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div/div/div[1]/div/div/div[2]/a[2]')
    YesButton.click()
    time.sleep(3)
    for x in range(200):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    Imgs = driver.find_elements_by_xpath('//*[@alt="Post image"]')
    link = []
    for s in Imgs:
        link.append(s.get_attribute('src'))
    driver.quit()
    if not os.path.exists(imgDir):
        os.makedirs(imgDir)
    for src in link:
        t = time.localtime()
        current_time = time.strftime("%H_%M_%S", t)
        request.urlretrieve(src, imgDir + "/IMG_" + current_time + ".jpg")
        print("Downloaded")

    print("Done")


main()
