from RPA.Browser.Selenium import Selenium
import time



browser = Selenium()
url = "https://bases.rexmas.cl/login"
user ='vainatec1'
clave ='M4n4g3r2020'
path = '/Robot/Web_interaction'
#screenshot_filename_0 = path + '/'+"output/screenshot_login.png"
#screenshot_filename_1 = path + '/'+"output/screenshot_ingreso.png"
#screenshot_filename_2 = path + '/'+"output/screenshot_nuevo_dominio.png"
#screenshot_filename_3 = path + '/'+"output/screenshot_importar_dominio.png"
#screenshot_filename_4 = path + '/'+"output/screenshot_rellenar_formulario.png"

def open_the_website(url):
    browser.open_available_browser(url)
    browser.driver.maximize_window()


def search_for(user, clave):
    input_field_username = "id:username"
    input_field_clave = "id:password"
    browser.input_text(input_field_username,user)
    browser.input_text(input_field_clave,clave)
    #store_screenshot(screenshot_filename_0)
    browser.press_keys(input_field_clave, "ENTER")

def click_nuevo_dominio():
    boton_field='css:.btn-primary.btn-large'
    boton=browser.find_elements(locator=boton_field)
    for b in boton:
        href=b.get_attribute(name='href')
        if href=='https://bases.rexmas.cl/bases/nueva':
            b.click()
            time.sleep(10)
            #store_screenshot(screenshot_filename)
            return

def click_importar_dominio():
    boton_field='css:.btn-primary.btn-large.ml-2'
    boton=browser.find_elements(locator=boton_field)
    for b in boton:
        href=b.get_attribute(name='href')
        print(href)
        if href=='https://bases.rexmas.cl/bases/importar':
            print(b.location)
            b.click()
            time.sleep(10)
            #store_screenshot(screenshot_filename)
            return

def click_guardar_dominio():
    boton_field = 'css:.btn-primary.btn'
    boton = browser.find_elements(locator=boton_field)
    for b in boton:
        value=b.get_attribute(name='value')
        print(value)
        return

def click_importar_bases():
    boton_field = 'css:.btn-warning.btn-fill.btn-sm'
    boton = browser.find_elements(locator=boton_field)
    for b in boton:
        value=b.get_attribute(name='value')
        print(value)
        #value.click()
        return

##diccionario tipo de nuevo dominio
ticket_dicc={'id_domain':'Prueba Dominio',
            'id_domain_type':'Estudiante',
             'id_server':'rexprod-cluster.cluster-cw5msd8qk9sy.sa-east-1.rds.amazonaws.com',
             'id_database':'rex16',
             'id_schema':'esquema',
             'id_database_user':'ususario',
             'id_database_password':'password',
             'id_email_user':'eduardo.sinning@gmail.com',
             'id_email_user_2':'consultoriarex@manager.cl',
             'id_business_national_identifier':'17864721-0',
             'id_business_contract_name':'razon social',
             }

email_user='consultoriarex@manager.cl'

def completar_scroll(input_field,value_dicc):
    val = browser.driver.find_element_by_id(input_field)
    #form_val=val.get_attribute('value')
    form_val = val.text
    #print(form_val)
    if form_val==value_dicc:
        #print(form_val)
        print('correct')
    else:
        for option in val.find_elements_by_tag_name('option'):
            if option.text == value_dicc:
                option.click()  # select() in earlier versions of webdriver
                return


def completar_formulario(diccionario_ticket):
    for key in diccionario_ticket.keys():
        input_field = 'id:'+key
        if input_field=='id:id_domain_type':
            completar_scroll(input_field=key,value_dicc=diccionario_ticket[key])
        else:
            browser.input_text(input_field, diccionario_ticket[key])

    #store_screenshot(screenshot_filename_4)

filename_example= '/Machine_learning/Database/Seguridad/autentia.csv'

def agregar_documento(filename):
    # to identify element
    s = browser.driver.find_element_by_xpath("//input[@type='file']")
    # file path specified with send_keys
    s.send_keys(filename)


def store_screenshot(filename):
    browser.screenshot(filename=filename)


def crear_ambiente():
    #Ingresar en el dominio Rex + , https://bases.rexmas.cl/login con usuario:vainatec1 y clave:M4n4g3r2020
    open_the_website(url)
    search_for(user, clave)
    time.sleep(10)
    #En la Opción Bases Seleccionar Nuevo Dominio
    click_nuevo_dominio()
    #Rellenar el formulario
    #time.sleep(5)
    completar_formulario(diccionario_ticket=ticket_dicc)
    #clickear guardar dominio
    click_guardar_dominio()

def crear_ambiente_masivo(filename):
    #Ingresar en el dominio Rex + , https://bases.rexmas.cl/login con usuario:vainatec1 y clave:M4n4g3r2020
    open_the_website(url)
    search_for(user, clave)
    time.sleep(10)
    #En la Opción Bases Seleccionar Nuevo Dominio
    click_importar_dominio()
    time.sleep(15)
    agregar_documento(filename)
    #time.sleep(5)
    click_importar_bases()

from Robot.Excel.Excel_demo import cambiar_documento
def copiar_ambiente(nombre_ambiente):
    return


def conectar_servidor_ssh(id_servidor):

    return

def verificacion(url,filename):
    open_the_website(url)
    store_screenshot(filename)
    #falta adjuntar imagen a zoho


def main():

    try:
        #crear_ambiente()
        crear_ambiente_masivo(filename_example)


    finally:
        browser.close_all_browsers()


if __name__ == "__main__":
    main()