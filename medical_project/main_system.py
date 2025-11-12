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


if __name__ == "__main__":
    system = MedicalRecordSystem()
    
    # Test 1: Registration
    print("\n🧪 TEST 1: Register Patient")
    success, patient_id, pin, message = system.register_patient(
        ssn="123-45-6789",
        name="John Doe",
        email="john@email.com",
        password="SecurePass123"
    )
    print(f"✅ Patient ID: {patient_id}, PIN: {pin}")
    
    # Test 2: Create sample file
    print("\n🧪 TEST 2: Create Sample File")
    sample_file = "sample_blood_test.txt"
    with open(sample_file, 'w') as f:
        f.write("BLOOD TEST: O+, Cholesterol: 180")
    print(f"✅ Created: {sample_file}")
    
    # Test 3: Doctor encrypts file
    print("\n🧪 TEST 3: Doctor Encrypts File")
    success, message = system.create_medical_record(
        patient_id=patient_id,
        file_path=sample_file,
        record_type="blood_test"
    )
    print(f"✅ {message}")
    
    # Test 4: Patient tries to view WITHOUT logging in
    print("\n🧪 TEST 4: Try to View Records (Not Logged In)")
    success, records, message = system.view_my_records()
    if not success:
        print(f"✅ Correctly blocked: {message}")
    
    # Test 5: Patient logs in
    print("\n🧪 TEST 5: Patient Logs In")
    success, message = system.login(
        ssn="123-45-6789",
        pin=pin,
        password="SecurePass123"
    )
    print(f"✅ {message}")
    
    # Test 6: Patient views records (NOW it works!)
    print("\n🧪 TEST 6: View Records (Logged In)")
    success, records, message = system.view_my_records()
    
    if success:
        print(f"\n✅ {message}")
        for record in records:
            print(f"\n{'='*60}")
            print(f"📄 {record['filename']} ({record['record_type']})")
            print(f"{'='*60}")
            print(record['content'])

    # Test 7: Logout
    print("\n🧪 TEST 7: Patient Logs Out")
    logout_msg = system.logout()
    print(f"✅ {logout_msg}")
    
    # Test 8: Forgot PIN
    print("\n🧪 TEST 8: Patient Forgets PIN")
    success, new_pin, message = system.forgot_pin(
        ssn="123-45-6789",
        email="john@email.com"
    )
    
    if success:
        print(f"\n✅ {message}")
        print(f"   New PIN: {new_pin}")
        print(f"   📧 Would be sent to email")
        
        # Test 9: Login with NEW PIN
        print("\n🧪 TEST 9: Login with New PIN")
        success, message = system.login(
            ssn="123-45-6789",
            pin=new_pin,  # ← Using NEW PIN!
            password="SecurePass123"  # ← Same password
        )
        
        if success:
            print(f"\n✅ {message}")
            
            # Test 10: Can still view records!
            print("\n🧪 TEST 10: View Records (With New PIN)")
            success, records, message = system.view_my_records()
            
            if success and len(records) > 0:
                print(f"\n✅ {message}")
                print(f"\n🎉 SUCCESS! Can still access encrypted files!")
                print(f"   This proves: PIN change ≠ Re-encryption needed!")