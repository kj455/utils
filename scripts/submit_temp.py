import os
from re import A
import sys
import time
from datetime import datetime
from datetime import time as tm

import chromedriver_binary
from selenium import webdriver

from google_photo import get_and_download_image
from line_notification import notify_line

BASE_FORM_URL = os.getenv('TEMPERATURE_FORM_URL')
NAME_ID = os.getenv('NAME_ID')
HAS_SYMPTOM_ID = os.getenv('HAS_SYMPTOM_ID')
BODY_TEMP_ID = os.getenv('BODY_TEMP_ID')

email = os.getenv('TEMP_FORM_EMAIL')
password = os.getenv('TEMP_FORM_PASSWORD')

name = os.getenv('PERSON_NAME')

xpaths = {
    'g_login_email': '//*[@id="identifierId"]',
    'g_login_submit': '//*[@id="identifierNext"]/div/button',
    'g_password_input': '//*[@id="password"]/div[1]/div/div[1]/input',
    'g_password_submit': '//*[@id="passwordNext"]/div/button',
    'add_file': '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[2]',
    'upload_file': '//*[@id="doclist"]/div/div[4]/div[2]/div/div[2]/div/div/div[1]/div/div[2]/div[2]/input',
    'upload_file_button': '//*[@id="picker:ap:0"]',
    'submit_form': '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div/div',
}


def delete_file(file_path):
    os.remove(file_path)


def click(driver, xpath):
    driver.find_element_by_xpath(xpath).click()


def insert_text(driver, xpath, str):
    driver.find_element_by_xpath(xpath).send_keys(str)


def is_morning() -> bool:
    return datetime.now().time() < tm(12, 0, 0)


def make_url():
    has_symptom = 'なし'
    body_temp = sys.argv[1]
    return f'{BASE_FORM_URL}?entry.{NAME_ID}={name}&entry.{HAS_SYMPTOM_ID}={has_symptom}&entry.{BODY_TEMP_ID}={body_temp}'
    # if is_morning():
    #   url += f'&entry.{ACTIVITY_HISTORY_ID}=朝'
    # else:
    #   url += f'&entry.{ACTIVITY_HISTORY_ID}={sys.argv[2]}'

def submit_form(file_path):
    driver = webdriver.Chrome()
    try:
        url = make_url()
        driver.implicitly_wait(1)
        driver.get(url)
        time.sleep(1)

        # * Googleアカウントでログインする
        # * u-tokyoアカウントメールアドレス入力
        insert_text(driver, xpaths['g_login_email'], email)
        click(driver, xpaths['g_login_submit'])
        time.sleep(3)

        # * u-tokyoアカウントパスワード入力
        insert_text(driver, xpaths['g_password_input'], password)
        click(driver, xpaths['g_password_submit'])
        time.sleep(5)

        # * 大体のデータは入力し終わっているので、画像のアップロードだけ行う
        # * 画像のアップロード
        click(driver, xpaths['add_file'])
        time.sleep(2)
        iframe = driver.find_element_by_class_name('picker-frame')
        driver.switch_to.frame(iframe)
        insert_text(driver, xpaths['upload_file'], file_path)
        time.sleep(3)
        click(driver, xpaths['upload_file_button'])
        time.sleep(7)
        driver.switch_to.default_content()

        # * 送信
        click(driver, xpaths['submit_form'])
        print(datetime.now())
        time.sleep(5)
    except Exception as e:
        print(e, 'フォーム送信失敗')
        notify_line('検温フォームの送信に失敗しました')
    finally:
        driver.close()
        driver.quit()
    return


def main():
    file_path = get_and_download_image()
    print('画像取得完了')
    submit_form(file_path)
    delete_file(file_path)
    print('提出完了')


if __name__ == "__main__":
    main()
