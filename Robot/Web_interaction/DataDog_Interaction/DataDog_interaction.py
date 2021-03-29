from RPA.Browser.Selenium import Selenium
import time

browser = Selenium()
url = "https://app.datadoghq.com/account/login?next=%2F"

user = 'aguerra@vainatec.com'
clave = 'Ma..37861'
path = 'C:/Users/56979/PycharmProjects/Unitti/Robot/Web_interaction/DataDog_Interaction'
screenshot_filename_0 = path + '/' + "output/screenshot_login.png"
screenshot_filename_1 = path + '/' + "output/screenshot_ingreso.png"
screenshot_filename_2 = path + '/' + "output/screenshot_events.png"
screenshot_filename_3 = path + '/' + "output/screenshot_watchdog.png"
screenshot_filename_4 = path + '/' + "output/screenshot_rellenar_formulario.png"


def open_the_website(url):
    browser.open_available_browser(url)
    browser.driver.maximize_window()


def search_for(user, clave):
    input_field_username = "id:username"
    input_field_clave = "id:password"
    browser.input_text(input_field_username, user)
    browser.input_text(input_field_clave, clave)
    store_screenshot(screenshot_filename_0)
    browser.press_keys(input_field_clave, "ENTER")


def click_menu(screenshot_filename,tool_menu):
    boton_field = 'css:li.single-page-app_navbar_navbar-menu__list-item'
    boton = browser.find_elements(locator=boton_field)
    menu={'watchdog':['https://app.datadoghq.com/watchdog'],
          'events':['https://app.datadoghq.com/event/stream'],
          'dashboards_list':['https://app.datadoghq.com/dashboard/lists','https://docs.datadoghq.com/graphing/dashboards/'],
          'infrastructure':['https://app.datadoghq.com/infrastructure','https://app.datadoghq.com/infrastructure/map','https://app.datadoghq.com/infrastructure','https://app.datadoghq.com/containers','https://app.datadoghq.com/process','https://app.datadoghq.com/functions','https://app.datadoghq.com/network','https://app.datadoghq.com/network/map','https://docs.datadoghq.com/graphing/infrastructure/'],
          'monitors':['https://app.datadoghq.com/monitors/manage','https://app.datadoghq.com/monitors/triggered','https://app.datadoghq.com/monitors#/create','https://app.datadoghq.com/monitors#/downtime','https://app.datadoghq.com/incidents','https://app.datadoghq.com/incidents/new','https://app.datadoghq.com/incidents/introduction','https://app.datadoghq.com/slo','https://app.datadoghq.com/slo/new','https://app.datadoghq.com/check/summary'],
          'metrics':['https://app.datadoghq.com/metric/explorer','https://app.datadoghq.com/metric/summary','https://docs.datadoghq.com/graphing/metrics/'],
          'apm':['https://app.datadoghq.com/apm/home','https://app.datadoghq.com/apm/services','https://app.datadoghq.com/apm/map','https://app.datadoghq.com/apm/traces','https://app.datadoghq.com/apm/analytics','https://app.datadoghq.com/profiling','https://app.datadoghq.com/apm/getting-started'],
          'notebooks':['https://app.datadoghq.com/notebook/list','https://docs.datadoghq.com/notebooks/'],
          'logs':['https://app.datadoghq.com/logs','https://app.datadoghq.com/logs/analytics','https://app.datadoghq.com/logs/patterns','https://app.datadoghq.com/logs/livetail','https://app.datadoghq.com/logs/pipelines/historical-views','https://app.datadoghq.com/logs/pipelines/generate-metrics','https://app.datadoghq.com/logs/pipelines','https://app.datadoghq.com/logs/onboarding','https://docs.datadoghq.com/logs/'],
          'security':['https://app.datadoghq.com/security','https://app.datadoghq.com/security/compliance-getting-started','https://app.datadoghq.com/security/runtime-getting-started','https://app.datadoghq.com/security/analytics','https://app.datadoghq.com/security/configuration/rules','https://app.datadoghq.com/security/getting-started','https://docs.datadoghq.com/security_monitoring/']}
    for b in boton:
        #print(b)
        a_list = b.find_elements_by_tag_name(name='a')
        #print(len(a_list))
        for a in a_list:
            #print(a)
            href=a.get_property(name='href')
            #print(href)
            if href == menu[tool_menu][0]:
                 b.click()
                 time.sleep(10)
                 store_screenshot(screenshot_filename)
                 return


def search_event(event_info):
    input_field = "id:query"
    browser.input_text(input_field, event_info)
    time.sleep(10)
    browser.press_keys(input_field, "ENTER")


def search_timestamp(timestamp):
    #input_field = "class:ui_form_input-text__input.ui_form_validation__element"
    input_field='class:druids_misc_option-default'
    timestamp_scroll(input_field=input_field,value_dicc=timestamp)
    #browser.input_text(input_field,timestamp)
    time.sleep(10)
    #browser.press_keys(input_field, "ENTER")




def timestamp_scroll(input_field, value_dicc):
    for option in browser.driver.find_elements_by_tag_name('option'):
        if option.text == value_dicc:
            option.click()  # select() in earlier versions of webdriver
            break
    #val = browser.driver.find_element_by_css_selector(input_field)
    val_time_list=browser.driver.find_elements_by_class_name(name=input_field)
    for i in val_time_list:
        print(i)
        print(i.id)
        print(i.tag_name)
        print(i.screenshot_as_png)
        i

def agregar_documento(filename):
    # to identify element
    s = browser.driver.find_element_by_xpath("//input[@type='file']")
    # file path specified with send_keys
    s.send_keys(filename)


def store_screenshot(filename):
    browser.screenshot(filename=filename)


# Define a main() function that calls the other functions in order:
def main():
    try:
        open_the_website(url)
        store_screenshot(screenshot_filename_0)
        search_for(user, clave)
        time.sleep(10)
        store_screenshot(screenshot_filename_1)
        click_menu(screenshot_filename=screenshot_filename_3,tool_menu='events')
        time.sleep(10)
        search_event('busca cualquier cosa')
        time.sleep(5)
        search_timestamp('Mar 6, 5:52 pm – Mar 6, 9:52 pm')




    finally:
        browser.close_all_browsers()


# Call the main() function, checking that we are running as a stand-alone script:
if __name__ == "__main__":
    main()