"""
Locator definitions for the <PAGE NAME> of the Desktop application.

This module provides all locators used by pywinauto to identify Windows UI
controls. Locators represent attributes exposed by the application’s
automation backend (UIA recommended).

Purpose:
    - Centralize desktop UI selectors for stable automation.
    - Avoid scattering control names or automation IDs across Page Objects.
    - Make locator updates simple when application versions change.

Locator Format:
    LOCATOR_NAME = ("attribute", "value")

Common pywinauto Attributes:
    - "name"        → Visible text of the control
    - "automation_id" → UIA Automation ID (preferred)
    - "class_name"  → Win32/Control class
    - "control_type" → UIA type (Button, Edit, Window)
    - "title"       → Window title
    
Example:
    LOGIN_WINDOW    = ("title", "HP Smart - Sign in")
    USERNAME_INPUT  = ("automation_id", "txtUser")
    SIGNIN_BUTTON   = ("name", "Sign In")

Usage:
    Page objects send these locators to pywinauto methods such as:
        window.child_window(**locator).click()
        window.child_window(**locator).type_keys()

Naming Convention:
    - CONSTANTS in UPPER_SNAKE_CASE
    - Use meaningful names describing the UI control
"""
from selenium.webdriver.common.by import By
class LoginPageLocators:
    """
    Desktop (pywinauto) locators for HP Smart / test login app window.
    Each locator is a dictionary that can be passed as **kwargs to driver.find_element(**locator)
    """
    USERNAME_INPUT = {"title": "Username", "control_type": "Edit"}
    PASSWORD_INPUT = {"title": "Password", "control_type": "Edit"}
    LOGIN_BUTTON = {"title": "Sign in", "control_type": "Button"}
    SUCCESS_MESSAGE = {"title": "Login Successful", "control_type": "Text"}
    ERROR_MESSAGE = {"title": "Invalid credentials", "control_type": "Text"}


class CreateAccountLocators:
    """
    Desktop (pywinauto) locators for HP Smart → Manage HP Account → Create Account flow.
    """
    MANAGE_HP_ACCOUNT_BTN = { "title": "Manage HP Account","control_type": "Button","found_index": 0}
    CREATE_ACCOUNT_BTN = {"title": "Create account","control_type": "Button"}
    CHROME_WINDOW = {"title_re": ".*Chrome.*","control_type": "Window"}
    HP_ACCOUNT_CHROME_WINDOW = {"title_re": ".*(HP Account|Create Account).*","control_type": "Window"}
    OTP_INPUT = {"title_re": ".*Enter verification code.*","control_type": "Edit"}
    SUBMIT_OTP_BTN = {"title": "Verify","control_type": "Button"}
    POPUP_OPEN_BTN = {"title_re": "Open","control_type": "Button"}
    POPUP_CONTINUE_BTN = {"title_re": "Continue","control_type": "Button"}
    EMAIL=(By.CSS_SELECTOR, "tr.ng-scope")
    BODY=(By.TAG_NAME, "body")
