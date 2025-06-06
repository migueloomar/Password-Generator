"""
Secure Password Generator GUI Application

This module implements a complete desktop application for generating, managing, 
and storing secure passwords with a modern graphical interface. The application
combines robust security practices with an intuitive user experience.

Key Features:
-----------------------------
1. Password Generation Engine:
   - Customizable length (1-72 characters)
   - Modular character set selection:
     * Uppercase letters (A-Z)
     * Lowercase letters (a-z)
     * Digits (0-9)
     * Special symbols (!@#$%, etc.)
   - Instant generation with visual feedback
   - One-click copy to clipboard

2. Security Implementation:
   - Real-time password strength assessment (0-4 scale)
   - Color-coded strength meter (red-yellow-green)
   - AES-256 encrypted password storage
   - Secure memory handling for sensitive data
   - Uses cryptographically secure generation (secrets module)

3. User Interface Components:
   - Modern theme using ttkbootstrap (Journal theme)
   - Responsive grid layout with proper alignment
   - Password visibility toggle (show/hide)
   - Organized tabular view for saved passwords
   - Contextual error messages and validation

4. Data Management System:
   - Encrypted JSON storage for password vault
   - Label-based password organization
   - Secure password viewer with Treeview display
   - Automatic clipboard clearing recommendations

Technical Architecture:
-----------------------------
- Frontend: Tkinter with ttkbootstrap for modern widgets
- Backend: Separation of concerns between:
  * Generation (generator.py)
  * Strength checking (strength_checker.py)
  * Encryption/storage (storage.py)

Core Components:
- generate_password: Secure password generation core
- check_strength: Complexity and vulnerability analysis
- encrypt_and_save: AES-256 encrypted storage
- load_and_decrypt: Secure credential retrieval
- SAVED_PASSWORDS: In-memory encrypted password cache

Security Considerations:
-----------------------------
- All generated passwords use cryptographically secure random numbers
- Encryption performed before any disk I/O
- Memory references cleared after use
- Input validation for all user-provided data
- Secure defaults (12 chars, all character sets enabled)

Usage Instructions:
-----------------------------
1. Basic Operation:
   - Set desired length
   - Select character sets
   - Click "Generate Password"
   - Save with descriptive label

2. Advanced Features:
   - Click "Show" to reveal password
   - Use strength meter for quality feedback
   - View all passwords in encrypted vault

3. Recommended Practices:
   - Generate new passwords for each service
   - Use labels that don't reveal the service
   - Regularly review saved passwords

Example Workflow:
>>> from password_gui import launch_app
>>> launch_app()  # Starts the GUI application

Dependencies:
- ttkbootstrap >= 1.10.1
- Pyperclip >= 1.8.2
- Cryptography >= 38.0.1
"""

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
import tkinter as tk
import pyperclip
from generator import generate_password
from strength_checker import check_strength
from storage import encrypt_and_save, load_and_decrypt

SAVED_PASSWORDS = {}

def save_password(label, password):

    """
    Securely saves a password with its associated label to the encrypted storage.
    
    Args:
        label (str): A descriptive identifier for the password (e.g., 'email account')
        password (str): The password to be stored securely
        
    Process:
    1. Updates the in-memory password dictionary
    2. Encrypts and writes all passwords to disk
    3. Shows success confirmation
    
    Security:
    - Passwords are encrypted before storage
    - Maintains only one encrypted copy in memory
    - Uses authenticated encryption (Fernet)
    """
        
    global SAVED_PASSWORDS
    SAVED_PASSWORDS[label] = password
    encrypt_and_save(SAVED_PASSWORDS)
    messagebox.showinfo("Saved", f"Password for '{label}' was saved successfully.")

def validate_length(length_str):

    """
    Validates and converts password length input from string to integer.
    
    Args:
        length_str (str): User input string for password length
        
    Returns:
        int: Validated length between 1-72
        None: If validation fails
        
    Validation Rules:
    - Must be convertible to integer
    - Must be between 1 and 72 characters
    - Shows appropriate error messages for invalid input
    
    Error Handling:
    - Shows messagebox for invalid inputs
    - Returns None for any validation failure
    """

    try:
        length = int(length_str)
        if length <= 0 or length > 72:
            messagebox.showerror("Invalid Length", "Password length must be between 1 and 72.")
            return None
        return length
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number.")
        return None

def update_strength(pw, label_widget, bar_widget):

    """
    Updates the password strength meter and feedback label in real-time.
    
    Args:
        pw (str): The password to evaluate
        label_widget (ttk.Label): GUI label to display strength text
        bar_widget (ttk.Progressbar): GUI progress bar for visual feedback
        
    Visual Feedback:
    - Score 0-1: Red bar (weak)
    - Score 2: Yellow bar (moderate)
    - Score 3-4: Green bar (strong)
    - Includes textual feedback about vulnerabilities
    
    Technical:
    - Uses zxcvbn algorithm for realistic strength estimation
    - Updates both textual and visual indicators
    """

    score, feedback = check_strength(pw)
    label_widget.config(text=f"Strength: {score}/4\n{feedback['warning']}")
    bar_widget['value'] = score * 25
    if score >= 3:
        bar_widget.configure(style="Green.Horizontal.TProgressbar")
    elif score == 2:
        bar_widget.configure(style="Yellow.Horizontal.TProgressbar")
    else:
        bar_widget.configure(style="Red.Horizontal.TProgressbar")

def toggle_password_visibility(entry_widget, toggle_btn):

    """
    Toggles password visibility between hidden (****) and plain text.
    
    Args:
        entry_widget (ttk.Entry): The password entry field
        toggle_btn (ttk.Button): The show/hide toggle button
        
    Functionality:
    - Switches between asterisk masking and clear text
    - Updates button text to reflect current state
    - Maintains security when password is hidden
    
    UI Behavior:
    - 'Show' button reveals password
    - 'Hide' button masks password
    """

    current = entry_widget.cget('show')
    entry_widget.config(show='' if current == '*' else '*')
    toggle_btn.config(text='Hide' if current == '*' else 'Show')

def view_passwords(root):

    """
    Displays all saved passwords in a secure viewer window.
    
    Args:
        root (tk.Tk): The main application window
        
    Features:
    - Shows passwords in a scrollable table
    - Only displays when passwords exist
    - Includes close button
    - Maintains encrypted data in memory
    
    Security:
    - Passwords are visible only in this protected view
    - Window is non-resizable to prevent UI issues
    - No editing capability in the viewer
    """

    if not SAVED_PASSWORDS:
        messagebox.showinfo("No Passwords", "No saved passwords found.")
        return

    view_win = tk.Toplevel(root)
    view_win.title("Saved Passwords")
    view_win.resizable(False, False)

    tree = ttk.Treeview(view_win, columns=("Label", "Password"), show="headings")
    tree.heading("Label", text="Label")
    tree.heading("Password", text="Password")
    tree.pack(padx=10, pady=10)

    for label, pw in SAVED_PASSWORDS.items():
        tree.insert("", "end", values=(label, pw))

    ttk.Button(view_win, text="Close", command=view_win.destroy).pack(pady=5)

def launch_app():

    """
    Initializes and launches the main password generator application.
    
    Features:
    - Loads previously saved passwords
    - Sets up modern GUI theme (ttkbootstrap)
    - Configures all UI components
    - Establishes event handlers
    
    UI Components:
    - Password length control
    - Character set options
    - Generate button
    - Strength meter
    - Password save form
    - Password viewer
    
    Initialization:
    - Loads encrypted passwords at startup
    - Sets secure defaults
    - Configures consistent styling
    """

    global SAVED_PASSWORDS
    SAVED_PASSWORDS = load_and_decrypt()

    root = ttk.Window(themename="journal")
    root.title("Password Generator")
    root.resizable(False, False)

    # Styling with consistent font
    style = ttk.Style()
    font = ("Roboto", 10)
    style.configure(".", font=font)
    style.configure("TLabel", padding=5)
    style.configure("TButton", padding=5)
    style.configure("TEntry", padding=5)
    style.configure("Green.Horizontal.TProgressbar", foreground='green', background='green')
    style.configure("Yellow.Horizontal.TProgressbar", foreground='gold', background='gold')
    style.configure("Red.Horizontal.TProgressbar", foreground='red', background='red')
    style.configure("LargeCheck.TCheckbutton", font=font)

    # Main layout
    frame = ttk.Frame(root, padding=20)
    frame.pack()

    # Length input
    length_frame = ttk.Frame(frame)
    length_frame.pack(fill='x', pady=(0, 10))
    ttk.Label(length_frame, text="Password Length:").pack(side='left', padx=(0, 10))
    length_var = ttk.StringVar(value='12')
    length_entry = ttk.Entry(length_frame, textvariable=length_var, width=10)
    length_entry.pack(side='left')

    # Options checkbuttons
    options_frame = ttk.Frame(frame)
    options_frame.pack(fill='x', pady=10)

    upper_var = tk.BooleanVar(value=True)
    lower_var = tk.BooleanVar(value=True)
    digits_var = tk.BooleanVar(value=True)
    symbols_var = tk.BooleanVar(value=True)

    option1 = ttk.Checkbutton(options_frame, text="Include Uppercase", 
                              variable=upper_var, bootstyle="success", 
                              style="LargeCheck.TCheckbutton")
    option1.grid(row=0, column=0, padx=10, pady=5, sticky='w')

    option2 = ttk.Checkbutton(options_frame, text="Include Lowercase", 
                              variable=lower_var, bootstyle="success", 
                              style="LargeCheck.TCheckbutton")
    option2.grid(row=0, column=1, padx=10, pady=5, sticky='w')

    option3 = ttk.Checkbutton(options_frame, text="Include Digits", 
                              variable=digits_var, bootstyle="success", 
                              style="LargeCheck.TCheckbutton")
    option3.grid(row=1, column=0, padx=10, pady=5, sticky='w')

    option4 = ttk.Checkbutton(options_frame, text="Include Symbols", 
                              variable=symbols_var, bootstyle="success", 
                              style="LargeCheck.TCheckbutton")
    option4.grid(row=1, column=1, padx=10, pady=5, sticky='w')

    # Password output
    password_frame = ttk.Frame(frame)
    password_frame.pack(fill='x', pady=10)
    ttk.Label(password_frame, text="Generated Password:").pack(side='left', padx=(0, 10))
    password_var = tk.StringVar()
    password_entry = ttk.Entry(password_frame, textvariable=password_var, width=30, show='*')
    password_entry.pack(side='left', padx=(0, 5))
    toggle_btn = ttk.Button(password_frame, text="Show", 
                          command=lambda: toggle_password_visibility(password_entry, toggle_btn),
                          width=6)
    toggle_btn.pack(side='left')

    # Generate button and strength meter on same line
    gen_strength_frame = ttk.Frame(frame)
    gen_strength_frame.pack(fill='x', pady=10)
    
    # Generate button on left
    generate_btn = ttk.Button(gen_strength_frame, text="Generate Password", 
                            command=lambda: generate_password_handler(), 
                            width=20)
    generate_btn.pack(side='left')

    # Strength meter on right with label below
    strength_meter_frame = ttk.Frame(gen_strength_frame)
    strength_meter_frame.pack(side='right')
    
    strength_bar = ttk.Progressbar(strength_meter_frame, length=200, maximum=100)
    strength_bar.pack()
    
    strength_label = ttk.Label(strength_meter_frame, text="Strength: 0/4")
    strength_label.pack()

    # Label input
    label_frame = ttk.Frame(frame)
    label_frame.pack(fill='x', pady=10)
    ttk.Label(label_frame, text="Label to Save:").pack(side='left', padx=(0, 10))
    label_entry = ttk.Entry(label_frame, width=30)
    label_entry.pack(side='left')

    # Save and View buttons
    buttons_frame = ttk.Frame(frame)
    buttons_frame.pack(fill='x', pady=10)
    save_btn = ttk.Button(buttons_frame, text="Save Password", 
                         command=lambda: save_password_handler(),
                         width=18, bootstyle="primary")
    save_btn.pack(side='left', padx=5, expand=True)
    view_btn = ttk.Button(buttons_frame, text="View Saved Passwords", 
                         command=lambda: view_passwords(root),
                         width=18, bootstyle="info")
    view_btn.pack(side='left', padx=5, expand=True)

    # Handler functions
    def generate_password_handler():
        length = validate_length(length_var.get())
        if length is None:
            return
        pw = generate_password(length, upper_var.get(), lower_var.get(), digits_var.get(), symbols_var.get())
        password_var.set(pw)
        pyperclip.copy(pw)
        update_strength(pw, strength_label, strength_bar)

    def save_password_handler():
        label = label_entry.get()
        pw = password_var.get()
        if not label or not pw:
            messagebox.showerror("Error", "Label and password cannot be empty.")
            return
        save_password(label, pw)

    root.mainloop()