from RPA.Browser.Selenium import Selenium
import time


def Buda_ingreso():
    lib = Selenium()
    lib.open_available_browser('https://www.buda.com/ingreso')
    lib.input_text("id:user_email", 'eduardo.sinning@gmail.com')
    lib.input_text("id:user_password", 'yrg3t6j9D')
    lib.wait_and_click_button('xpath://button[@ng-show="!signinForm.$validating"]')
    time.sleep(120)
    return

Buda_ingreso()