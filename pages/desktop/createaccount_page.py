import time
import allure
import pytest
import random
import string
import re
from datetime import datetime

import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywinauto import Desktop, timings

from core.logger import get_logger
from resources.locators.desktop_locators import CreateAccountLocators


class CreateAccountPage:

    def __init__(self, main_window):
        self.main_window = main_window
        self.logger = get_logger(self.__class__.__name__)

    def open_manage_account(self):
        self.logger.info("Opening Manage HP Account section")

        with allure.step("Open Manage HP Account"):
            self.main_window.set_focus()
            self.main_window.maximize()

            btn = self.main_window.child_window(**CreateAccountLocators.MANAGE_HP_ACCOUNT_BTN)
            btn.wait("ready", timeout=20)
            btn.click_input()

    
    def click_create_account(self):
        self.logger.info("Clicking Create Account button")

        with allure.step("Click Create Account"):
            btn = self.main_window.child_window(**CreateAccountLocators.CREATE_ACCOUNT_BTN)
            btn.wait("ready", timeout=20)
            btn.click_input()

    
    def wait_for_chrome_window(self):
        self.logger.info("Waiting for HP Account Chrome window")

        with allure.step("Wait for Chrome Create Account Page"):
            deadline = time.time() + 160

            while time.time() < deadline:
                for win in Desktop(backend="uia").windows(title_re=".*Chrome.*"):
                    title = win.window_text().lower()

                    if "hp account" in title or "create account" in title:
                        win.set_focus()
                        win.maximize()
                        self.logger.info("HP Account Chrome window detected")
                        return win

                time.sleep(2)

            raise TimeoutError("HP Account Chrome window not found!")

    
    def create_account(self):
        self.logger.info("Filling Create Account form")

        with allure.step("Fill Create Account Form"):

            # Generate dynamic email + password
            suffix = ''.join(random.choices(string.digits, k=4))
            email = f"stagestack{suffix}@mailsac.com"
            password = f"Password@{suffix}"
            first_name = "Stage"
            last_name = "Stack"

            time.sleep(10)  # allow full form load

            # FIRST NAME
            pyautogui.typewrite(first_name, interval=0.05)
            pyautogui.press("tab")

            # LAST NAME
            pyautogui.typewrite(last_name, interval=0.05)
            pyautogui.press("tab")

            # EMAIL
            pyautogui.typewrite(email, interval=0.05)
            pyautogui.press("tab")

            # PASSWORD
            pyautogui.typewrite(password, interval=0.05)
            pyautogui.press("tab", presses=4)

            # SUBMIT
            pyautogui.press("enter")
            self.logger.info(f"Submitted account form for {email}")

            time.sleep(10)

        
        self.logger.info("Fetching OTP from Mailsac inbox")

        with allure.step("Fetch OTP"):
            driver = webdriver.Chrome()
            driver.get(f"https://mailsac.com/inbox/{email}")

            wait = WebDriverWait(driver, 15)
            start_time=time.time()


            otp = None

            while time.time()-start_time < 120:

                
                rows = driver.find_elements(**CreateAccountLocators.EMAIL)
                if rows:
                    self.logger.info("Email list found → Clicking first email")
                    rows[0].click()
                    break

                driver.refresh()
                time.sleep(4)

            # Extract OTP
            body = wait.until(
                EC.visibility_of_element_located(**CreateAccountLocators.BODY)
            ).text

            match = re.search(r"\b(\d{6})\b", body)

            driver.quit()

            if not match:
                raise Exception("OTP not found in email content!")

            otp = match.group(1)
            self.logger.info(f"OTP Received: {otp}")

        
        with allure.step("Enter OTP"):

            time.sleep(2)
            pyautogui.hotkey("ctrl", "shift", "tab")  # switch back to HP Account tab
            time.sleep(3)

            pyautogui.typewrite(otp, interval=0.07)
            pyautogui.press('tab',presses=1,interval=0.3)
            pyautogui.press('enter')

            self.logger.info("OTP entered successfully")

    
    def return_to_hp_smart(self):
        self.logger.info("Switching back to HP Smart Desktop App")

        with allure.step("Return to HP Smart App"):
            time.sleep(30)

            pyautogui.press("tab", presses=2)
            time.sleep(1)
            pyautogui.press("enter")

            time.sleep(15)
            self.main_window.set_focus()

            self.logger.info("Successfully returned to HP Smart App")
