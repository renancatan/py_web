import time
from selenium import webdriver
import selenium
from selenium.webdriver.chrome import service
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

class scrape:

    def scrapedata(self):


        # ser = Service("C:\Program Files (x86)\chromedriver.exe")
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # driver = webdriver.Chrome(options=options, service=ser)
        chromedriver = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=chromedriver, options=options)
        driver.get('https://soundcloud.com/jujubucks')
        print(driver.title)

        wait = WebDriverWait(driver, 30)

        wait.until(EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))).click()

        song_list = []

        for i in range(1, 4):
            song_contents = driver.find_element(By.XPATH, "//li[@class='soundList__item'][{}]".format(i))
            driver.execute_script("arguments[0].scrollIntoView(true);", song_contents)
            try:
                search = song_contents.find_element(By.XPATH, ".//a[contains(@class,'soundTitle__username')]/span").text
                search_song = song_contents.find_element(By.XPATH,
                                                         ".//a[contains(@class,'soundTitle__title')]/span").text
                search_date = song_contents.find_element(By.XPATH, ".//time[contains(@class,'relativeTime')]/span").text
                search_plays = song_contents.find_element(By.XPATH,
                                                          ".//span[contains(@class,'sc-ministats-small')]/span").text
            except NoSuchElementException:
                continue
            if search_plays == False:
                continue

            option = {
                'Artist': search,
                'Song_title': search_song,
                'Date': search_date,
                'Streams': search_plays
            }
            song_list.append(option)

        df = pd.DataFrame(song_list)
        driver.quit()
        return song_list



# data = scrape()
# data.scrapedata()