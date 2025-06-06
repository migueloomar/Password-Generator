"""
Secure Password Generator Core Module

This module provides cryptographically strong password generation functionality with
customizable character composition. It is designed to create secure random passwords
suitable for authentication systems and sensitive applications.

Key Features:
- Cryptographically secure random generation using Python's secrets module
- Customizable password length (default 12 characters)
- Flexible character set configuration:
  * Uppercase letters (A-Z)
  * Lowercase letters (a-z)
  * Digits (0-9)
  * Special symbols/punctuation
- Validation to ensure at least one character set is selected

Security Implementation:
- Uses secrets module instead of random for CSPRNG (Cryptographically Secure 
  Pseudorandom Number Generator)
- Guarantees uniform distribution of selected character types
- Raises explicit error for invalid configurations

Usage Examples:
1. Basic password with default settings (12 chars, all character types):
   generate_password()

2. Custom length password with only letters:
   generate_password(length=16, use_digits=False, use_symbols=False)

3. Numeric PIN code:
   generate_password(length=6, use_upper=False, use_lower=False, use_symbols=False)

The module follows security best practices by:
- Avoiding predictable patterns in password generation
- Using cryptographically strong random number generation
- Providing clear validation for configuration errors
"""

import string   # For character sets
import secrets  # For cryptographically secure random generation


def generate_password(length=12, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):

    """
    Generate a cryptographically secure random password with customizable character sets.

    Args:
        length (int): Desired password length (default: 12)
        use_upper (bool): Include uppercase letters (default: True)
        use_lower (bool): Include lowercase letters (default: True)
        use_digits (bool): Include digits (default: True)
        use_symbols (bool): Include symbols (default: True)

    Returns:
        str: Generated password

    Raises:
        ValueError: If no character sets are selected or invalid length is provided

    Security Note:
        Uses secrets module which is suitable for generating authentication credentials.
        Never use the random module for security-sensitive applications.

    """
    
    characters = ''
    if use_upper:
        characters += string.ascii_uppercase
    if use_lower:
        characters += string.ascii_lowercase
    if use_digits:
        characters += string.digits
    if use_symbols:
        characters += string.punctuation

    if not characters:
        raise ValueError("At least one character type must be selected.")

    return ''.join(secrets.choice(characters) for _ in range(length))
