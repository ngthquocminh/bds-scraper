import os
import platform
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json 
import requests
import time

from LibFunc import get_proxies

HTTP_BIN = 'https://httpbin.org/ip'

class Browser(object):
    CHROME_DRIVER = """\chrome-driver\chromedriver.exe"""
    HOME_PATH = os.path.abspath(os.getcwd())
    def __init__(self, headless=True, window_size:tuple=(1920,1080), incognito=True):

        self.rotate_ip = True
        self.time_delay = 0
        self.headless = headless
        self.window_size = window_size
        self.incognito = incognito
        self.proxies = []
        self.chrome_options = self.create_chrome_option()
        self.init_browser_driver(self.chrome_options)

    def create_chrome_option(self):
        
        chrome_options = Options()
        if platform.system() == "Linux":
            print("Linux chrome")
            self.chrome_options.binary_location = """/usr/bin/chromium-browser"""
            CHROME_DRIVER = """/chrome-driver-linux/chromedriver"""

        prefs = {"profile.managed_default_content_settings.images": 2}

        if self.headless:
            self.chrome_options.add_argument("--headless")

        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("--window-size=%d,%d"%(self.window_size[0],self.window_size[1]))
        chrome_options.add_argument('--ignore-certificate-errors')
        if self.incognito:
            chrome_options.add_argument('--incognito')
        return chrome_options

    def init_browser_driver(self, chrome_options):
        self.browser = webdriver.Chrome(
            executable_path=self.HOME_PATH + self.CHROME_DRIVER,
            chrome_options=chrome_options)

    def set_time_delay(self, interval = 0):
        self.time_delay = int(interval)
        return

    def set_rotate_ip(self, enable=True):
        if enable:
            self.rotate_ip = True
            self.proxies = get_proxies()

        else:
            self.proxies = []
            self.rotate_ip = False

        return

    def get_html(self, url, time_out=10, until_ec=None, run_script=None, explicit_wait=-1):
        """
        Get HTML (page source) of a given url
        """
        if self.time_delay > 0:
            time.sleep(self.time_delay)
        
        if self.rotate_ip and len(self.proxies) > 0:
            for proxy in self.proxies:
                try:
                    requests.get(HTTP_BIN,proxies={"http": proxy, "https": proxy}).json()

                    self.current_proxy = proxy
                    break
                except:
                    ""
            self.chrome_options.add_argument('--proxy-server={}'.format(self.current_proxy))

        html = ""
        driver_error = True # default True allows code to enter the while loop

        retries_time = 5
        count_retry = 0
        while driver_error:
            try:
                self.browser.get(url)
                
                if explicit_wait > 0:
                    self.browser.implicitly_wait(10)
                elif until_ec:
                    WebDriverWait(self.browser, time_out).until(until_ec)

                try:
                    if run_script is not None:
                        self.browser.execute_script(run_script)
                except:
                    traceback.print_exc()

                html = self.browser.page_source
                driver_error = False

            except Exception as e: 
                traceback.print_exc()
                if count_retry >= retries_time:
                    break
                driver_error = True
                count_retry += 1
                if "not reachable" in repr(e) or "no such window" in repr(e) or "Timed out receiving message from renderer" in repr(e): 
                    self.init_browser_driver(self.chrome_options)
                else:
                    "others"
                    break


        return html

    def close(self):
        self.browser.quit()



