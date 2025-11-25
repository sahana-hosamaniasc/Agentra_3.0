# apps/hp_app_web.py
from pages.desktop import *
from pages.desktop.login_page import LoginPage
from pages.desktop.createaccount_page import CreateAccountPage
from pages.desktop.launchapp_page import LaunchAppPage
from pywinauto.application import Application


class HPAppDesktop:
    def __init__(self, main_window):
        app = Application(backend="uia").connect(title="HP Smart")
        self.main_window =app.window(title_re="HP Smart")
        self.login_page = LoginPage(main_window)
        self.launchapp_page = LaunchAppPage(main_window)
        self.createaccount_page= CreateAccountPage(main_window)
        # self.enroll_page = WebEnrollPage(driver)

    def login(self, username, password):
        self.login_page.open()
        self.login_page.login()
    
    def start_enrollment(self):
        self.login_page.open()
        self.login_page.login()
    
    def enter_shipping_details(self):
        self.enroll_page.fill_shipping()
    
    def confirm_enrollment(self):
        self.enroll_page.confirm()
    
    def verify_confirmation_screen(self):
        self.enroll_page.verify_success_message()

    def launch_app(self):
        self.launchapp_page.launchapp()

    def create_account(self):
        self.createaccount_page.open_manage_account()
        self.createaccount_page.click_create_account()
        self.createaccount_page.wait_for_chrome_window()
        self.createaccount_page.create_account()
        self.createaccount_page.return_to_hp_smart()
