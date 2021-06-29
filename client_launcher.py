#!/usr/bin/env python3
import PySimpleGUIQt as sg
import os

# Check that the client exists
if not os.path.isfile("test.py"):
    sg.Popup("The client script wasn't found in the current directory.", title="No client found.")
    exit()

sg.ChangeLookAndFeel("Default1")
address_layout = [sg.Frame(layout=[
    [sg.Text("server IP"), sg.InputText(key='ip', default_text="localhost")],
    [sg.Text("server PORT"), sg.InputText(key="port", default_text="25565")],
], title="Server address")]

account_layout = [sg.Frame(layout=[
    [sg.Combo(("Login", "Register"), key="combobox", readonly=True)],
    [sg.Text("Username"), sg.InputText(key="username", default_text="guest")],
    [sg.Text("Password"), sg.InputText(key="password", default_text="guest")]
], title="Login/Register")]

window = sg.Window("VindChat client launcher",
                   layout=[address_layout, account_layout, [sg.Button("Connect", key="start")],],
                   location=(400, 400)
                   )

while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        print(sg.WIN_CLOSED)
        break

    elif event == "start":
        print("Starting client with the following credentials:")
        print(values['ip'], values['port'])
        print(values["combobox"])
        print(values["username"], values["password"])
        window.close()
        os.system(f"./test.py --{values['combobox'].lower()} {values['username']} {values['password']}")
        exit(0)

window.close()
