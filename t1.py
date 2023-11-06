import tkinter as tk
from tkinter import filedialog, messagebox
from cryptography.fernet import Fernet
import os

class FaceLock:
    def __init__(self, root):
        self.root = root
        self.root.title("File Locking System")
        self.root.geometry("800x600")
        self.keys = {}  # Dictionary to store keys for each file

    def save_keys(self, filename="keys.txt"):
        with open(filename, 'w') as key_file:
            for file_name, key in self.keys.items():
                key_file.write(f"{file_name}::{key.decode()}\n")

    def load_keys(self, filename="keys.txt"):
        if os.path.exists(filename):
            with open(filename, 'r') as key_file:
                lines = key_file.readlines()
                for line in lines:
                    file_name, key = line.strip().split("::")
                    self.keys[file_name] = key.encode()

    def encrypt_file(self):
        try:
            key = Fernet.generate_key()
            cipher_suite = Fernet(key)
            file_path = filedialog.askopenfilename()

            with open(file_path, 'rb') as file:
                file_data = file.read()

            encrypted_data = cipher_suite.encrypt(file_data)

            with open(file_path, 'wb') as file:
                file.write(encrypted_data)

            key_folder = "C:/Users/Mohammed Arif H/PycharmProjects/pythonProject/newtester/key"  # Specify the folder path
            os.makedirs(key_folder, exist_ok=True)
            file_name = os.path.basename(file_path)
            key_file_path = os.path.join(key_folder, f'{file_name}_key.key')

            with open(key_file_path, 'wb') as key_file:
                key_file.write(key)

            self.keys[file_name] = key  # Store the key in the dictionary
            self.save_keys()  # Save the keys to a file

            messagebox.showinfo(title="File Encryption", message="The file has been encrypted successfully.")
        except Exception as e:
            messagebox.showerror(title="File Encryption Error", message=e)

    def decrypt_file(self):
        try:
            file_path = filedialog.askopenfilename()
            file_name = os.path.basename(file_path)

            if file_name not in self.keys:
                messagebox.showerror(title="File Decryption Error", message="No key found for this file.")
                return

            key = self.keys[file_name]
            cipher_suite = Fernet(key)

            with open(file_path, 'rb') as file:
                encrypted_data = file.read()

            decrypted_data = cipher_suite.decrypt(encrypted_data)

            with open(file_path, 'wb') as file:
                file.write(decrypted_data)

            messagebox.showinfo(title="File Decryption", message="The file has been decrypted successfully.")
        except Exception as e:
            messagebox.showerror(title="File Decryption Error", message=e)

    def create_gui(self):
        encrypt_button = tk.Button(self.root, text="Encrypt File", command=self.encrypt_file)
        decrypt_button = tk.Button(self.root, text="Decrypt File", command=self.decrypt_file)

        encrypt_button.pack()
        decrypt_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = FaceLock(root)
    app.load_keys()  # Load keys from a file at the start of the program
    app.create_gui()
    root.mainloop()
