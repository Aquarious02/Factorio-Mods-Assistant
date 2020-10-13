def ui_py_converter(ui_file_name, py_file_name):
    from os import system

    if ui_file_name.find('.ui') != -1:
        ui_file_name = ui_file_name.replace('.ui', '')

    if py_file_name.find('.py') != -1:
        py_file_name = py_file_name.replace('.py', '')
    system(f'pyuic5 {ui_file_name}.ui -o {py_file_name}.py')
    print(f'Converted "{ui_file_name}.ui" to "{py_file_name}.py"')


if __name__ == '__main__':
    ui_py_converter('MainWindow', 'Scheme')
