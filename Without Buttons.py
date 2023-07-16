import PySimpleGUI as sg
import os
from cryptography.fernet import Fernet
import pyperclip

# Generate a key using Fernet
key = Fernet.generate_key()

# Encrypt a file
def encrypt_file():
    layout = [
        [sg.Text('Select a file to encrypt:')],
        [sg.Input(), sg.FileBrowse(key='file_path')],
        [sg.Button('Encrypt'), sg.Button('Cancel')]
    ]

    window = sg.Window('File Encryption', layout, background_color='black', icon='icon.ico')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Encrypt':
            file_path = values['file_path']
            if file_path:
                encryption_key = Fernet.generate_key()
                cipher_suite = Fernet(encryption_key)

                with open(file_path, 'rb') as file:
                    original_data = file.read()
                    encrypted_data = cipher_suite.encrypt(original_data)

                encrypted_file_path = file_path + '.enc'
                with open(encrypted_file_path, 'wb') as file:
                    file.write(encrypted_data)

                sg.popup('File encrypted successfully!', title='Success', background_color='black', text_color='white')
                window.close()
                show_encryption_key(encryption_key.decode())
                break

    window.close()


# Display encryption key
def show_encryption_key(encryption_key):
    layout = [
        [sg.Text('Encryption Key:', background_color='black', text_color='white')],
        [sg.Input(encryption_key, key='key_input', enable_events=True, background_color='black', text_color='white'), sg.Button('Copy')],
    ]

    window = sg.Window('Encryption Key', layout, background_color='black', icon='icon.ico')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Copy':
            pyperclip.copy(values['key_input'])

    window.close()


# Decrypt a file
def decrypt_file():
    layout = [
        [sg.Text('Select a file to decrypt:')],
        [sg.Input(), sg.FileBrowse(key='file_path')],
        [sg.Text('Enter the Encryption Key:')],
        [sg.Input(key='key_input', enable_events=True)],
        [sg.Button('Decrypt'), sg.Button('Cancel')]
    ]

    window = sg.Window('File Decryption', layout, background_color='black', icon='icon.ico')

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Cancel':
            break
        elif event == 'Decrypt':
            file_path = values['file_path']
            encryption_key = values['key_input']
            if file_path and encryption_key:
                try:
                    cipher_suite = Fernet(encryption_key.encode())

                    with open(file_path, 'rb') as file:
                        encrypted_data = file.read()
                        decrypted_data = cipher_suite.decrypt(encrypted_data)

                    decrypted_file_path = file_path[:-4]  # Remove '.enc' extension
                    with open(decrypted_file_path, 'wb') as file:
                        file.write(decrypted_data)

                    sg.popup('File decrypted successfully!', title='Success', background_color='black', text_color='white')
                    window.close()
                    break
                except:
                    sg.popup('Invalid encryption key!', title='Error', background_color='black', text_color='white')

    window.close()


# Dark mode theme
sg.theme('Black')

# Menu definition
menu_def = [['&File', ['&Encrypt', '&Decrypt', 'E&xit']]]

# Layout definition
layout = [
    [sg.Menu(menu_def, background_color='black', text_color='white')],
    [sg.Text('Welcome to Cryptography Project!', justification='center', font=('Helvetica', 20), relief=sg.RELIEF_RIDGE, size=(40, 1), key='-TEXT-', background_color='black', text_color='white')]
]

# Create the window
window = sg.Window('Cryptography Project', layout, background_color='black', icon='icon.ico')

# Event loop
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Encrypt':
        encrypt_file()
    elif event == 'Decrypt':
        decrypt_file()

window.close()
