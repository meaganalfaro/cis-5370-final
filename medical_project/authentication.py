# Patient Authentication System
# This system will be capabable of authenticating patients
# This includes registering patients, authenticating patients, and resetting PINs
# Each patient will be authenticated with a unique PIN

import hashlib
from datetime import datetime
import random

# This class will handle the authentication of patients
class PatientAuthenticator:
    
    # This function will initialize the authenticator and store the patients
    # In real practice this would be stored in a database
    def __init__(self):
        
        self.patients = {}
        self.patient_id_counter = 1
    
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
                print(f"\n Authentication successful!")
                print(f"\n\t Welcome, {patient['name']}!")
                return True, patient['patient_id'], f"Welcome, {patient['name']}!"
            else:
                print(f"Invalid Credentials!")
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
                print(f"New Pin: {patient['pin_hash']}")
                return True, new_pin, "Pin reset successful"
    
        print(f"Invalid Credentials")
        return False, None, "Patient not found"


    
    def list_patients(self):
        """Display all registered patients (for demo purposes)."""
        print(f"\n{'='*60}")
        print(f"REGISTERED PATIENTS")
        print(f"{'='*60}\n")
        
        if not self.patients:
            print("No patients registered yet.")
            return
        
        for patient_id, patient in self.patients.items():
            print(f"Patient ID: {patient_id}")
            print(f"  Name: {patient['name']}")
            print(f"  Email: {patient['email']}")
            print(f"  Registered: {patient['registered_at']}")
            print(f"  SSN Hash: {patient['ssn_hash'][:30]}...")
            print(f"  PIN Hash: {patient['pin_hash'][:30]}...")
            print()


# ============================================================
# DEMO: Test the authentication system
# ============================================================

def demo():
    """Demonstrate the authentication system."""
    
    print("\n" + "="*60)
    print("PATIENT AUTHENTICATION SYSTEM - DEMO")
    print("="*60)
    
    auth = PatientAuthenticator()
    
    # ========================================
    # STEP 1: Register a new patient
    # ========================================
    
    input("\nPress Enter to register a new patient...")
    
    success, patient_id, pin, message = auth.register_patient(
        ssn="123-45-6789",
        name="John Doe",
        email="john@email.com",
        password="MySecurePassword123"
    )
    
    # Save the PIN for later
    johns_pin = pin
    
    # ========================================
    # STEP 2: View registered patients
    # ========================================
    
    input("\nPress Enter to view registered patients...")
    
    auth.list_patients()
    
    # ========================================
    # STEP 3: Patient tries to login
    # ========================================
    
    input("\nPress Enter to test patient login...")
    
    print("\n🏥 John Doe tries to login to patient portal...")
    print(f"   SSN: 123-45-6789")
    print(f"   PIN: {johns_pin}")
    print(f"   Password: MySecurePassword123")
    
    success, patient_id_result, message = auth.authenticate_patient(
        ssn="123-45-6789",
        pin=johns_pin,
        password="MySecurePassword123"
    )
    
    if success:
        print(f"\n✅ {message}")
        print(f"   Logged in as Patient ID: {patient_id_result}")
    else:
        print(f"\n❌ {message}")
    
    # ========================================
    # STEP 4: Wrong password attempt
    # ========================================
    
    input("\nPress Enter to test wrong password...")
    
    print("\n🚨 Attacker tries with wrong password...")
    
    success, _, message = auth.authenticate_patient(
        ssn="123-45-6789",
        pin=johns_pin,
        password="WrongPassword123"
    )
    
    if not success:
        print(f"\n✅ GOOD: Login denied - {message}")
    else:
        print(f"\n❌ ERROR: Should have been denied!")
    
    # ========================================
    # STEP 5: PIN recovery
    # ========================================
    
    input("\nPress Enter to test PIN recovery...")
    
    print("\n🔄 John forgets his PIN and requests recovery...")
    
    success, new_pin, message = auth.reset_pin(
        ssn="123-45-6789",
        email="john@email.com"
    )
    
    if success:
        print(f"\n✅ {message}")
        print(f"   New PIN: {new_pin}")
        print(f"   📧 This would be sent to: john@email.com")
        
        # ========================================
        # STEP 6: Login with new PIN
        # ========================================
        
        input("\nPress Enter to login with new PIN...")
        
        print("\n🏥 John tries to login with NEW PIN...")
        
        success, patient_id_result, message = auth.authenticate_patient(
            ssn="123-45-6789",
            pin=new_pin,
            password="MySecurePassword123"
        )
        
        if success:
            print(f"\n✅ {message}")
            print(f"   ✓ Can still login with new PIN!")
            print(f"\n   💡 IMPORTANT: Encryption keys unchanged!")
            print(f"      Medical files still encrypted with same keys.")
    
    # ========================================
    # SUMMARY
    # ========================================
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print("""
What we demonstrated:

1. ✅ Registered patient with hashed credentials
2. ✅ Three-factor authentication (SSN + PIN + Password)
3. ✅ Rejected wrong password attempts
4. ✅ PIN recovery without affecting encryption
5. ✅ Login works with new PIN

Key Security Points:
• Credentials are HASHED (one-way, can't reverse)
• Authentication ≠ Encryption
• Changing PIN doesn't re-encrypt files
• Three factors = Better security

Next: Combine authentication + encryption = Complete system!
""")
    
    print("="*60)


if __name__ == "__main__":
    # TODO: Complete the missing functions above, then run this!
    demo()