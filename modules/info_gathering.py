# modules/info_gathering.py

import socket
import whois
import dns.resolver
import requests
from colorama import Fore, Style
from modules.tool_utils import slow_print, display_section_header, press_enter_to_continue, get_user_input, log_error

# --- General Error Handling Function for Modules ---
def handle_module_error(e, module_name, function_name, target=None):
    error_message = f"Error in {module_name} -> {function_name}"
    if target:
        error_message += f" for target '{target}'"
    error_message += f": {e}"

    slow_print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}", delay=0.01)
    slow_print(f"{Fore.RED}This issue has been logged. Please ensure your inputs are valid and your internet connection is stable.{Style.RESET_ALL}", delay=0.01)
    log_error(error_message)

def whois_lookup():
    display_section_header("Whois Lookup")
    domain = get_user_input(f"{Fore.CYAN}Enter target domain (e.g., example.com): {Style.RESET_ALL}").strip()
    if not domain:
        slow_print(f"{Fore.RED}Domain cannot be empty.{Style.RESET_ALL}")
        press_enter_to_continue()
        return

    try:
        slow_print(f"{Fore.YELLOW}Performing WHOIS lookup for {domain}...{Style.RESET_ALL}", delay=0.01)
        w = whois.whois(domain)
        slow_print(f"{Fore.GREEN}Whois Information for {domain}:{Style.RESET_ALL}")
        # Print relevant WHOIS details
        if isinstance(w, dict): # Ensure it's a dictionary before iterating
            for key, value in w.items():
                if isinstance(value, list):
                    slow_print(f"{Fore.YELLOW}{key.replace('_', ' ').title()}: {', '.join(map(str, value))}{Style.RESET_ALL}", delay=0.005)
                else:
                    slow_print(f"{Fore.YELLOW}{key.replace('_', ' ').title()}: {value}{Style.RESET_ALL}", delay=0.005)
        else:
            slow_print(f"{Fore.YELLOW}No detailed WHOIS data found or format is unexpected.{Style.RESET_ALL}", delay=0.01)

    except whois.parser.PywhoisError as e:
        slow_print(f"{Fore.RED}WHOIS lookup failed for {domain}: {e}. This usually means the domain is not registered or WHOIS server is down.{Style.RESET_ALL}", delay=0.01)
        log_error(f"WHOIS Lookup failed for {domain}: {e}")
    except Exception as e:
        handle_module_error(e, "Information Gathering", "whois_lookup", domain)
    finally:
        press_enter_to_continue()

def dns_lookup():
    display_section_header("DNS Lookup (A, MX, NS)")
    domain = get_user_input(f"{Fore.CYAN}Enter target domain (e.g., example.com): {Style.RESET_ALL}").strip()
    if not domain:
        slow_print(f"{Fore.RED}Domain cannot be empty.{Style.RESET_ALL}")
        press_enter_to_continue()
        return

    record_types = ['A', 'MX', 'NS']
    found_records = False
    for rtype in record_types:
        try:
            slow_print(f"{Fore.YELLOW}Attempting to resolve {rtype} records for {domain}...{Style.RESET_ALL}", delay=0.01)
            answers = dns.resolver.resolve(domain, rtype)
            slow_print(f"\n{Fore.GREEN}{rtype} Records for {domain}:{Style.RESET_ALL}")
            for rdata in answers:
                slow_print(f"{Fore.YELLOW}- {rdata}{Style.RESET_ALL}", delay=0.005)
                found_records = True
        except dns.resolver.NoAnswer:
            slow_print(f"{Fore.YELLOW}No {rtype} record found for {domain}.{Style.RESET_ALL}", delay=0.005)
        except dns.resolver.NXDOMAIN:
            slow_print(f"{Fore.RED}Domain '{domain}' does not exist or cannot be resolved.{Style.RESET_ALL}", delay=0.01)
            found_records = False # Mark as not found to avoid "No records found"
            break # Exit if domain doesn't exist for any record type
        except dns.resolver.Timeout:
            slow_print(f"{Fore.RED}DNS query timed out for {rtype} record. Check your network or DNS server.{Style.RESET_ALL}", delay=0.01)
            log_error(f"DNS lookup timeout for {domain} ({rtype}): {e}")
        except Exception as e:
            handle_module_error(e, "Information Gathering", "dns_lookup", domain)
            break # Break on general error to avoid multiple error messages for same domain
    
    if not found_records and "NXDOMAIN" not in str(sys.exc_info()[1]): # Only if no records were found AND it's not a non-existent domain
        slow_print(f"{Fore.YELLOW}No DNS records found for {domain} across specified types.{Style.RESET_ALL}", delay=0.01)
    
    press_enter_to_continue()


def ip_geolocation():
    display_section_header("IP Geolocation")
    target = get_user_input(f"{Fore.CYAN}Enter target IP address or Domain (e.g., 8.8.8.8 or example.com): {Style.RESET_ALL}").strip()
    if not target:
        slow_print(f"{Fore.RED}Target cannot be empty.{Style.RESET_ALL}")
        press_enter_to_continue()
        return

    ip_address = target
    try:
        # Resolve domain to IP if domain is given
        if not target.replace('.', '').isdigit(): # Simple check if it's not purely an IP
            slow_print(f"{Fore.YELLOW}Resolving domain to IP address...{Style.RESET_ALL}", delay=0.01)
            ip_address = socket.gethostbyname(target)
            slow_print(f"{Fore.GREEN}Resolved {target} to IP: {ip_address}{Style.RESET_ALL}", delay=0.01)

        slow_print(f"{Fore.YELLOW}Performing IP Geolocation for {ip_address}...{Style.RESET_ALL}", delay=0.01)
        # Using ip-api.com for free IP geolocation (rate limited for free tier)
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query")
        data = response.json()

        if data.get('status') == 'success':
            slow_print(f"\n{Fore.GREEN}Geolocation Information for {ip_address}:{Style.RESET_ALL}")
            for key, value in data.items():
                if key not in ['status', 'query']:
                    slow_print(f"{Fore.YELLOW}{key.replace('_', ' ').title()}: {value}{Style.RESET_ALL}", delay=0.005)
        else:
            slow_print(f"{Fore.RED}Failed to get geolocation for {ip_address}. Error: {data.get('message', 'Unknown Error')}{Style.RESET_ALL}", delay=0.01)
            if "private range" in data.get('message', '').lower():
                slow_print(f"{Fore.YELLOW}Note: This might be a private IP address, which cannot be geolocated publicly.{Style.RESET_ALL}", delay=0.01)
            elif "rate limit" in data.get('message', '').lower():
                slow_print(f"{Fore.YELLOW}Note: You might have hit the API rate limit for ip-api.com. Try again later or use a different service.{Style.RESET_ALL}", delay=0.01)
            log_error(f"Geolocation failed for {ip_address}: {data.get('message', 'Unknown Error')}")

    except requests.exceptions.ConnectionError:
        slow_print(f"{Fore.RED}Network connection error. Please check your internet connection.{Style.RESET_ALL}", delay=0.01)
        log_error(f"Network error during Geolocation for {target}")
    except requests.exceptions.Timeout:
        slow_print(f"{Fore.RED}Geolocation request timed out. The server might be slow or unreachable.{Style.RESET_ALL}", delay=0.01)
        log_error(f"Geolocation timeout for {target}")
    except socket.gaierror:
        slow_print(f"{Fore.RED}Could not resolve domain: '{target}'. Please check the domain name.{Style.RESET_ALL}", delay=0.01)
        log_error(f"Domain resolution failed for {target} during geolocation.")
    except Exception as e:
        handle_module_error(e, "Information Gathering", "ip_geolocation", target)
    finally:
        press_enter_to_continue()
