import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By

def login_tiktok(username: str, password: str):
    options = uc.ChromeOptions()
    options.headless = False
    driver = uc.Chrome(options=options)
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    time.sleep(5)
    email_input = driver.find_element(By.NAME, "email")
    password_input = driver.find_element(By.NAME, "password")
    email_input.send_keys(username)
    password_input.send_keys(password)
    login_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    login_button.click()
    time.sleep(10)
    return driver
