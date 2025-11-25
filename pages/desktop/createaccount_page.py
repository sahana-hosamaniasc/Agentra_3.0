from random import random
import string
import time
import allure
import pytest
from core.logger import get_logger
from selenium.webdriver.common.by import By
from resources.locators.desktop_locators import CreateAccountLocators
import time
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywinauto import Desktop
import re
import random
import string
from pywinauto import timings


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
            btn.wait("ready", timeout=15)
            btn.click_input()

    
    def click_create_account(self):
        self.logger.info("Clicking Create Account button")
        with allure.step("Click Create Account"):
            btn = self.main_window.child_window(**CreateAccountLocators.CREATE_ACCOUNT_BTN)
            btn.wait("ready", timeout=15)
            btn.click_input()

   
    def wait_for_chrome_window(self):
        self.logger.info("Waiting for HP Account Chrome window")

        with allure.step("Wait for Chrome Create Account Page"):
            end_time = time.time() + 120

            while time.time() < end_time:
                for win in Desktop(backend="uia").windows(title_re=".*Chrome.*"):
                    title = win.window_text().lower()
                    if "hp account" in title or "create account" in title:
                        win.set_focus()
                        win.maximize()
                        return win

                timings.wait_until_passes(3, 1, lambda: None)

            raise TimeoutError("HP Account Chrome window not found")

   
    def create_account(self):
        self.logger.info("Filling Create Account form")

        with allure.step("Fill Create Account Form"):

            suffix = ''.join(random.choices(string.digits, k=3))
            email = f"stagestack{suffix}@mailsac.com"
            password = f"Password@{suffix}"
            first_name = "Stage"
            last_name = "Stack"
            time.sleep(10)
             # ---------- Explicit wait: wait for first input box ----------
        timings.wait_until(
            timeout=20,
            retry_interval=1,
            func=lambda: pyautogui.locateOnScreen("first_name_field.png") is not None
        )

        # ---------- Type FIRST NAME ----------
        pyautogui.typewrite(first_name, interval=0.04)
        pyautogui.press("tab")
        

        # ---------- Wait for LAST NAME field ----------
        timings.wait_until(
            timeout=20,
            retry_interval=1,
            func=lambda: True  # Page already focused; tab ensures next input
        )

        # ---------- Type LAST NAME ----------
        time.sleep(10)
        pyautogui.typewrite(last_name, interval=0.04)
        pyautogui.press("tab")

        # ---------- Type EMAIL ----------
        time.sleep(10)
        pyautogui.typewrite(email, interval=0.04)
        pyautogui.press("tab")

        # ---------- Type PASSWORD ----------
        time.sleep(10)
        pyautogui.typewrite(password, interval=0.04)
        pyautogui.press("tab", presses=4)

        # ---------- Submit ----------
        pyautogui.press("enter")

    
    
        self.logger.info("Fetching OTP from Mailsac inbox")
        

        with allure.step("Fetch OTP"):
            
            driver = webdriver.Chrome()
            driver.get(f"https://mailsac.com/inbox/{email}")

            wait = WebDriverWait(driver, 20)
            otp = None
            end = time.time() + 120

            while time.time() < end:
                emails = driver.find_elements(*CreateAccountLocators.EMAIL)
                if emails:
                    emails[0].click()
                    break

                driver.refresh()
                timings.wait_until_passes(3, 1, lambda: None)

            body = driver.find_element(*CreateAccountLocators.BODY).text
            match = re.search(r"\b(\d{6})\b", body)

            driver.quit()

            if not match:
                raise Exception("OTP not found")

           

    
   

        with allure.step("Enter OTP"):
            pyautogui.hotkey("ctrl", "shift", "tab")
            timings.wait_until_passes(5, 1, lambda: None)

            pyautogui.typewrite(otp)
            pyautogui.press("tab")
            pyautogui.press("enter")

   
    def return_to_hp_smart(self):
        self.logger.info("Switching back to HP Smart Desktop App")

        with allure.step("Return to HP Smart App"):
            timings.wait_until_passes(10, 1, lambda: None)
            pyautogui.press("tab", presses=2)
            pyautogui.press("enter")

            timings.wait_until_passes(15, 1, lambda: None)
            self.main_window.set_focus()

   
    