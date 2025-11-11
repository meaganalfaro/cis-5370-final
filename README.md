# Secure Medical Record Sharing System
## Team Project - CIS 5370
### Project Overview
A secure medical record sharing system that demonstrates proper separation of authentication and encryption for protecting sensitive healthcare data.
Key Security Features

- Separate Authentication and Encryption: Patient credentials (SSN + PIN + Password) are used for authentication, while medical records are encrypted with random, unique keys.
- Secure Password Storage: All sensitive credentials are hashed using SHA-256.
- PIN Recovery System: Patients can recover forgotten PINs without compromising encrypted data.
- Multiple Record Types: Support for different medical record types (blood tests, prescriptions, X-rays, etc.).
- Access Logging: Tracks who accessed what records and when.

## Technologies Used

- Python 3.x
- Cryptography Library: AES-256 encryption using Fernet (symmetric encryption)
- Hashlib: SHA-256 for password/PIN hashing
- SQLite: For database storage (simulated with dictionaries in prototype)

## How to Run

### Install dependencies:

bash   pip install -r requirements.txt 

### Run the demo:

bash   python demo.py

### Run the interactive system:

bash   python main.py

## Demo Scenarios
The demo.py file demonstrates:

- Hospital registration of new patient
- Doctor creating encrypted medical records
- Patient logging in and viewing records
- PIN recovery process
- Attack simulation showing encryption protection

## Security Highlights
### Why This Design is Secure:

Authentication credentials can be changed without re-encrypting data
Random encryption keys are not derivable from patient information
Even if credentials are compromised, encrypted data remains secure
PIN recovery doesn't expose encryption keys
Follows HIPAA security guidelines for protecting healthcare data

## Team Members
Meagan Alfaro, Danny Colina, Agustin De La Guardia
## Course Information

Course: CIS 5370
Instructor: Ruimin Sun
Semester: Spring 2025
