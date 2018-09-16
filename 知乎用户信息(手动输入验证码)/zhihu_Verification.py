#!/usr/bin/python3
#
#   解决验证码问题
#
from time import sleep
from selenium import webdriver

def login_page(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    win=webdriver.Chrome(chrome_options=options)
    win.get(url)
    sleep(10)
