"""
This program has a GUI that allows anything from the datalayer to be backed up
to a .json file and then restored.
"""
import json
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import filedialog as fd
import httpx
from ctrlx import CtrlX

DEFAULT_URL = "https://192.168.1.1"
DEFAULT_PATH = "plc/app/Application/sym/PersistentVars"
DEFAULT_USER = "boschrexroth"
DEFAULT_PASSWORD = "boschrexroth"
FILETYPES = [("json files", "*.json"), ("All files", "*.*")]

window = tk.Tk()
window.title(" ctrlX Save Datalayer ")
json_object = tk.StringVar()


url = tk.Label(text="URL")
url.grid(column=0,row=1)
path = tk.Label(text="Backup Path")
path.grid(column=0, row=2)
user = tk.Label(text="User")
user.grid(column=0, row=3)
password = tk.Label(text="Password")
password.grid(column=0, row=4)

url_entry = tk.Entry(window, textvariable=tk.StringVar(window, DEFAULT_URL), width=40)
url_entry.grid(column=1, row=1, columnspan=3)
path_entry = tk.Entry(window, textvariable=tk.StringVar(window, DEFAULT_PATH), width=40)
path_entry.grid(column=1, row=2, columnspan=3)
user_entry = tk.Entry(window, textvariable=tk.StringVar(window, DEFAULT_USER), width=40)
user_entry.grid(column=1, row=3, columnspan=3)
password_entry = tk.Entry(window, textvariable=tk.StringVar(window, DEFAULT_PASSWORD), width=40)
password_entry.grid(column=1, row=4, columnspan=3)


"""
When the backup button is pressed use get_folder function to read the datalayer
and save it to a .json file.
"""
def backup():
    with httpx.Client(verify=False) as client:
        try:
            ctrlx = CtrlX(
                client, url_entry.get(), user_entry.get(), password_entry.get()
            )
        except httpx.ConnectError:
            showinfo("Connection Failed", "Failed to connect to controller")
            return

        try:
            data = {path_entry.get(): ctrlx.get_folder(path_entry.get())}
        except AttributeError:
            showinfo("Connection Failed", "Failed to read path")
            return

        json_text = json.dumps(data, indent=4, sort_keys=True)

        file = fd.asksaveasfile(mode="w", defaultextension=FILETYPES, filetypes=FILETYPES)
        file.write(json_text)


backup_button = tk.Button(window, text="Backup", command=backup)
backup_button.grid(column=0, row=6, columnspan=4)


"""
Restore the same .json file that was saved with the backup function.
"""
def restore():
    file = fd.askopenfile(filetypes=FILETYPES)
    file_data = json.load(file)

    with httpx.Client(verify=False) as client:
        try:
            ctrlx = CtrlX(
                client, url_entry.get(), user_entry.get(), password_entry.get()
            )
        except httpx.ConnectError:
            showinfo("Connection Failed", "Failed to connect to controller")
            return

        try:
            ctrlx.put_folder("", file_data)
        except AttributeError:
            showinfo("Connection Failed", "Failed to write data")
            return


restore_button = tk.Button(window, text="Restore", command=restore)
restore_button.grid(column=0, row=5, columnspan=4)


window.mainloop()
