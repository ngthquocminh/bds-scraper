import os
import platform
import traceback

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

class Browser(object):
    CHROME_DRIVER = """\chrome-driver\chromedriver.exe"""
    HOME_PATH = os.path.abspath(os.getcwd())
    def __init__(self, headless=True, window_size:tuple=(1920,1080), incognito=True):
        self.chrome_options = Options()
        if platform.system() == "Linux":
            print("Linux chrome")
            self.chrome_options.binary_location = """/usr/bin/chromium-browser"""
            CHROME_DRIVER = """/chrome-driver-linux/chromedriver"""

        prefs = {"profile.managed_default_content_settings.images": 2}

        if headless:
            self.chrome_options.add_argument("--headless")

        self.chrome_options.add_experimental_option("prefs", prefs)
        self.chrome_options.add_argument("--window-size=%d,%d"%(window_size[0],window_size[1]))
        self.chrome_options.add_argument('--ignore-certificate-errors')
        if incognito:
            self.chrome_options.add_argument('--incognito')

        self.init_browser_driver()

    def init_browser_driver(self):
        self.browser = webdriver.Chrome(
            executable_path=self.HOME_PATH + self.CHROME_DRIVER,
            chrome_options=self.chrome_options)

    def get_html(self, url, time_out=10, until_ec=None, explicit_wait=-1):
        """
        Get HTML (page source) of a given url
        """
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
                
                html = self.browser.page_source
                driver_error = False

            except Exception as e: 
                traceback.print_exc()
                if count_retry >= retries_time:
                    break
                driver_error = True
                count_retry += 1
                if "not reachable" in repr(e) or "no such window" in repr(e) or "Timed out receiving message from renderer" in repr(e): 
                    self.init_browser_driver()
                else:
                    "others"
                    break

        return html