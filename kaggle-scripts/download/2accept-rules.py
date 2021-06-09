#!env python3
import sqlite3
import time
import pandas as pd
import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

"""
QUICKSTART:
0.You need to log in to kaggle.com with your Firefox browser.
1.Open about:profiles ; scroll down and locate your profile folder
2.Locate cookies.sqlite inside your firefox Profile dir
3.Insert the path to cookies.sqlite in the COOKIESFILE constant (in this file)
4.Run this script. A firefox instance should pop up in a few seconds and you should be able to visually see the contracts being accepted in the browser
5.You can watch the files `accepted`, `not-accepted-pre`, and `not-accepted-post` being populated in real time.

"""

COOKIESFILE = r"C:\Users\mecheto\AppData\Roaming\Mozilla\Firefox\Profiles\jnoufypq.default-release-1-1593455847800\cookies.sqlite"


def report(name, state):
    print(f"{name} {state}")
    with open(state, "a") as donefile:
        donefile.write(name + "\n")


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def accept_successful(browser):
    try:
        browser.find_element_by_class_name("competition-rules__accepted-text")
        return True
    except selenium.common.exceptions.NoSuchElementException:
        return False


def setup_browser():
    conn = sqlite3.connect(COOKIESFILE)
    conn.row_factory = dict_factory
    c = conn.cursor()
    c.execute("select name, value from moz_cookies where host='www.kaggle.com';")
    cookielist = c.fetchall()
    conn.close()

    browser = Firefox()
    browser.implicitly_wait(10)  # seconds
    browser.get("https://www.kaggle.com/404")
    for cookie in cookielist:
        browser.add_cookie(cookie)
    time.sleep(4)
    return browser


browser = setup_browser()

competitions_series = pd.read_csv("competitions.csv", index_col=False)["ref"]
competitions = list(competitions_series)
for c in competitions:
    url = f"https://www.kaggle.com/c/{c}/rules"
    browser.get(url)

    try:
        button = browser.find_element_by_class_name("dnFnGI")
    except selenium.common.exceptions.NoSuchElementException:
        report(c, "not-accepted-pre")
        continue

    time.sleep(1)
    button.click()

    if accept_successful(browser):
        report(c, "accepted")
    else:
        report(c, "not-accepted-post")


browser.close()
quit()
