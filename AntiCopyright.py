import datetime
import time
import urllib.parse
import warnings
import os.path

from sys import platform
from bs4 import BeautifulSoup
from art import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

CLASSNAME = "yuRUbf"
WINPATH = "C:\\AntiCopyright"
LINUXPATH = "//dev/AntiCopyright"

# Logs Results to a file
def LogResults(start_time : int, uniqueURLs : list, links : list, query : str, sitetext : list, pages):

    # Creating the file
    currentTime = round(time.time() * 1000)
    if platform == "win32":
        filename = os.path.join(WINPATH, f"AntiCopyright_GSReport_{currentTime}")
        if not os.path.isdir(WINPATH):
            os.mkdir(WINPATH)
    if platform == "linux":
        filename = os.path.join(LINUXPATH, f"AntiCopyright_GSReport_{currentTime}")
        if not os.path.isdir(WINPATH):
            os.mkdir(WINPATH)

    file = open(f"{filename}.txt", 'w', encoding="utf-8")

    file.write(f"""(c) Copyright {datetime.date.today().year} Agesoft. All Rights Reserved
    AntiCopyright Google Scrapping report from {datetime.date.today()}\n
    Details:
    Query: "{query}"
    Indexes Found: {len(links)}
    Pages Scanned: {pages}
    URLs: {len(uniqueURLs)}\n\n""")

    for i in range(0, len(links)):
        file.write(f"Text: {sitetext[int(i)]}\nLink: {links[int(i)]}\n\n")

    file.write("URLs:\n")
    for i in range(0, len(links)):
        parsed = urllib.parse.urlparse(links[int(i)])
        phn = parsed.hostname

        if phn not in uniqueURLs:
            uniqueURLs.append(phn)

    for i in range(0, len(uniqueURLs)):
        file.write(f"{uniqueURLs[int(i)]}\n")

    print(f"[Success] File can be found at: {file.name}")
    file.close()

    print(f"Successfully Scrapped! [{round(time.time() - start_time)}s]")

def ScrapGoogle(query : str, pages : int):
    start_time = time.time()  # Start Timestamp
    links = []  # URLs
    sitetext = []  # Site Text
    uniqueURLs = []  # Unique URLs

    # Scrapping each Google Search site
    for page in range(1, pages):
        print(f"Search Page: {page}")
        url = "http://www.google.com/search?hl=en&q=" + query + "&start=" + str((page - 1) * 10)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        elements = soup.find_all('div', class_=CLASSNAME)

        for h in elements:
            link = h.a.get('href')
            links.append(link)
            sitetext.append(h.h3.text)

        for i in range(0, len(links)):
            print(f"Text: {sitetext[int(i)]}\nLink: {links[int(i)]}\n\n")

    # Appends every unique URL in the list
    for i in range(0, len(links)):
        parsed = urllib.parse.urlparse(links[int(i)])
        phn = parsed.hostname

        if phn not in uniqueURLs:
            uniqueURLs.append(phn)
    LogResults(start_time, uniqueURLs, links, query, sitetext, pages)

tprint("AntiCopyright")
print("------------------------------[  By  Agesoft   ]--------------------------------")

print("Setting up ChromeDriver")

# Shut Up!
warnings.filterwarnings("ignore", category=DeprecationWarning)

# Setting up ChromeDriver
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

print("[1] Scrap Google Search")
print("[2] Automatically Scrap Google Search\n")

choice = int(input("Enter Option: "))

if choice == 1:
    query = str(input("Enter search query: "))
    pages = int(input("How many pages should be scanned: "))
    ScrapGoogle(query, pages)

if choice == 2:

    links = []  # URLs
    sitetext = []  # Site Text
    uniqueURLs = []  # Unique URLs
    pages = 1000
    scannedpages = 1

    try:
        query = str(input("Enter search query: "))

        # Scrapping each Google Search site
        print("Starting scrapping:\n\n")
        while True:
            for page in range(1, pages):
                print(f"Search Page: {page}")
                url = "http://www.google.com/search?hl=en&q=" + query + "&start=" + str((page - 1) * 10)
                driver.get(url)
                soup = BeautifulSoup(driver.page_source, 'lxml')

                elements = soup.find_all('div', class_=CLASSNAME)

                for h in elements:
                    link = h.a.get('href')
                    links.append(link)
                    sitetext.append(h.h3.text)

                for i in range(0, len(links)):
                    print(f"Text: {sitetext[int(i)]}\nLink: {links[int(i)]}\n\n")

                time.sleep(5)
                scannedpages = scannedpages + 1
    except KeyboardInterrupt:
        print("Scrapping stopped")
        LogResults(0.0, uniqueURLs, links, query, sitetext, scannedpages)


if choice > 2:
    print("Error: Invalid Choice")
    exit(1)
