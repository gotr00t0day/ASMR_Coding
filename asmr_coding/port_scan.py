import requests
import socket
import argparse
from colorama import Fore

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d", "--domain", type=str, help="The domain to scan")
arg_parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose mode")
args = arg_parser.parse_args()

if not args.domain:
    print(f"{Fore.RED}[-] Error: Please provide a domain")
    exit()


# Get the IP from a domain

def get_ip(domain: str) -> str:
    if "https://" in domain:
        domain = domain.replace("https://", "")
    if "http://" in domain:
        domain = domain.replace("http://", "")
    if "www." in domain:
        domain = domain.replace("www.", "")
    if "http://www." in domain:
        domain = domain.replace("http://www.", "")
    if "https://www." in domain:
        domain = domain.replace("https://www.", "")
    s = requests.Session()
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        return None
    
# Port scan the target

def port_scan(ip: int) -> str:
    ports = [80, 8080, 443, 8443]
    open_ports = []
    
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)  # Add timeout to prevent hanging
        
        try:
            s.connect((ip, port))
            open_ports.append(port)
        except Exception as e:
            if args.verbose: 
                print(f"{Fore.YELLOW}Port {port}: {e}{Fore.RESET}")
        finally:
            s.close()
    
    return ",".join(map(str, open_ports))

if __name__ == "__main__":
    if args.domain:
        ip = get_ip(args.domain)
        print(port_scan(ip))
        

    



