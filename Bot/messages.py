import time
from selenium.webdriver.common.by import By

def send_message(driver, username, message, log_callback=None):
    driver.get(f"https://www.tiktok.com/@{username}")
    time.sleep(5)
    try:
        msg_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Nachricht')]")
        msg_button.click()
        time.sleep(3)
        textarea = driver.find_element(By.TAG_NAME, "textarea")
        textarea.send_keys(message)
        send_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Senden')]")
        send_button.click()
        if log_callback:
            log_callback(f"Nachricht an {username} gesendet.")
    except Exception as e:
        if log_callback:
            log_callback(f"Fehler beim Senden der Nachricht: {e}")
