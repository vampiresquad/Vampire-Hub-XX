# Vampire_Hub_X.py (Main Script)

import hashlib
import sys # Import sys for exiting
from colorama import init, Fore, Style

# Import functions from our modules
from assets.banners import get_normal_banner
from assets.disclaimers import get_normal_disclaimer, get_admin_disclaimer
from modules.tool_utils import clear_screen, slow_print, get_user_input, check_and_install_dependencies, log_error # Import new functions
from modules.menus import normal_user_menu, admin_user_menu

# Initialize Colorama for cross-platform colored output
init(autoreset=True)

# --- Configuration ---
MASTER_PASSWORD_HASH = hashlib.sha256("VampireX".encode()).hexdigest()
ADMIN_PASSWORD_HASH = hashlib.sha256("SH404".encode()).hexdigest()

# --- Main Application Logic ---
def main():
    clear_screen()
    print(get_normal_banner())
    slow_print(f"{Fore.BLUE}Welcome to Vampire-Hub-X!{Style.RESET_ALL}", delay=0.03)

    # Step 1: Check and install dependencies
    if not check_and_install_dependencies():
        slow_print(f"{Fore.RED}Failed to install required dependencies. Exiting. Please fix the above errors and try again.{Style.RESET_ALL}", delay=0.02)
        sys.exit(1) # Exit if dependencies aren't met

    # Master Password Check
    while True:
        master_input = get_user_input(f"{Fore.CYAN}Enter Master Password: {Style.RESET_ALL}", hide_input=True).strip()
        if hashlib.sha256(master_input.encode()).hexdigest() == MASTER_PASSWORD_HASH:
            slow_print(f"{Fore.GREEN}Master Password Accepted!{Style.RESET_ALL}", delay=0.03)
            break
        else:
            slow_print(f"{Fore.RED}Incorrect Master Password. Please try again.{Style.RESET_ALL}", delay=0.03)

    # Mode Selection
    while True:
        clear_screen()
        slow_print(f"{Fore.YELLOW}Select Mode:{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1] Normal User Mode{Style.RESET_ALL}")
        print(f"{Fore.RED}[2] Admin Mode (Password Required){Style.RESET_ALL}")
        mode_choice = get_user_input(f"{Fore.BLUE}Enter your choice: {Style.RESET_ALL}").strip()

        if mode_choice == '1':
            print("\n" + "="*70)
            slow_print(get_normal_disclaimer(), delay=0.01)
            print("\n" + "="*70 + "\n")
            normal_user_menu()
            break
        elif mode_choice == '2':
            admin_input = get_user_input(f"{Fore.CYAN}Enter Admin Password: {Style.RESET_ALL}", hide_input=True).strip()
            if hashlib.sha256(admin_input.encode()).hexdigest() == ADMIN_PASSWORD_HASH:
                slow_print(f"{Fore.GREEN}Admin Password Accepted!{Style.RESET_ALL}", delay=0.03)
                print("\n" + "="*70)
                slow_print(get_admin_disclaimer(), delay=0.01)
                print("\n" + "="*70 + "\n")
                admin_user_menu()
                break
            else:
                slow_print(f"{Fore.RED}Incorrect Admin Password. Returning to mode selection.{Style.RESET_ALL}", delay=0.03)
        else:
            slow_print(f"{Fore.RED}Invalid mode choice. Please try again.{Style.RESET_ALL}", delay=0.03)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        slow_print(f"\n{Fore.YELLOW}Exiting Vampire-Hub-X. Goodbye!{Style.RESET_ALL}", delay=0.03)
    except Exception as e:
        error_message = f"An unexpected error occurred in main: {e}"
        slow_print(f"\n{Fore.RED}{error_message}{Style.RESET_ALL}", delay=0.01)
        log_error(error_message) # Log the error
        slow_print(f"{Fore.RED}Please report this to the developer for auto-fix analysis.{Style.RESET_ALL}", delay=0.01)
