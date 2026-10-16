import time
from selenium.webdriver.common.by import By

def get_stats(driver):
    try:
        driver.get("https://www.tiktok.com/@me")
        time.sleep(5)
        followers = driver.find_element(By.XPATH, "//strong[contains(text(),'Follower')]").text
        likes = driver.find_element(By.XPATH, "//strong[contains(text(),'Likes')]").text
        videos = driver.find_element(By.XPATH, "//strong[contains(text(),'Videos')]").text
        stats = f"Follower: {followers}\\nLikes: {likes}\\nVideos: {videos}"
        return stats
    except Exception as e:
        return f"Fehler beim Abrufen der Statistik: {e}"
