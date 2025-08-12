from autoselenium import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import schedule
import time
import webbrowser

kongpanion_url = 'https://www.kongregate.com/achievements'

def badge(max_retries=3):
    print(f"Loading: {kongpanion_url}")
    attempts = 0

    while attempts < max_retries:
        try:
            with Firefox(headless=True) as driver:
                driver.get(kongpanion_url)

                # Wait for full page load
                WebDriverWait(driver, 10).until(
                    lambda d: d.execute_script('return document.readyState') == 'complete'
                )

                # Find the <k-challenge-badge> without 'hidden' in class
                badge_element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        '//k-challenge-badge[not(contains(@class, "hidden"))]'
                    ))
                )

                game_url = badge_element.get_attribute("href")

                if game_url:
                    print("✅ Found badge link:", game_url)
                    webbrowser.open(game_url, 2)
                else:
                    print("❌ Badge element found, but no href attribute present.")
                return  # Exit the function if successful

        except Exception as e:
            attempts += 1
            print(f"⚠️ Attempt {attempts} failed: {e}")
            if attempts >= max_retries:
                print("❌ All retry attempts failed.")

schedule.every().day.at("17:00").do(badge)

badge()
while True:
    schedule.run_pending()
    time.sleep(1)
