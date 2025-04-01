from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium_recaptcha_solver import RecaptchaSolver
from selenium.webdriver.common.action_chains import ActionChains
import pytest, sys, logging
from pytest_html_reporter import attach
import pytest_check as check
from selenium.webdriver.support.select import Select
from twocaptcha import TwoCaptcha
import datetime
import pyautogui
import test_web

def newtab():
    tabs = test_web.driver.window_handles
    test_web.driver.switch_to.window(tabs[1])
    time.sleep(2)

def closenewtab():
    driver.close()
    tabs = driver.window_handles
    driver.switch_to.window(tabs[0])
    time.sleep(2)


def scrollelement(element):
    element = driver.find_element(By.CLASS_NAME, element)
    actions = ActionChains(driver)
    actions.scroll_to_element(element)
    actions.perform()
    time.sleep(2)


def urlcheck(url):
    nowurl = driver.current_url
    check.equal(nowurl, url)