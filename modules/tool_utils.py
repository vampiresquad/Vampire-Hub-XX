# modules/tool_utils.py

import os
import sys
import time
import getpass
import subprocess # Import subprocess for running shell commands
from colorama import Fore, Style, init # Import init here as well

# Initialize Colorama for cross-platform colored output
init(autoreset=True)

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.01):
    """Prints text with a slow writing effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    sys.stdout.write('\n')
    sys.stdout.flush()

def display_section_header(title):
    """Displays a colored section header."""
    print(f"\n{Fore.CYAN}--- {title} ---{Style.RESET_ALL}\n")

def press_enter_to_continue():
    """Waits for the user to press Enter to continue."""
    input(f"\n{Fore.LIGHTBLACK_EX}Press Enter to continue...{Style.RESET_ALL}")

def get_user_input(prompt, hide_input=False):
    """
    Gets input from the user.
    If hide_input is True, the input will not be echoed on the screen (for passwords).
    """
    if hide_input:
        return getpass.getpass(prompt=prompt)
    else:
        return input(prompt)

def check_and_install_dependencies():
    """
    Checks for and automatically installs required Python packages from requirements.txt.
    """
    slow_print(f"{Fore.YELLOW}Checking for required dependencies...{Style.RESET_ALL}", delay=0.02)
    requirements_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requirements.txt') # Adjust path for requirements.txt

    if not os.path.exists(requirements_path):
        slow_print(f"{Fore.RED}Error: 'requirements.txt' not found at {requirements_path}. Cannot auto-install dependencies.{Style.RESET_ALL}", delay=0.02)
        return False

    try:
        # Using pip to install from requirements.txt
        process = subprocess.run([sys.executable, "-m", "pip", "install", "-r", requirements_path],
                                 capture_output=True, text=True, check=True)
        slow_print(f"{Fore.GREEN}All dependencies checked/installed successfully!{Style.RESET_ALL}", delay=0.02)
        # print(process.stdout) # Uncomment for detailed output if needed
        return True
    except subprocess.CalledProcessError as e:
        slow_print(f"{Fore.RED}Error installing dependencies:{Style.RESET_ALL}", delay=0.02)
        slow_print(f"{Fore.RED}STDOUT: {e.stdout}{Style.RESET_ALL}", delay=0.005)
        slow_print(f"{Fore.RED}STDERR: {e.stderr}{Style.RESET_ALL}", delay=0.005)
        slow_print(f"{Fore.RED}Please ensure pip is installed and accessible in your PATH. You might need to run as administrator/sudo.{Style.RESET_ALL}", delay=0.02)
        return False
    except FileNotFoundError:
        slow_print(f"{Fore.RED}Error: 'pip' command not found. Please ensure Python and pip are correctly installed.{Style.RESET_ALL}", delay=0.02)
        return False
    except Exception as e:
        slow_print(f"{Fore.RED}An unexpected error occurred during dependency check/install: {e}{Style.RESET_ALL}", delay=0.02)
        return False

# Function to write errors to a log file
def log_error(error_message):
    log_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'Vampire_Hub_X.log')
    try:
        with open(log_file_path, 'a') as f:
            f.write(f"[{time.ctime()}] ERROR: {error_message}\n")
        slow_print(f"{Fore.YELLOW}Error logged to {log_file_path}{Style.RESET_ALL}", delay=0.01)
    except Exception as e:
        print(f"{Fore.RED}Failed to write to log file: {e}{Style.RESET_ALL}")
