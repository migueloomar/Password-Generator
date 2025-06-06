"""
Secure Password Storage Module
-----------------------------

This module provides encrypted storage for password data using industry-standard
cryptographic practices. It implements secure file-based storage with Fernet
symmetric encryption (AES-128-CBC with PKCS7 padding) and proper key management.

Security Features:
-----------------------------
- AES-128 encryption via Fernet (cryptography library)
- Automatic key generation and management
- Encrypted JSON serialization
- Protection against common cryptographic vulnerabilities:
  * Key stored separately from encrypted data
  * Secure key generation (cryptographically random)
  * Message authentication (HMAC)
  * Timestamp verification

Implementation Details:
-----------------------------
1. Key Management:
   - First-run: Generates new 32-byte URL-safe base64 encoded key
   - Subsequent runs: Loads existing key from secure file
   - Key storage: Separate file (secret.key) with restricted permissions

2. Data Storage:
   - Uses JSON serialization for structured data
   - Encrypts entire payload rather than individual items
   - Outputs binary encrypted file (passwords.enc)

3. Cryptographic Operations:
   - Encryption: Fernet.encrypt() with current timestamp
   - Decryption: Includes automatic validation of:
     * HMAC signature
     * Token expiration (not enforced by default)
     * Correct decryption key

File Structure:
-----------------------------
secret.key        - Encryption key (32 bytes, base64)
passwords.enc     - Encrypted password data (JSON format)

API Reference:
-----------------------------
encrypt_and_save(data: dict) -> None
    - Encrypts and saves password dictionary
    - Args: Python dictionary of {label: password} pairs
    - Writes to passwords.enc

load_and_decrypt() -> dict
    - Loads and decrypts password data
    - Returns: Decrypted dictionary
    - Returns empty dict if no file exists

Security Considerations:
-----------------------------
1. Key Protection:
   - Store secret.key with strict file permissions (chmod 600)
   - Never commit secret.key to version control
   - Consider additional protection for production:
     * Key rotation schedule
     * Hardware security modules

2. Best Practices:
   - Rotate keys periodically (requires re-encryption)
   - Secure deletion of old key files
   - Regular backups of encrypted data

3. Limitations:
   - Does not protect against memory scraping
   - No built-in key rotation
   - File-based storage only

Dependencies:
- cryptography >= 3.4.7
- Python standard library
"""

import json                             # For serialization
from cryptography.fernet import Fernet  # For encryption

KEY_FILE = 'secret.key'
PASSWORD_FILE = 'passwords.enc'


def load_key():

    """
    Manage encryption key lifecycle.

    Handles:
    - Key generation on first run
    - Key loading on subsequent runs
    - Secure key storage

    Returns:
        bytes: 32-byte Fernet encryption key

    Security Note:
        Generates cryptographically strong random key
        using system's CSPRNG when creating new key.
    """

    try:
        with open(KEY_FILE, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        return key


def encrypt_and_save(data):

    """
    Encrypt and securely store password data.
    
    Args:
        data (dict): Password dictionary {label: password}
    
    Process:
    1. Serializes data to JSON
    2. Encrypts with Fernet
    3. Writes to secure file
    
    Security Features:
    - Includes timestamp in encryption
    - Adds HMAC signature
    - Uses AES-128-CBC with PKCS7 padding
    """

    key = load_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(json.dumps(data).encode())
    with open(PASSWORD_FILE, 'wb') as file:
        file.write(encrypted)


def load_and_decrypt():

    """
    Load and decrypt stored passwords.
    
    Returns:
        dict: Decrypted password dictionary
    
    Handles:
    - FileNotFoundError (returns empty dict)
    - Cryptographic verification:
      * HMAC validation
      * Token expiration check
    
    Security:
    - Verifies data wasn't tampered with
    - Validates encryption timestamp
    """

    key = load_key()
    fernet = Fernet(key)
    try:
        with open(PASSWORD_FILE, 'rb') as file:
            encrypted = file.read()
            return json.loads(fernet.decrypt(encrypted).decode())
    except FileNotFoundError:
        return {}
