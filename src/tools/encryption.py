import pathlib
import secrets
import os
import base64
import getpass
import argparse
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.exceptions import InvalidKey, InvalidSignature, UnsupportedAlgorithm


def handle_errors(func) -> callable:
    def wrapper(*params, **kwargs):
        try:
            return func(*params, **kwargs)
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except IsADirectoryError as e:
            print(f"Expected a file, but found a directory: {e}")
        except NotADirectoryError as e:
            print(f"Expected a directory, but found a file: {e}")
        except PermissionError as e:
            print(f"Permission denied: {e}")
        except InvalidKey as e:
            print(f"Invalid encryption key: {e}")
        except InvalidSignature as e:
            print(f"Invalid signature: {e}")
        except InvalidToken as e:
            print(f"Invalid token: {e}")
        except UnsupportedAlgorithm as e:
            print(f"Unsupported algorithm: {e}")
        except ValueError as e:
            print(f"Value error: {e}")
        except TypeError as e:
            print(f"Type error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

    return wrapper


@handle_errors
def generate_random_salt(salt_size=16):
    return secrets.token_bytes(salt_size)


@handle_errors
def derive_encryption_key(salt, password_for_key):
    return Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1).derive(password_for_key.encode())


@handle_errors
def load_existing_salt():
    return open("salt.salt", "rb").read()


@handle_errors
def save_salt(salt):
    with open("salt.salt", "wb") as salt_file:
        salt_file.write(salt)


@handle_errors
def generate_encryption_key(password_for_key, salt_size=16, is_salt_defined=False, is_saving_salt_required=True):
    salt = load_existing_salt() if is_salt_defined \
        else generate_random_salt(salt_size) if is_saving_salt_required else None
    if is_saving_salt_required and salt:
        save_salt(salt)
    derived_key = derive_encryption_key(salt, password_for_key)
    return base64.urlsafe_b64encode(derived_key) if derived_key else None


@handle_errors
def encrypt_file(file_name, key_encryption):
    fernet = Fernet(key_encryption)
    with open(file_name, "rb") as file:
        file_data = file.read()
    encrypted_data = fernet.encrypt(file_data)
    with open(file_name, "wb") as file:
        file.write(encrypted_data)


@handle_errors
def encrypt_folder(folder_name, key_encryption):
    for child in pathlib.Path(folder_name).glob("*"):
        if child.is_file():
            encrypt_file(child, key_encryption)


@handle_errors
def decrypt_file(file_name, key_encryption):
    fernet = Fernet(key_encryption)
    with open(file_name, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    with open(file_name, "wb") as file:
        file.write(decrypted_data)


@handle_errors
def decrypt_folder(folder_name, key_encryption):
    for child in pathlib.Path(folder_name).glob("*"):
        if child.is_file():
            decrypt_file(child, key_encryption)


def get_password_and_action(cryptography_args):
    selected_actions = {'encrypt': cryptography_args.encrypt, 'decrypt': cryptography_args.decrypt}
    if sum(selected_actions.values()) != 1:
        print("Please specify whether you want to encrypt or decrypt, not both.")
        exit(1)
    for cryptography_action, is_selected in selected_actions.items():
        if is_selected:
            return getpass.getpass(f"Enter the password for {cryptography_action}: "), cryptography_action


def perform_action(selected_action, path, key_to_encrypt):
    action_mapping = {
        'encrypt': (encrypt_file, encrypt_folder),
        'decrypt': (decrypt_file, decrypt_folder)
    }
    file_func, folder_func = action_mapping[selected_action]
    func = folder_func if os.path.isdir(path) else file_func
    func(path, key_to_encrypt)


if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser(description="File Encryptor Script with a Password")
    argument_parser.add_argument("path", help="Path to the file or folder to encrypt/decrypt")
    argument_parser.add_argument("-s", "--salt-size", help="Generate a new salt with the specified size", type=int)
    argument_parser.add_argument("-e", "--encrypt", action="store_true")
    argument_parser.add_argument("-d", "--decrypt", action="store_true")
    args = argument_parser.parse_args()
    password, action = get_password_and_action(args)
    if password is None:
        print("Password is required for encryption/decryption.")
        exit(1)

    encryption_key = generate_encryption_key(password, salt_size=args.salt_size, save_salt=True) if args.salt_size \
        else generate_encryption_key(password, is_salt_defined=True)

    if not encryption_key:
        print("Error generating encryption key.")
        exit(1)

    perform_action(action, args.path, encryption_key)
