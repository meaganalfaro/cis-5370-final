# Patient Authentication System
# This system will be capabable of authenticating patients
# This includes registering patients, authenticating patients, and resetting PINs
# Each patient will be authenticated with a unique PIN

import hashlib
from datetime import datetime
import random
import json

# This class will handle the authentication of patients
class PatientAuthenticator:
    
    # This function will initialize the authenticator and store the patients
    # In real practice this would be stored in a database
    def __init__(self):
        self.patients = {}
        self.patient_id_counter = 1
        self.load_patients()
    
    def hash_credential(self, credential):
        
        # Encoding credential to bytes
        credential_bytes = credential.encode('utf-8')
        
        # Hashing the credential using SHA-256
        hashed_credential = hashlib.sha256(credential_bytes).hexdigest()
        
        # Returning hashed credential
        return hashed_credential

    # This function will register a new patient
    def register_patient(self, ssn, name, email, password):
        print(f"\n{'='*60}")
        print(f"REGISTERING NEW PATIENT: {name}")
        print(f"{'='*60}")
        
        # Check if patient already exists
        ssn_hash = self.hash_credential(ssn)
        for patient in self.patients.values():
            if patient['ssn_hash'] == ssn_hash:
                print(f"Patient already exists")
                return False, patient['patient_id'], None, "Patient already exists"
        
        # Generate a random 6-digit PIN
        import random
        pin = str(random.randint(100000, 999999))
        print(f"\nGenerated PIN: {pin}")
        print(f"\n\tGive this to the patient on paper!")
        
        # Hash all credentials
        ssn_hash = self.hash_credential(ssn)
        pin_hash = self.hash_credential(pin)
        password_hash = self.hash_credential(password)
        
        # Store patient information
        patient_id = self.patient_id_counter
        self.patient_id_counter += 1
        
        self.patients[patient_id] = {
            'patient_id': patient_id,
            'name': name,
            'ssn_hash': ssn_hash,        # Hashed - can't reverse!
            'pin_hash': pin_hash,        # Hashed - can't reverse!
            'password_hash': password_hash,  # Hashed - can't reverse!
            'email': email,
            'registered_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        print(f"\nPatient registered successfully!")
        print(f"\tPatient ID: {patient_id}")
        print(f"\tName: {name}")
        print(f"\tEmail: {email}")
        print(f"\n{'='*40}")
        
        return True, patient_id, pin, "Registration successful"
    
    # Used to verify a patients login credentials
    def authenticate_patient(self, ssn, pin, password):
        
        print(f"\n{'='*60}")
        print(f"AUTHENTICATING PATIENT")
        print(f"{'='*60}")
        
        
        hashed_ssn = self.hash_credential(ssn)
        hashed_pin = self.hash_credential(pin)
        hashed_password = self.hash_credential(password)

        for patient in self.patients.values():
            if patient['ssn_hash'] == hashed_ssn and patient['pin_hash'] == hashed_pin and patient['password_hash'] == hashed_password:
                
                return True, patient['patient_id'], f"Welcome, {patient['name']}!"
            
                
        print(f"Authentication failed!")
        return False, None, "Invalid credentials"
    
    # Function incase patient forgets their pin 
    def reset_pin(self, ssn, email):
        print(f"\n{'='*60}")
        print(f"PIN RECOVERY")
        print(f"{'='*60}")
        
        
        # Hash the SSN
        hashed_ssn = self.hash_credential(ssn)
        # Find the patient with matching SSN hash
        for patient in self.patients.values():
            if patient['ssn_hash'] == hashed_ssn:
                # Verify the email matches
                if patient['email'] != email:
                    print(f"\nEmail does not match")
                    return False, None, "Invalid Credentials"

                new_pin = str(random.randint(100000,999999))
                    # Hash the new PIN
                hashed_new_pin = self.hash_credential(new_pin)
                    # Update patient['pin_hash'] with the new hash
                patient['pin_hash'] = hashed_new_pin

                print(f"Pin successfully reseted")
                print(f"New Pin: {new_pin}")

                self.save_patients()

                return True, new_pin, "Pin reset successful"
    
        
        print(f"Invalid Credentials")
        return False, None, "Patient not found"


    # "Display all registered patients (For Demonstration purposes)
    def list_patients(self):
        print(f"\n{'='*60}")
        print(f"REGISTERED PATIENTS")
        print(f"{'='*60}\n")
        
        if not self.patients:
            print("No patients registered yet.")
            return
        
        for patient_id, patient in self.patients.items():
            print(f"Patient ID: {patient_id}")
            print(f"Name: {patient['name']}")
            print(f"Email: {patient['email']}")
            print(f"Registered: {patient['registered_at']}")
            print(f"SSN Hash: {patient['ssn_hash'][:30]}...")
            print(f"PIN Hash: {patient['pin_hash'][:30]}...")
            print()

    # Save patients to file
    def save_patients(self):
        data = {
            'patients': self.patients,
            'patient_id_counter': self.patient_id_counter
        }
        with open('patients_data.json', 'w') as f:
            json.dump(data, f, indent=2)
    
    # Load patients from file
    def load_patients(self):
        try:
            with open('patients_data.json', 'r') as f:
                data = json.load(f)
                self.patients = data['patients']
                # Convert string keys back to integers
                self.patients = {int(k): v for k, v in self.patients.items()}
                self.patient_id_counter = data['patient_id_counter']
            print(f"Loaded {len(self.patients)} patients from file")
        except FileNotFoundError:
            print("No existing patient data found, starting fresh")
        except Exception as e:
            print(f"Error loading patients: {e}")
