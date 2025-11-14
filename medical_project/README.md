# Medical Record Sharing System

## Project Overview
A secure medical record sharing system that demonstrates proper separation of authentication and encryption for protecting sensitive healthcare data.

## Key Security Features
* **Separate Authentication and Encryption**: Patient credentials (SSN + PIN + Password) are used for authentication, while medical records are encrypted with random, unique keys.
* **Secure Credential Storage**: All sensitive credentials are hashed using SHA-256.
* **PIN Recovery System**: Patients can recover forgotten PINs without compromising encrypted data.
* **Multiple Record Types**: Support for different medical record types (blood tests, prescriptions, X-rays, etc.).
* **Data Persistence**: Patient and encryption data saved across sessions using JSON files.
* **Interactive Portals**: Separate Doctor and Patient portals with role-based functionality.

## Technologies Used
* **Python 3.x**
* **Cryptography Library**: AES-256 encryption using Fernet (symmetric encryption)
* **Hashlib**: SHA-256 for password/PIN hashing
* **JSON**: For data persistence (patients_data.json, encryption_keys.json)

## Project Structure
```
medical_project/
├── encryption.py              # File encryption/decryption module
├── authentication.py          # Patient authentication module
├── main_system.py            # Main interactive system
├── requirements.txt          # Python dependencies
├── patients_data.json        # Stored patient data (auto-generated)
└── encryption_keys.json      # Stored encryption keys (auto-generated)
```

## How to Run

1. **Install dependencies:**
```bash
   pip install -r requirements.txt
```

2. **Run the interactive system:**
```bash
   python main_system.py
```

## System Features

### Doctor Portal
* Register new patients with SSN, name, email, and password
* Create encrypted medical records from files
* View all registered patients
* Generate secure PINs for patient portal access

### Patient Portal
* Three-factor authentication (SSN + PIN + Password)
* View decrypted medical records (only your own)
* Reset forgotten PIN via email verification
* Secure logout

## Demo Workflow

The interactive system demonstrates:
1. **Patient Registration** - Hospital staff registers new patients
2. **Medical Record Creation** - Doctor encrypts patient files
3. **Patient Authentication** - Patient logs in with three factors
4. **Secure Record Access** - Patient views their decrypted records
5. **PIN Recovery** - Patient resets forgotten PIN without re-encryption
6. **Data Persistence** - All data saved across sessions

## Security Highlights

**Why This Design is Secure:**
* Authentication credentials can be changed without re-encrypting data
* Random encryption keys are not derivable from patient information
* Even if credentials are compromised, encrypted data remains secure
* PIN recovery doesn't expose encryption keys
* Each medical record encrypted with unique random key
* Follows HIPAA security guidelines for protecting healthcare data

**Security Architecture:**
```
Authentication (Login)          Encryption (Data Protection)
     ↓                                    ↓
SSN + PIN + Password           Random AES-256 Keys
     ↓                                    ↓
Can be changed                  Never changes
     ↓                                    ↓
Proves identity                 Protects files
```

## Key Security Principle

**Authentication ≠ Encryption**

When a patient forgets their PIN:
- New PIN is generated and stored
- Patient can log in with new PIN
- **Encryption keys remain unchanged**
- Patient can still access all medical records

This demonstrates that authentication credentials are completely separate from encryption keys, a critical security architecture principle.

## Team Members
* Meagan Alfaro
* Danny Colina  
* Agustin De La Guardia

## Course Information
* **Course**: CIS 5370
* **Instructor**: Ruimin Sun, KFSCIC, FIU
* **Semester**: Spring 2025
