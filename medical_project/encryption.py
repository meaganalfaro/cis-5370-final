# Medical File Encryption System
# This system will be capabable of encrypting many different types of files
# This includes medical images, reports, and other sensitive data
# Each file will be encrypted with a unique key

from cryptography.fernet import Fernet
import os
import json
from datetime import datetime

# This class will handle the encrypting and decrypting of files
class MedicalFileEncryptor:
    def __init__(self):
        # This will store the keys, in real practice this would be stored in a detabase. 
        self.key_storage = {}

    # This function will encrypt the file 
    # Recieves the input file path, pateint id, and the record type
    def encrypt_file(self, input_file_path, patient_id, record_type):
        print(f"\n{'='*40}")
        print(f"Encrypting file: {input_file_path}")
        print(f"\n{'='*40}")

        # Check if the file exists
        if not os.path.exists(input_file_path):
            print(f"Error: File not found: {input_file_path}")
            return None
    
        # Getting the file size and name
        file_size = os.path.getsize(input_file_path)
        file_name = os.path.basename(input_file_path)

        # Printing the file information
        print(f"\n File: {file_name}")
        print(f"\n\tSize: {file_size} bytes")
        print(f"\n\tPatient ID: {patient_id}")
        print(f"\n\tRecord Type: {record_type}")

        # Reading the file contents
        print(f"\n\tReading file contents...")
        with open(input_file_path, 'rb') as f:
            file_contents = f.read()

        # Generating a key for the file and is unique to the file
        print(f"\n Generating key...")
        encryption_key = Fernet.generate_key()
        cipher = Fernet(encryption_key)

        print(f"\nKey generated successfully")

        print(f"\nEncrypting file contents...")
        encrypted_contents = cipher.encrypt(file_contents)

        print(f"\nFile contents encrypted successfully")

        # Saving the encrypted file
        encrypted_filename = f"encrypted_{file_name}.enc" 
        with open(encrypted_filename, 'wb') as f:
            f.write(encrypted_contents)

        print(f"\nEncrypted file saved as: {encrypted_filename}")

        # Storing the encryption key
        # In real practice this would be stored in a database
        record_id = len(self.key_storage) + 1
        self.key_storage[record_id] = {
            'record_id': record_id,
            'patient_id': patient_id,
            'record_type': record_type,
            'original_filename': file_name,
            'encryption_key': encryption_key.decode(),
            'encrypted_filename': encrypted_filename,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size': file_size,
        }

        print(f"\nKey stored successfully")

        print(f"\n{'='*40}")
        print(f"\nEncryption complete")
        print(f"\n{'='*40}")

        return self.key_storage[record_id]
    
    # This function will decrypt the file
    # Recieves the record id and the output file path
    def decrypt_file(self, record_id, output_file_path=None):
        print(f"\n{'='*40}")
        print(f"Decrypting file: {record_id}")
        print(f"\n{'='*40}")

        # Check if the record id is valid
        if record_id not in self.key_storage:
            print(f"Error: Record id not found: {record_id}")
            return None

        # Get the record information
        record_info = self.key_storage[record_id]

        print(f"\nRecord information:")
        print(f"\n\tPatient ID: {record_info['patient_id']}")
        print(f"\n\tRecord Type: {record_info['record_type']}")
        print(f"\n\tOriginal Filename: {record_info['original_filename']}")
        print(f"\n\tEncrypted: {record_info['created_at']}")  # ← FIXED

        # Read the encrypted file
        encrypted_filename = record_info['encrypted_filename']
        
        if not os.path.exists(encrypted_filename):
            print(f"Error: Encrypted file '{encrypted_filename}' not found!")
            return None
        
        print(f"\nReading encrypted file...")
        with open(encrypted_filename, 'rb') as f:
            encrypted_data = f.read()

        # Getting the encryption key (need to encode it back to bytes)
        encryption_key = record_info['encryption_key'].encode()  # ← FIXED
        cipher = Fernet(encryption_key)

        # Decrypting the file
        print(f"\nDecrypting file contents...")
        try:
            decrypted_data = cipher.decrypt(encrypted_data)  # ← Fixed typo
            print(f"\nFile contents decrypted successfully")
        except Exception as e:
            print(f"\nDecryption failed: {e}")
            return None

        # Saving the decrypted file
        if output_file_path is None:
            output_file_path = f"decrypted_{record_info['original_filename']}"
        
        with open(output_file_path, 'wb') as f:
            f.write(decrypted_data)
        print(f"\nDecrypted file saved as: {output_file_path}")

        print(f"\n{'='*40}")
        print(f"\nDecryption complete")
        print(f"\n{'='*40}")

        return decrypted_data

        
    # This function will display the encrypted files
    def list_encrypted_files(self, patient_id=None):
        print(f"\n{'='*40}")
        print(f"Encrypted Files Database")
        print(f"\n{'='*40}")

        if not self.key_storage:
            print(f"\nNo encrypted files found")
            return

    
        for record_id, info in self.key_storage.items():
            print(f"\nRecord ID: {record_id}")
            print(f"\n\tPatient ID: {info['patient_id']}")
            print(f"\n\tRecord Type: {info['record_type']}")
            print(f"\n\tOriginal Filename: {info['original_filename']}")
            print(f"\n\tEncrypted: {info['created_at']}")
            print()
    
    def demonstrate_wrong_key(self, record_id):
        # Shows what happens when you try to decrypt with wrong key
        print(f"\n{'='*40}")
        print(f"Demonstrating wrong key decryption")
        print(f"\n{'='*40}")

        if record_id not in self.key_storage:
            print(f"\nError: Record id not found: {record_id}")
            return

        record_info = self.key_storage[record_id]
        encrypted_filename = record_info['encrypted_filename']

        print(f"\n Scenario: Attacker tries to decrypt without the correct key")
        print(f"\n\tTarget file: {encrypted_filename}")

        # Read encrypted data
        with open(encrypted_filename, 'rb') as f:
            encrypted_data = f.read()

        print(f"\nAttacker generates their own key...")
        wrong_key = Fernet.generate_key()
        wrong_cipher = Fernet(wrong_key)

        correct_key = record_info['encryption_key']
        print(f"\n\tCorrect key: {correct_key[:30]}...")
        print(f"\n\tAttacker's key: {wrong_key.decode()[:30]}...")

        print(f"\nAttacker attempts decryption...")

        try:
            wrong_cipher.decrypt(encrypted_data)
            print(f"\n\tERROR: This should not work!")
        except Exception as e:
            print(f"\n\tGOOD: Decryption failed!")
            print(f"\n\tError: {type(e).__name__}")
            print(f"\n\tWithout the correct key, the file is SECURE!")

        print(f"\n{'='*40}")

