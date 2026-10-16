import time
from selenium.webdriver.common.by import By

def follow_users(driver, blacklist: list, hashtag: str = "coding"):
    driver.get(f"https://www.tiktok.com/tag/{hashtag}")
    time.sleep(5)

    video_links = driver.find_elements(By.XPATH, "//a[contains(@href, '/video/')]")
    visited = set()

    for link in video_links[:10]:
        href = link.get_attribute("href")
        if href not in visited:
            visited.add(href)
            driver.get(href)
            time.sleep(3)

            try:
                username_elem = driver.find_element(By.XPATH, "//a[contains(@href, '/@')]")
                username = username_elem.get_attribute("href").split("/")[-1]
                print("Gefunden:", username)

                if username not in blacklist:
                    follow_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Folgen')]")
                    follow_btn.click()
                    print(f"Gefolgt: {username}")
                    time.sleep(2)
                else:
                    print(f"{username} steht auf der Blacklist")

            except Exception as e:
                print("Fehler beim Folgen:", e)
