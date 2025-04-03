import requests
import socket
import argparse
from colorama import Fore

requests.packages.urllib3.disable_warnings()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--url", "-u", type=str, required=True, help="URL to scan")
args = arg_parser.parse_args()


def check_web(url: str) -> str:
    s = requests.Session()
    r  = s.get(url, verify = False, timeout=10)
    if r.status_code == 200:
        return True
    else:
        return False

    
def check_ip(domain: str) -> str:
    if "https://" in domain:
        domain = domain.replace("https://", "")
    if "http://" in domain:
        domain = domain.replace("http://", "")
    if "www." in domain:
        domain = domain.replace("www.", "")
    if "https://www." in domain:
        domain = domain.replace("https://www.", "")
    if "http://www." in domain:
        domain = domain.replace("http://www.", "")
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror:
        return None
    
def port_scan(ip: int) -> int:
    ports = [80, 443, 8080, 8443]
    open_ports = []
    for port in ports:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        try:
            s.connect((ip, port))
            open_ports.append(port)
        except socket.error:
            pass
        s.close()
    return open_ports

def check_headers(domain: str) -> str:
    s = requests.Session()
    r = s.get(domain, verify=False, timeout=10)
    for k,v in r.headers.items():
        print(f"{k}: {Fore.MAGENTA}{v}{Fore.RESET}")

def check_robots(domain: str) -> str:
    s = requests.Session()
    r = s.get(f"{domain}/robots.txt", verify=False, timeout=10)
    if r.status_code == 200:
        return f"Robots: {domain}/robots.txt"
    else:
        return None

def check_sitemap(domain: str) -> str:
    s = requests.Session()
    r = s.get(f"{domain}/sitemap.xml", verify=False, timeout=10)
    if r.status_code == 200:
        return f"Sitemap: {domain}/sitemap.xml"
    else:
        return None
    

if __name__ == "__main__":
    if check_web(args.url):
        print(f"{Fore.GREEN}{args.url}:{Fore.WHITE} Is up!")
    ip = check_ip(args.url)
    if ip:
        print(f"{Fore.GREEN}IP: {ip}{Fore.WHITE}")
        open_ports = port_scan(ip)
        if open_ports:
            print(f"{Fore.GREEN}Open ports: {", ".join(map(str, open_ports))}{Fore.WHITE}")
    else:
        print(f"{Fore.RED}IP not found{Fore.WHITE}")
    
    check_headers(args.url)
    check_robots(args.url)
    check_sitemap(args.url)
        
        
        
        


        




        