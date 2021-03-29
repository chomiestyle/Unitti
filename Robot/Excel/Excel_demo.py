from RPA.Excel.Application import Application

app = Application()
path='C:/Users/56979/PycharmProjects/Unitti/Robot/Excel'
app.open_application()



def cambiar_documento(filename, sheet_name,nombre_ambiente,fila,columna):
    app.open_workbook(path + '/'+filename)
    app.set_active_worksheet(sheetname=sheet_name)
    app.write_to_cells(row=fila, column=columna, value=nombre_ambiente)
    app.save_excel()
    app.quit_application()