"""
Password Generator Application Entry Point
-----------------------------------------

This script serves as the main launch point for the Secure Password Generator application.
It initializes and starts the graphical user interface when executed directly.

Application Overview:
- Primary Purpose: Launch the password generator GUI application
- Execution Mode: Designed to be run as main script (not for import)
- Dependencies: Requires gui.py module in same package

Technical Implementation:
-----------------------------
1. Execution Flow:
   - Checks for direct script execution (__name__ == '__main__')
   - Imports launch_app() function from gui module
   - Initiates GUI mainloop via ttkbootstrap

2. Architecture Role:
   - Separation of concerns: Isolates launch logic
   - Provides clean entry point for:
     * Direct execution
     * Potential future packaging
     * Testing harnesses

3. Safety Features:
   - Prevents accidental execution when imported
   - Explicit namespace control
   - Minimal global namespace pollution

Usage Instructions:
-----------------------------
1. Direct Execution:
   $ python main.py

2. Programmatic Launch (alternative):
   >>> from gui import launch_app
   >>> launch_app()

3. Packaging Integration:
   - Suitable for pyinstaller/pex packaging
   - Works with setup.py console_scripts

Best Practices:
- Always execute from project root directory
- Maintain gui.py in same package
- Use virtual environment for dependencies

Example:
-----------------------------
# From command line:
python main.py

# Expected Result:
- Launches password generator window
- Initializes encrypted password vault
- Shows main application interface
"""

# Import the function that starts the GUI
from gui import launch_app

# Launch the app when this script is executed directly
if __name__ == '__main__':
    launch_app()
