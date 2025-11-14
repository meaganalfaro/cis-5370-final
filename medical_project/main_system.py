from encryption import MedicalFileEncryptor
from authentication import PatientAuthenticator
import os 


class MedicalRecordSystem:
    # Initializing the system
    def __init__(self):
        self.encryptor = MedicalFileEncryptor()
        self.authenticator = PatientAuthenticator()
        self.current_user_id = None

    # Registers a new patient
    def register_patient(self, ssn, name, email, password):
        
        print(f"\n{'='*60}")
        print(f"HOSPITAL: Registering Patient")
        print(f"{'='*60}")
        
        # Call the authenticator's register_patient function
        success, patient_id, pin, message = self.authenticator.register_patient(ssn, name, email, password)

        # To save previous or any patients
        self.authenticator.save_patients()

        # Returning result
        return success, patient_id, pin, message

    # Logs in user
    def login(self, ssn, pin, password):

        print(f"\n{'='*60}")
        print(f"PATIENT PORTAL: Login")
        print(f"{'='*60}")
        
        # Call the authenticator's authenticate_patient function
        
        success, patient_id, message = self.authenticator.authenticate_patient(ssn,pin,password)
        # Checking if it is the same user
        if success:
            self.current_user_id = patient_id
            
    
        return success, message

        
    # Logs out user
    def logout(self):
        # Check if someone is logged in
        if self.current_user_id == None:
            return print(f"\n No one is logged in")
        
        # Clear the current_user_id
        self.current_user_id = None

    # Creating a medical record 
    def create_medical_record(self, patient_id, file_path, record_type):
        
        print(f"\n{'='*60}")
        print(f"DOCTOR: Creating Medical Record")
        print(f"{'='*60}")
        
        #  Check if the patient exists

        if patient_id not in self.authenticator.patients:
            return False, "Patient not found"
        
        # Check if the file exists
        if not os.path.exists(file_path):
            return False, f"File not found: {file_path}"
        
        # Encrypt the file using the encryptor
        record_info = self.encryptor.encrypt_file(file_path, patient_id, record_type)
        
        # Check if encryption was successful
        if record_info is None:
            return False, "Encryption failed"
        
        # Return success
        return True, f"Medical record created successfully (Record ID {record_info['record_id']})"

    # View medical records for the current patient
    def view_my_records(self):

        print(f"\n{'='*60}")
        print(f"PATIENT: Viewing My Medical Records")
        print(f"{'='*60}")
        
        # Check if anyone is logged in
        if self.current_user_id is None:
            return False, [], "No one is logged in. Please login first."
        
        my_records = []
        # Get all encrypted records for THIS patient
        for record_id, record_info in self.encryptor.key_storage.items():
            
            if record_info['patient_id'] == self.current_user_id:
                print(f"\nFound record: {record_info['original_filename']}")
                print(f"\n\tDecrypting...")
                
                decrypted_data = self.encryptor.decrypt_file(record_id)
                
                if decrypted_data:
                    my_records.append({
                        'record_id': record_id,
                        'filename': record_info['original_filename'],
                        'record_type': record_info['record_type'],
                        'created_at': record_info['created_at'],
                        'content': decrypted_data.decode('utf-8')
                    })
        if len(my_records) == 0:
            return False, [], "No medical records found"
        
        return True, my_records, f"Found {len(my_records)} record(s)"

    # Incase someone forgot a pin
    def forgot_pin(self, ssn, email):

        print(f"\n{'='*60}")
        print(f"PATIENT: Forgot PIN Recovery")
        print(f"{'='*60}")

        #  Call the authenticator's reset_pin function
        success, new_pin, message = self.authenticator.reset_pin(ssn, email)
        
        # If successful, print an important reminder
        if success: 
            print(f"\nIMPORTANT: Your medical records are still encrypted")
    
        return success, new_pin, message

# Interactive menu functions
def main_menu(system):
    while True:
        print("\n" + '='*60)
        print("MEDICAL RECORD SYSTEM - MAIN MENU".center(60))
        print("="*60)
        print("\n[1] Doctor Portal")
        print("[2] Patient Portal")
        print("[3] Exit")

        choice = input("\nEnter your choice (1-3): ").strip()

        if choice == "1":
            doctor_portal(system)
        elif choice == "2":
            patient_portal(system)
        elif choice == "3":
            print("\nThank you for using Medical Record System!")
            exit(0)
        else:
            print("\n Invalid choice. Please try again.")

# Doctor portal system
def doctor_portal(system):
    while True:
        print("\n" + "="*60)
        print("DOCTOR PORTAL".center(60))
        print("="*60)
        print("\n[1] Register New Patient")
        print("[2] Create Medical Record (Encrypt File)")
        print("[3] View All Patients")
        print("[4] Back to Main Menu")

        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            print("\nRegistering a New Patient!")
            print("-"*60)

            ssn = input("Enter last 4 digits of SSN: ").strip()
            name = input("Enter full name: ").strip()
            email = input("Enter email: ").strip()
            password = input("Enter password: ").strip()

            success, patient_id, pin, message = system.register_patient(ssn, name, email, password)

            if success:
                print(f"\n {message}")
                print(f"\n IMPORTANT: Give patient this PIN on paper:")
                print(f"\n\tPIN: {pin}")
                input("\nPress Enter to continue...")
        
        elif choice == "2":
            print("\nCreate Medical Record")
            print("-" * 60)
            
            # Get patient ID
            try:
                patient_id = int(input("Enter patient ID: ").strip())
            except ValueError:
                print("\nInvalid patient ID")
                input("\nPress Enter to continue...")
                continue
            
            # Ask if they want to create a sample file or use existing
            print("\n[1] Create sample blood test file")
            print("[2] Use existing file")
            file_choice = input("\nChoice (1-2): ").strip()
            
            if file_choice == "1":
                # Create sample file
                filename = f"blood_test_patient_{patient_id}.txt"
                with open(filename, 'w') as f:
                    f.write(f"""
BLOOD TEST RESULTS
==================
Patient ID: {patient_id}
Date: 2025-11-10

Blood Type: O+
Cholesterol: 180 mg/dL
Glucose: 95 mg/dL
Hemoglobin: 14.5 g/dL

All values within normal range.
                    """)
                print(f"\nCreated sample file: {filename}")
                file_path = filename
                record_type = "blood_test"
                
            else:
                # Use existing file
                file_path = input("Enter file path: ").strip()
                record_type = input("Enter record type (blood_test/prescription/xray): ").strip()
            
            # Create the record
            success, message = system.create_medical_record(
                patient_id, file_path, record_type
            )
            
            if success:
                print(f"\n{message}")
            else:
                print(f"\n{message}")
            
            input("\nPress Enter to continue...")

        elif choice == "3":
            system.authenticator.list_patients()
            input("\nPress Enter to continue")
        
        elif choice == "4":
            break
        else: 
            print("\nInvalid choice. Please try again.")

# Patient portal
def patient_portal(system):
    while True:
        print("\n" + "="*60)
        print("PATIENT PORTAL".center(60))
        print("="*60)
        print("\n[1] Login")
        print("[2] View My Medical Records")
        print("[3] Forgot PIN")
        print("[4] Logout")
        print("[5] Back to Main Menu")

        choice = input("\nEnter your choice (1-5): ").strip()

        if choice == "1":
            # Login section
            print("\nPatient Login")
            print("-"*60)

            ssn = input("Enter last 4 digits of SSN: ").strip()
            pin = input("Enter PIN: ").strip()
            password = input("Enter password: ").strip()

            success, message = system.login(ssn, pin, password)

            if success:
                print(f"\n{message}")
            else: 
                print(f"\n{message}")

            input("\nPress Enter to continue...")

        elif choice == "2":
            print("\nMedical Records")
            print("-"*60)

            success, records, message = system.view_my_records()

            if success and len(records) > 0:
                print(f"\n{message}\n")

                for i, record in enumerate(records, 1):
                    print("="*60)
                    print(f"Record {i}: {record['filename']} ({record['record_type']})")
                    print("=" * 60)
                    print(f"Created: {record['created_at']} ")
                    print("\nContent:")
                    print(record['content'])
                    print()
            
            elif success and len(records) == 0:
                print(f"\n{message}")
            else:
                print(f"\n{message}")

            input("\nPress Enter to continue...")

        elif choice == "3":
            print("\nForgot PIN Recovery")
            print("-"*60)

            ssn = input("Enter last 4 digits of SSN: ").strip()
            email = input("Enter email: ").strip()

            success, new_pin, message = system.forgot_pin(ssn, email)

            if success:
                print(f"\n{message}")
                print(f"\tNew PIN: {new_pin}")
                print(f"\t(this would be sent to your email)")
            else: 
                print(f"\n{message}")
            
            input("\nPress Enter to continue...")

        elif choice == "4":
            logout_message = system.logout()
            print(f"\n{logout_message}")
            input("\nPress Enter to continue...")
        
        elif choice == "5":
            break

        else:
            print("\nInvalid choice. Please try again.")
            
if __name__ == "__main__":
    # Initialize the system
    system = MedicalRecordSystem()
    
    # Start the interactive menu
    main_menu(system)