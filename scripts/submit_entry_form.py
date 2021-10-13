import os
import time

import chromedriver_binary
from dotenv import load_dotenv
from selenium import webdriver

from line_notification import notify_line
from submit_temp import click, insert_text

load_dotenv()

xpaths = {
    "email_input": '//*[@id="i0116"]',
    "email_submit": '//*[@id="idSIButton9"]',
    "password_input": '//*[@id="passwordInput"]',
    "password_submit": '//*[@id="submitButton"]',
    "no_button": '//*[@id="idBtn_Back"]',
    "vaccine_no": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/div[1]/div/label/input',
    "vaccine_submit": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[3]/div[1]/button',
    "email_destination": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[2]/div[1]/div/div[2]/div/div[1]/div/label',
    "campus": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[2]/div[2]/div/div[2]/div/div[1]/div/label',
    "main_location": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[2]/div[3]/div/div[2]/div/div/input',
    "temperature": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[2]/div[4]/div/div[2]/div/div[1]/div/label',
    "is_positive": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[2]/div[5]/div/div[2]/div/div[2]/div/label',
    "form_submit": '//*[@id="form-container"]/div/div/div[1]/div/div[1]/div[3]/div[3]/div[1]/button',
}

url = os.getenv("U_TOKYO_ENTRY_FORM")
email = os.getenv("U_TOKYO_EMAIL")
password = os.getenv("U_TOKYO_PASSWORD")
main_location = "工学部3号舘"

driver = webdriver.Chrome()
try:
    driver.implicitly_wait(1)
    driver.get(url)
    time.sleep(5)

    # * マイクロソフトサインイン
    insert_text(driver, xpaths["email_input"], email)
    click(driver, xpaths["email_submit"])
    time.sleep(3)

    # * 東大アカウントへのログイン
    insert_text(driver, xpaths["password_input"], password)
    click(driver, xpaths["password_submit"])
    time.sleep(3)

    # * 認証状態の維持についてのダイアログで「いいえ」
    click(driver, xpaths["no_button"])
    time.sleep(3)

    # # * ワクチン接種希望
    # click(driver, xpaths['vaccine_no'])
    # click(driver, xpaths['vaccine_submit'])
    # time.sleep(1)

    # * 入構フォーム
    click(driver, xpaths["email_destination"])
    click(driver, xpaths["campus"])
    insert_text(driver, xpaths["main_location"], main_location)
    click(driver, xpaths["temperature"])
    time.sleep(1)
    click(driver, xpaths["is_positive"])
    click(driver, xpaths["form_submit"])
    time.sleep(3)
    print("入構フォーム提出完了")
except Exception as e:
    print(e)
    print("フォーム送信失敗")
    notify_line("入構フォームの送信に失敗しました")
finally:
    driver.close()
    driver.quit()
