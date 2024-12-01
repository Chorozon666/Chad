import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import init, Fore
import os
import sys

init(autoreset=True)

chromedriver_path = "( ADD YOUR WEBDRIVER PATH )"

if not os.path.exists(chromedriver_path):
    raise FileNotFoundError(f"Chromedriver not found at: {chromedriver_path}")
if not os.access(chromedriver_path, os.X_OK):
    raise PermissionError(f"Chromedriver is not executable: {chromedriver_path}")

user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.992.50 Safari/537.36"
]

def get_chrome_options(user_agent):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument(f"user-agent={user_agent}")
    return chrome_options

user_agent = random.choice(user_agents)
chrome_options = get_chrome_options(user_agent)
service = Service(chromedriver_path)
driver = webdriver.Chrome(service=service, options=chrome_options)

queries = [
    'inurl:/wp-content/uploads/ filetype:sql',
    'inurl:/wp-content/uploads/ ext:sql | ext:txt',
    'inurl:/wp-content/uploads/ "sql dump"',
    'inurl:/wp-content/uploads/ ext:txt'
]

max_pages = 10
max_urls = 500
max_retries = 3

scanned_urls = set()
valid_urls = []

queries_searched = 0
total_scanned = 0
total_valid = 0

first_url_scanned = False

def print_stats():
    sys.stdout.write(Fore.GREEN + f"\n--- Progress ---\n")
    sys.stdout.write(Fore.GREEN + f"Total Queries Searched: {queries_searched}\n")
    sys.stdout.write(Fore.GREEN + f"Total URLs Scanned: {total_scanned}\n")
    sys.stdout.write(Fore.GREEN + f"Total Valid URLs Found: {total_valid}\n")
    sys.stdout.write(Fore.GREEN + f"Valid URLs: {len(valid_urls)}\n")
    sys.stdout.flush()

def check_if_blocked():
    try:
        recaptcha_frame = driver.find_elements(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
        if recaptcha_frame:
            print(Fore.RED + "CAPTCHA detected! Google may be blocking requests.")
            return True
        
        page_source = driver.page_source.lower()
        if "403 forbidden" in page_source or "503 service unavailable" in page_source:
            print(Fore.RED + "Rate limiting detected! Google is blocking further requests.")
            return True
        
    except Exception as e:
        print(Fore.YELLOW + f"Error checking for block status: {e}")
    return False

def change_user_agent():
    global user_agent, chrome_options, driver
    user_agent = random.choice(user_agents)
    chrome_options = get_chrome_options(user_agent)
    driver.quit()
    driver = webdriver.Chrome(service=service, options=chrome_options)
    print(Fore.YELLOW + f"Changing User-Agent to: {user_agent}")

def random_delay(min_time=2, max_time=5):
    delay = random.uniform(min_time, max_time)
    time.sleep(delay)
    print(Fore.YELLOW + f"Sleeping for {delay:.2f} seconds to humanize traffic.")

def scan_query(query):
    global total_scanned, total_valid, queries_searched, first_url_scanned

    driver.get(f"https://www.google.com/search?q={query}")
    random_delay(3, 5)

    page_num = 1
    retries = 0
    start_time = time.time()

    while total_scanned < max_urls and retries < max_retries:
        print(f"Scanning page {page_num}...")

        if check_if_blocked():
            retries += 1
            random_delay(10, 20)
            print(Fore.YELLOW + "Refreshing page with new User-Agent...")
            change_user_agent()
            print(Fore.YELLOW + "Waiting for 3 minutes before retrying access to the page...")
            time.sleep(180)
            driver.get(f"https://www.google.com/search?q={query}")
            random_delay(3, 5)
            continue

        links = driver.find_elements(By.XPATH, "//a[@href]")
        print(f"Found {len(links)} links on page {page_num}")

        for link in links:
            try:
                href = link.get_attribute("href")
                if not href or href in scanned_urls:
                    continue

                scanned_urls.add(href)

                if (".sql" in href or ".txt" in href) and "/wp-content/uploads/" in href:
                    valid_urls.append(href)
                    total_valid += 1
                    print(f"Valid URL found: {href}")

                    if not first_url_scanned:
                        print(Fore.MAGENTA + "- - - - - -GOING OP - - - - -")
                        first_url_scanned = True

                total_scanned += 1
                if total_scanned >= max_urls:
                    break

                random_delay(1, 3)

            except Exception as e:
                print(f"Error processing link: {e}")

        print_stats()

        next_page_url = f"https://www.google.com/search?q={query}&start={page_num * 10}"
        driver.get(next_page_url)
        random_delay(3, 5)
        page_num += 1

        if retries >= max_retries:
            print(Fore.RED + f"Max retries reached for {query}. Moving to next query.")
            break

    print_stats()

def start_scan():
    global queries_searched
    for query in queries:
        queries_searched += 1
        scan_query(query)

print(Fore.MAGENTA + "Starting scan with new queries...")
start_scan()

driver.quit()

