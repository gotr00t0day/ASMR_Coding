import requests
from bs4 import BeautifulSoup
from colorama import Fore
from urllib.parse import urljoin
import argparse

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("-d", "--domain", type=str, help="The domain to crawl")
args = arg_parser.parse_args()

requests.packages.urllib3.disable_warnings()

def get_links(domain: str) -> str:
    try:
        s = requests.Session()
        r = s.get(domain, verify=False, timeout=5)
        soup = BeautifulSoup(r.text, "html.parser")
        links = set()
        for tags in soup.find_all("a", href=True):
            href = tags.get("href")
            link = urljoin(domain, href)
            if ";" in link:
                pass
            else:
                links.add(link.strip())
        return links
    except Exception as e:
        print(f"{Fore.RED}[-] Error: {e}")
        return set()

if __name__ == "__main__":
    if not args.domain:
        print(f"{Fore.RED}[-] Error: Please provide a domain")
        exit()
    page_links = get_links(args.domain)
    print(f"We have found {len(page_links)} Links\n")
    for page_link in page_links:
        print(page_link)
