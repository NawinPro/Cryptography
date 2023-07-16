import PySimpleGUI as sg
import os
from cryptography.fernet import Fernet
import pyperclip

# Generate a key using Fernet
key = Fernet.generate_key()

# Encrypt a file
def encrypt_file():
    file_path = sg.popup_get_file('Select a file to encrypt', file_types=(("All Files", "*.*"),))
    if file_path:
        encryption_key = Fernet.generate_key()
        cipher_suite = Fernet(encryption_key)

        with open(file_path, 'rb') as file:
            original_data = file.read()
            encrypted_data = cipher_suite.encrypt(original_data)

        encrypted_file_path = file_path + '.enc'
        with open(encrypted_file_path, 'wb') as file:
            file.write(encrypted_data)

        sg.popup('File encrypted successfully!', title='Success')
        show_encryption_key(encryption_key.decode())


# Display encryption key
def show_encryption_key(encryption_key):
    layout = [
        [sg.Text('Encryption Key:')],
        [sg.Input(encryption_key, key='key_input', enable_events=True), sg.Button('Copy')],
    ]

    window = sg.Window('Encryption Key', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break
        elif event == 'Copy':
            pyperclip.copy(values['key_input'])

    window.close()


# Decrypt a file
def decrypt_file():
    file_path = sg.popup_get_file('Select a file to decrypt', file_types=(("Encrypted Files", "*.enc"),))
    if file_path:
        encryption_key = sg.popup_get_text('Enter the Encryption Key')
        if encryption_key:
            try:
                cipher_suite = Fernet(encryption_key.encode())

                with open(file_path, 'rb') as file:
                    encrypted_data = file.read()
                    decrypted_data = cipher_suite.decrypt(encrypted_data)

                decrypted_file_path = file_path[:-4]  # Remove '.enc' extension
                with open(decrypted_file_path, 'wb') as file:
                    file.write(decrypted_data)

                sg.popup('File decrypted successfully!', title='Success')
            except:
                sg.popup('Invalid encryption key!', title='Error')


# Dark mode theme
sg.theme('Black')

# Layout definition
layout = [
    [sg.Text('Welcome to Cryptography Project!', justification='center', font=('Helvetica', 20), relief=sg.RELIEF_RIDGE, size=(40, 1), key='-TEXT-')],
    [sg.Button('Encrypt', size=(15, 5), button_color=('white', 'green')), sg.Button('Decrypt', size=(15, 5), button_color=('white', 'sky blue')), sg.Button('Exit', size=(15,5), button_color=('white', 'red'))]
]

# Create the window
window = sg.Window('Cryptography Project', layout, element_justification='c', finalize=True, keep_on_top=True)

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
