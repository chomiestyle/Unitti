from RPA.Desktop.Windows import Windows
import time

win = Windows()

def open_calculator():
    win.open_from_search("calc.exe", "Calculator")
    elements = win.get_window_elements()
    for j in range(len(elements[0])):
        #print(elements[0][j])
        #print('los valores son :')
        #print(elements[1][j]['automation_id'])
        if elements[1][j]['automation_id']=='CalculatorResults':
            print(elements[1][j])

def make_calculations(expression):
    win.send_keys(expression)
    boton_conect = win.get_element_rectangle('id:CalculatorResults')
    print(boton_conect)
    result = win.get_element_rich_text('id:CalculatorResults')
    #print(result)
    return int(result.strip('Display is '))

def open_teamviewer():
    #win.open_application("TeamViewer")
    win.open_from_search("TeamViewer", "TeamViewer")
    ##time.sleep(120)
    elements = win.get_window_elements()
    for j in range(len(elements[0])):
        #print(elements[0][j])
        #print('value :')
        #print(elements[1][j]['automation_id'])
        if elements[1][j]['name']=='Connect':
            print(elements[1][j])

def connect_button():
    #boton_element=win.get_element_rectangle('id:2')
    #print(boton_element)
    win.mouse_click('name:Connect')

    time.sleep(20)
    win.send_keys('92id1d')
    elements_win2 = win.get_window_elements()

    for j in range(len(elements_win2[0])):
        #print(elements_win2[0][j])
        #print('los valores son :')
        #print(elements_win2[1][j])
        if elements_win2[1][j]['rich_text']=='Log On':
            print(elements_win2[1][j])
    win.mouse_click('')


def calcular():
    open_calculator()
    exp = '5*2='
    result = make_calculations(exp)
    print(f"Calculation result of '{exp}' is '{result}'")
    win.close_all_applications()
def TeamViewer():
    open_teamviewer()
    connect_button()
    #win.close_all_applications()

if __name__ == "__main__":
    #TeamViewer()
    #calcular()
    TeamViewer()