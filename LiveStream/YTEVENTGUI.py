import PySimpleGUI as sg
import sys


layout = [[sg.Text("Enter Something"), sg.Input(key="_IN")],
          [sg.Text("Output:", key="_OUT")],
          [sg.Button("Ok"), sg.Button("Exit")]]

window = sg.Window("Youtube Event", layout)

while True:
    event, value = window.read()
    if event in (None, 'Exit'):
        sys.exit()
    window["_OUT"].update(value["_IN"])
