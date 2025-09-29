import argparse
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ASCII Art (adapted from the original)
ASCII_ART = """
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣤⣤⣶⣤⣤⣀⣀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣾⣿⣿⣿⣿⣿⡿⠋⠉⠛⠛⠛⠿⣿⠿⠿⢿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⣿⣿⣿⣿⣿⠟⠀⠀⠀⠀⠀⡀⢀⣽⣷⣆⡀⠙⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣿⣿⣷⠶⠋⠀⠀⣠⣤⣤⣉⣉⣿⠙⣿⠀⢸⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⠁⠀⠀⠴⡟⣻⣿⣿⣿⣿⣿⣶⣿⣦⡀⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢨⠟⡿⠻⣿⠃⠀⠀⠀⠻⢿⣿⣿⣿⣿⣿⠏⢹⣿⣿⣿⢿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣼⣷⡶⣿⣄⠀⠀⠀⠀⠀⢉⣿⣿⣿⡿⠀⠸⣿⣿⡿⣷⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⡿⣦⢀⣿⣿⣄⡀⣀⣰⠾⠛⣻⣿⣿⣟⣲⡀⢸⡿⡟⠹⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⠞⣾⣿⡛⣿⣿⣿⣿⣰⣾⣿⣿⣿⣿⣿⣿⣿⣿⡇⢰⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⠀⣿⡽⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⢿⠿⣍⣿⣧⡏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣷⣿⣿⣿⣿⣿⣿⣿⣿⣷⣮⣽⣿⣷⣙⣿⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡟⣹⡿⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡧⣦⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡆⠀⠀⠀⠀⠀⠀⠀⠉⠻⣿⣿⣾⣿⣿⣿⣿⣿⣿⡶⠏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⡴⠞⠛⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠚⣿⣿⣿⠿⣿⣿⠿⠟⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⢀⣠⣤⠶⠚⠉⠉⠀⢀⡴⠂⠀⠀⠀⠀⠀⠀⠀⠀⢠⠀⠀⢀⣿⣿⠁⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠞⠋⠁⠀⠀⠀⠀⣠⣴⡿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⣾⠀⠀⣾⣿⠋⠀⢠⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⡀⠀⠀⢀⣷⣶⣿⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣆⣼⣿⠁⢠⠃⠈⠓⠦⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⣿⣿⡛⠛⠿⠿⠿⠿⠿⢷⣦⣤⣤⣤⣦⣄⣀⣀⠀⢀⣿⣿⠻⣿⣰⠻⠀⠸⣧⡀⠀⠉⠳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠛⢿⣿⣆⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠙⠛⠿⣦⣼⡏⢻⣿⣿⠇⠀⠁⠀⠻⣿⠙⣶⣄⠈⠳⣄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠈⠋⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣐⠀⠀⠀⠈⠳⡘⣿⡟⣀⡠⠿⠶⠒⠟⠓⠀⠹⡄⢴⣬⣍⣑⠢⢤⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀ 
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠈⣿⣿⣷⣯⠀⠀⠀⠀⠀⠀⠀⠀⠉⠻⢦⣷⡀⠀⠀⠀⠀⠀⠀⠉⠲⣄⠀ 
⠠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢦⠀⢹⣿⣏⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢻⣷⣄⠀⠀⠀⠀⠀⠀⠈⠳ 
⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠁⣸⣿⣿⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⣽⡟⢶⣄⠀⠀⠀⠀⠀ 
⠯⠀⠀⠀⠒⠀⠀⠀⠀⠀⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢻⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⡄⠈⠳⠀⠀⠀⠀ 
⠀⠀⢀⣀⣀⡀⣼⣤⡟⣬⣿⣷⣤⣀⣄⣀⡀⠀⠀⠀⠀⠈⣿⣿⡄⣉⡀⠀⠀⠀⠀⠀⠀⠀⢀⠀⠀⠀⠀⠀⣿⣿⣄⠀⣀⣀⡀⠀
"""

# Even more updated lists of dorks
RDP_WEB_DORKS = [
    'intitle:"Remote Desktop Web Connection"',
    'intitle:"RD Web Access"',
    'inurl:"/tsweb"',
    'inurl:"/RDWeb"',
    'inurl:"/remote"',
    'inurl:"/remote-desktop"',
    'inurl:"/remote-desktop-gateway"',
    'inurl:"/webclient/index.html"',
    'inurl:"rdp.html"',
    'inurl:"rdweb/login.aspx"',
    'intext:"Terminal Services" "Welcome"',
    'intitle:"Remote Desktop" intext:"login"',
    'intitle:"Remote Desktop Login"',
    'inurl:"login" intext:"Remote Desktop"',
    'intitle:"Remote Desktop" intext:"Username" intext:"Password"',
    'intitle:"RD Web Access" intext:"Sign in"',
    'intitle:"Remote Desktop Web Connection" inurl:tsweb',
    'inurl:/rdweb intitle:"remote desktop"',
    'intext:"Connect to Remote Desktop" intitle:login',
    # Additional from sources
    'inurl:/remote/login/ intitle:"RDP"',
    'intitle:"index of" AND ("remote access" OR "remote desktop" OR "remote login") AND ext:(ini OR cfg OR conf)',
    'intitle:"index of" AND ("rdp" OR "remote desktop connection") AND ext:(ini OR cfg OR conf)'
]

RDP_FILES_DORKS = [
    'filetype:rdp',
    'intitle:index.of "rdp"',
    'intitle:"index of" default.rdp',
    'filetype:rdp intext:"hostname"',
    'filetype:rdp intext:"remote desktop"',
    'intitle:"index of" *.rdp',
    # Additional
    'filetype:rdp rdp'
]

RDP_LOGS_DORKS = [
    'filetype:log intext:"RDP"',
    'filetype:conf intext:"RDP"',
    'filetype:txt intext:"3389"',
    'filetype:ini intext:"3389"',
    'filetype:log intext:"remote desktop"',
    'filetype:txt intext:"rdp" intext:"password"',
    'intext:"port:3389" filetype:cfg',
    # Additional
    'filetype:log inurl:"access.log"',
    'filetype:sql inurl:wp-content/backup-*'
]

# Expanded VPS dorks
VPS_DORKS = [
    'intitle:"VPS Login"',
    'inurl:"/vps/login"',
    'intitle:"SolusVM Login"',
    'inurl:"/clientarea.php" intitle:"VPS"',
    'intitle:"Virtualizor Admin"',
    'inurl:admin/login intitle:"VPS Panel"',
    'inurl:/whmcs intitle:login',
    'inurl:/cpanel/login',
    'inurl:/webmin/ intitle:"Login"',
    'inurl:/plesk/login',
    'intitle:"index of /admin" intext:"vps"',
    'inurl:admin/login',
    'intitle:"login" inurl:cpanel',
    'inurl:/whm/ intitle:"Login"',
    'intext:"Welcome to phpMyAdmin"',
    'inurl:/phpmyadmin/index.php',
    'inurl:/db/websql/',
    # Additional from sources
    'intitle:"Login — WordPress"',
    'inurl:/phpPgAdmin/index.php',
    'intext:"phpPgAdmin — Login"',
    'inurl:login',
    'inurl:login ext:jsp intext:"username" AND intext:"password"',
    'ext:txt inurl:password OR inurl:credentials',
    'filetype:env intext:password',
    'inurl:admin.php',
    'intitle:"login" site:example.com',  # Adapt site: as needed
    'inurl:"admin" site:example.com',
    'site:target.com inurl:"admin" OR inurl:"debug"',
    'site:target.com inurl:"?action=" OR inurl:"?cmd="',
    'inurl:login.php'
]

# User agents for rotation
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.101 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
]

def setup_driver():
    options = Options()
    options.add_argument("--headless")  # Run in headless mode
    options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")
    # Add your chromedriver path here
    driver = webdriver.Chrome(options=options)  # Assuming chromedriver is in PATH or specify executable_path
    return driver

def detect_captcha(driver):
    try:
        driver.find_element(By.ID, "recaptcha")  # Simple check for reCAPTCHA
        return True
    except NoSuchElementException:
        return False

def scrape_google(dork, driver, output_file, pages=5):
    urls = set()
    base_url = "https://www.google.com/search?q="
    query = base_url + dork.replace(" ", "+").replace(":", "%3A").replace("\"", "%22")  # Encode special chars

    driver.get(query)
    time.sleep(random.uniform(2, 5))  # Initial delay

    if detect_captcha(driver):
        print("CAPTCHA detected. Please handle manually or use proxies.")
        return

    for page in range(pages):
        try:
            wait = WebDriverWait(driver, 10)
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.g')))

            results = driver.find_elements(By.CSS_SELECTOR, 'div.g')
            for result in results:
                try:
                    link = result.find_element(By.TAG_NAME, 'a').get_attribute('href')
                    if link.startswith('http'):
                        urls.add(link)
                except:
                    pass

            # Next page
            try:
                next_button = driver.find_element(By.ID, 'pnnext')
                next_button.click()
                time.sleep(random.uniform(3, 7))  # Delay between pages
            except NoSuchElementException:
                break

            # Rotate user agent and restart driver for evasion
            driver.quit()
            driver = setup_driver()

            if detect_captcha(driver):
                print("CAPTCHA detected on page change.")
                break

        except TimeoutException:
            print("Timeout waiting for results.")
            break

    # Save to file
    with open(output_file, 'a') as f:
        for url in urls:
            f.write(url + '\n')

    print(f"Scraped {len(urls)} URLs for dork: {dork}")

def main():
    print(ASCII_ART)
    print("Chad-RDP - Automated Dorking for RDP/RDS and VPS")
    print("Updated with even more dorks from additional sources.")
    print("Use responsibly for educational purposes only.\n")

    parser = argparse.ArgumentParser(description="RDP and VPS Dorking Tool")
    parser.add_argument('--rdp-web', action='store_true', help='Search for RDP Web Interfaces')
    parser.add_argument('--rdp-files', action='store_true', help='Search for Downloadable RDP Files')
    parser.add_argument('--rdp-logs', action='store_true', help='Search for Log Files with RDP Info')
    parser.add_argument('--vps', action='store_true', help='Search for VPS Control Panels and Logins')
    parser.add_argument('--output', default='results.txt', help='Output file (default: results.txt)')
    parser.add_argument('--pages', type=int, default=5, help='Number of Google pages to scrape per dork (default: 5)')

    args = parser.parse_args()

    driver = setup_driver()

    if args.rdp_web:
        print("Searching for RDP Web Interfaces...")
        for dork in RDP_WEB_DORKS:
            scrape_google(dork, driver, args.output, args.pages)

    if args.rdp_files:
        print("Searching for Downloadable RDP Files...")
        for dork in RDP_FILES_DORKS:
            scrape_google(dork, driver, args.output, args.pages)

    if args.rdp_logs:
        print("Searching for Log Files with RDP Info...")
        for dork in RDP_LOGS_DORKS:
            scrape_google(dork, driver, args.output, args.pages)

    if args.vps:
        print("Searching for VPS Control Panels and Logins...")
        for dork in VPS_DORKS:
            scrape_google(dork, driver, args.output, args.pages)

    driver.quit()
    print("\nDone. Results saved to", args.output)

if __name__ == "__main__":
    main()
