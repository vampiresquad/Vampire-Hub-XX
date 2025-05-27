# modules/menus.py (Updated)

import time
from colorama import Fore, Style
from assets.banners import get_normal_banner, get_admin_banner
from assets.disclaimers import get_normal_disclaimer, get_admin_disclaimer
from modules.tool_utils import clear_screen, slow_print, display_section_header, press_enter_to_continue, get_user_input
from modules.info_gathering import whois_lookup, dns_lookup, ip_geolocation
from modules.ddos_attacks import start_syn_flood, start_http_flood # Import DDoS functions

# --- Information Gathering Menu ---
def run_info_gathering_menu(is_admin=False):
    while True:
        clear_screen()
        display_section_header("Information Gathering Module")
        if is_admin:
            print(f"{Fore.MAGENTA}--- Admin IG Options ---{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[1] Whois Lookup (Advanced){Style.RESET_ALL}")
            print(f"{Fore.GREEN}[2] DNS Lookup (Advanced){Style.RESET_ALL}")
            print(f"{Fore.GREEN}[3] IP Geolocation (Advanced){Style.RESET_ALL}")
            print(f"{Fore.GREEN}[4] Port Scanning (Requires Nmap) (Under Development){Style.RESET_ALL}")
            print(f"{Fore.GREEN}[5] Subdomain Enumeration (Under Development){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[B] Back to Main Menu{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}--- Normal IG Options ---{Style.RESET_ALL}")
            print(f"{Fore.GREEN}[1] Whois Lookup (Limited){Style.RESET_ALL}")
            print(f"{Fore.GREEN}[2] DNS Lookup (Limited){Style.RESET_ALL}")
            print(f"{Fore.GREEN}[3] IP Geolocation (Limited){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[B] Back to Main Menu{Style.RESET_ALL}")

        choice = get_user_input(f"{Fore.BLUE}Enter your choice: {Style.RESET_ALL}").strip().upper()

        if choice == '1':
            whois_lookup()
        elif choice == '2':
            dns_lookup()
        elif choice == '3':
            ip_geolocation()
        elif is_admin and choice == '4':
            slow_print(f"{Fore.YELLOW}Port Scanning is under development. It will require Nmap to be installed on your system.{Style.RESET_ALL}")
            press_enter_to_continue()
        elif is_admin and choice == '5':
            slow_print(f"{Fore.YELLOW}Subdomain Enumeration is under development.{Style.RESET_ALL}")
            press_enter_to_continue()
        elif choice == 'B':
            break
        else:
            slow_print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1.5)

# --- DDoS Attack Menu ---
def run_ddos_attack_menu(is_admin=False):
    while True:
        clear_screen()
        display_section_header("DDoS Attack Module")
        slow_print(f"{Fore.RED}WARNING: This module contains powerful tools. Use ONLY in authorized environments.{Style.RESET_ALL}")
        if is_admin:
            print(f"{Fore.MAGENTA}--- Admin DDoS Options ---{Style.RESET_ALL}")
            print(f"{Fore.RED}[1] SYN Flood Attack{Style.RESET_ALL}")
            print(f"{Fore.RED}[2] HTTP Flood Attack{Style.RESET_ALL}")
            print(f"{Fore.RED}[3] UDP Flood Attack (Under Development){Style.RESET_ALL}")
            print(f"{Fore.YELLOW}[B] Back to Main Menu{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}--- Normal DDoS Options ---{Style.RESET_ALL}")
            slow_print(f"{Fore.YELLOW}DDoS options are severely limited in Normal Mode due to high risk.{Style.RESET_ALL}")
            print(f"{Fore.RED}[1] Limited HTTP Flood (Basic){Style.RESET_ALL}") # Only basic HTTP flood for normal
            print(f"{Fore.YELLOW}[B] Back to Main Menu{Style.RESET_ALL}")
        
        choice = get_user_input(f"{Fore.BLUE}Enter your choice: {Style.RESET_ALL}").strip().upper()

        if choice == '1':
            if is_admin:
                start_syn_flood() # Admin gets SYN Flood
            else:
                slow_print(f"{Fore.YELLOW}Executing Limited HTTP Flood...{Style.RESET_ALL}")
                # For normal mode, we can provide a very basic, non-threatening HTTP flood
                # Or simply block it and warn them. For now, block.
                slow_print(f"{Fore.RED}Limited HTTP Flood is under development, or restricted in Normal Mode.{Style.RESET_ALL}")
                press_enter_to_continue()
        elif choice == '2':
            if is_admin:
                start_http_flood() # Admin gets HTTP Flood
            else:
                slow_print(f"{Fore.RED}This option is restricted to Admin Mode.{Style.RESET_ALL}")
                press_enter_to_continue()
        elif is_admin and choice == '3':
            slow_print(f"{Fore.YELLOW}UDP Flood Attack is under development.{Style.RESET_ALL}")
            press_enter_to_continue()
        elif choice == 'B':
            break
        else:
            slow_print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1.5)


# Update existing main menu calls to use the new DDoS menu
def normal_user_menu():
    while True:
        clear_screen()
        print(get_normal_banner())
        print(f"{Fore.CYAN}--- Normal User Mode Menu ---{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1] Information Gathering (Limited){Style.RESET_ALL}")
        print(f"{Fore.RED}[2] DDoS Attack (Limited & Highly Restricted){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[3] Exit{Style.RESET_ALL}")

        choice = get_user_input(f"{Fore.BLUE}Enter your choice: {Style.RESET_ALL}").strip()

        if choice == '1':
            run_info_gathering_menu(is_admin=False)
        elif choice == '2':
            run_ddos_attack_menu(is_admin=False) # Call the new DDoS menu
        elif choice == '3':
            slow_print(f"{Fore.YELLOW}Exiting Vampire-Hub-X Normal Mode. Goodbye!{Style.RESET_ALL}")
            break
        else:
            slow_print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1.5)

def admin_user_menu():
    while True:
        clear_screen()
        print(get_admin_banner())
        print(f"{Fore.MAGENTA}--- Admin Mode Menu ---{Style.RESET_ALL}")
        print(f"{Fore.GREEN}[1] Advanced Information Gathering{Style.RESET_ALL}")
        print(f"{Fore.RED}[2] Powerful DDoS Attack Options{Style.RESET_ALL}")
        print(f"{Fore.CYAN}[3] Tool Maintenance & Configuration (Under Development){Style.RESET_ALL}")
        print(f"{Fore.YELLOW}[4] Exit{Style.RESET_ALL}")

        choice = get_user_input(f"{Fore.BLUE}Enter your choice: {Style.RESET_ALL}").strip()

        if choice == '1':
            run_info_gathering_menu(is_admin=True)
        elif choice == '2':
            run_ddos_attack_menu(is_admin=True) # Call the new DDoS menu for admin
        elif choice == '3':
            slow_print(f"{Fore.YELLOW}Entering Tool Maintenance... (Under Development){Style.RESET_ALL}")
            press_enter_to_continue()
        elif choice == '4':
            slow_print(f"{Fore.YELLOW}Exiting Admin Mode. Goodbye!{Style.RESET_ALL}")
            break
        else:
            slow_print(f"{Fore.RED}Invalid choice. Please try again.{Style.RESET_ALL}")
            time.sleep(1.5)
