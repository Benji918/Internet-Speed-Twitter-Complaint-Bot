import time
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

PROMISED_UP = 150
PROMISED_DOWN = 10
TWITTER_EMAIL = os.environ['email']
TWITTER_PWD = os.environ['twitter_pwd']
twitter_url = 'https://twitter.com/i/flow/login'
chrome_driver_path = 'C:\Development\chromedriver_win32\chromedriver.exe'
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"  # Don't wait for page to fully load


class InternetSpeedTwitterBot:
    def __init__(self, chrome_path):
        service = Service(chrome_path)
        self.driver = webdriver.Chrome(desired_capabilities=caps, service=service)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get(url='https://www.speedtest.net/')
        time.sleep(10)
        # click on the go button
        go_btn = self.driver.find_element(By.CLASS_NAME, 'start-text')
        go_btn.click()
        time.sleep(60)
        # get the download and upload speeds
        self.down = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                                       '3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span').text
        self.up = self.driver.find_element(By.XPATH, '//*[@id="container"]/div/div[3]/div/div/div/div[2]/div[3]/div['
                                                     '3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span').text
        print(f'Download {self.down}: Upload {self.up}')

    def tweet_at_provider(self):
        self.driver.get(url=twitter_url)
        # tweet text
        tweet_text = f"Hello @MTNNG  right now my download speed is {self.down} and" \
                     f" my Upload speed id {self.up}" \
                     f" but I pay for Download Speed = {PROMISED_DOWN} and Upload Speed = {PROMISED_UP}"
        time.sleep(10)
        # Enter email
        email = self.driver.find_element(By.NAME, 'text')
        email.send_keys(TWITTER_EMAIL)
        email.send_keys(Keys.ENTER)
        time.sleep(5)
        # Enter password
        pwd = self.driver.find_element(By.NAME, 'password')
        pwd.send_keys(TWITTER_PWD)
        time.sleep(4)
        pwd.send_keys(Keys.ENTER)
        # Enter tweet
        time.sleep(10)
        tweet_msg = self.driver.find_element(By.CLASS_NAME, "public-DraftStyleDefault-block")
        tweet_msg.send_keys(tweet_text)
        time.sleep(4)
        # Send tweet
        send_tweet = self.driver.find_element(By.XPATH,
                                              '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[2]'
                                              '/div/div[2]/div[1]/div/div/div/div[2]/div[3]/div/div/div[2]/div[3]')
        send_tweet.click()
        self.driver.quit()


speed_bot = InternetSpeedTwitterBot(chrome_driver_path)
speed_bot.get_internet_speed()
speed_bot.tweet_at_provider()
