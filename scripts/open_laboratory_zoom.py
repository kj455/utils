import os
import time

import chromedriver_binary
import pyautogui
from dotenv import load_dotenv
from selenium import webdriver

load_dotenv()

ZOOM_URL = os.getenv("LABOLATORY_ZOOM_URL")
BUTTON_LOCATION_X = 800
BUTTON_LOCATION_Y = 300
BUTTON_KIND = "left"


def open_zoom():
    driver = webdriver.Chrome()
    try:
        driver.get(ZOOM_URL)
        time.sleep(3)
        pyautogui.click(x=BUTTON_LOCATION_X, y=BUTTON_LOCATION_Y)

    except Exception as e:
        print(e)
    finally:
        driver.quit()


def main():
    open_zoom()


if __name__ == "__main__":
    main()
