import subprocess
import sys
import os
import time

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import config
import funcs
def open(acc, task_id):
    os.chdir(config.user_workdir)
    keys = funcs.get_json("keys", True)
    if (acc not in keys.keys()):
        funcs.error(f"Cant find account {acc}")
    fullname, key = keys[acc]

    options = Options()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    service = Service(ChromeDriverManager().install())
    service.creationflags = subprocess.CREATE_NO_WINDOW
    try:
        driver = webdriver.Chrome(service=service, options=options)
    except selenium.common.exceptions.WebDriverException as e:
        funcs.error(str(e))
        sys.exit(0)
    print("browser started")
    driver.get('https://nearcrowd.com/v2')

    driver.execute_script(f'localStorage.setItem("near-api-js:keystore:{fullname}:mainnet","{key}");')
    driver.execute_script("localStorage.setItem('undefined_wallet_auth_key', '{\"accountId\":\"" + fullname + "\"}');")
    driver.refresh()
    driver.implicitly_wait(10)
    x = driver.find_elements(By.XPATH, '//button[contains(@onclick, "select")]')
    toclick = None
    print("[!]task_ids:")
    for el in x:
        numb =el.get_attribute('outerHTML').replace(')', '(').split('(')[1]
        print("[!]", numb, sep="")
        driver.execute_script(f"localStorage.setItem('v2tutorialseen{numb}', 'true');")
        if (numb == task_id):
            toclick = el
    if (toclick != None):
        toclick.click()
    print("[!]wait till browser not close")
    while 1:
        try:
            h = driver.window_handles
            time.sleep(0.5)
        except:
            break


