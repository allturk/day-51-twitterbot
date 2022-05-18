import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions

PROMISED_DOWN = 100
PROMISED_UP = 8
CHROME_DRIVER_PATH = "C:/Development/chromedriver.exe"
T_MAIL = os.getenv("T_MAIL")
T_LOGIN = os.getenv("T_LOGIN")
T_USER = os.getenv("T_USER")


class InternetSpeedTwitterBot():
    def __init__(self):
        self.ping = None
        self.wait = None
        self.s = Service(executable_path=CHROME_DRIVER_PATH)
        self.driver = webdriver.Chrome(service=self.s)
        self.down_speed = 0
        self.upload_speed = 0

    def get_internet_speed(self):
        self.driver.maximize_window()

        self.driver.get("https://www.speedtest.net/")

        self.wait = WebDriverWait(self.driver, 15, 0.5, [exceptions.WebDriverException,
                                                         exceptions.NoSuchElementException])
        time.sleep(2)
        speed = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".start-button a")))
        time.sleep(3)
        speed.click()
        time.sleep(40)
        self.down_speed = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".download-speed"))).text
        print(f"Download speed: {self.down_speed}")
        self.upload_speed = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, ".upload-speed"))).text
        print(f"upload speed: {self.upload_speed}")
        self.ping = self.wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, ".result-data-value.ping-speed"))).text
        print(f"Ping: {self.ping}")

    def tweet_at_provider(self):
        self.driver.get("https://twitter.com/")

        login_twitter = self.wait.until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[5]/a')))
        login_twitter.click()
        time.sleep(2)
        user = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div input')))
        # //*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]
        user.send_keys(T_MAIL)
        time.sleep(2)
        next_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                        '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[6]')))
        next_button.click()
        time.sleep(2)
        try:
            user_control = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                             '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div[1]/div/div[1]/span/span')))

        except exceptions.NoSuchElementException:
            print("Normal giriş yapabilirsiniz")

        else:
            type_user = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div input')))
            type_user.send_keys(T_USER)
            time.sleep(1)
            user_controlButtton = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                                    '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div')))
            user_controlButtton.click()
        pas = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')))
        pas.send_keys(T_LOGIN)
        login = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                  '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div[1]/div/div')))
        login.click()
        time.sleep(2)
        compose_tweet = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '[href="/compose/tweet"')))
        compose_tweet.click()
        time.sleep(2)
        enter_text = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div[role="textbox"]')))

        enter_text.send_keys(
            f'''You promised: {PROMISED_DOWN}Mbps/{PROMISED_UP}Mbps but my actual speed {self.down_speed}Mbps/{self.upload_speed}Mbps, Ping: {self.ping}, https://github.com/allturk/day-51-twitterbot  #100daysofcode #100daysofpython day-51''')
        time.sleep(2)
        tweet_button = self.wait.until(EC.visibility_of_element_located((By.XPATH,
                                                                         '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/div/div[3]/div/div[1]/div/div/div/div/div[2]/div[3]/div/div/div[2]/div[4]')))
        tweet_button.click()

    def close_browser(self):
        self.driver.quit()
