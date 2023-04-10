import datetime
import time
import urllib.parse
import warnings
import os.path

from bs4 import BeautifulSoup
from art import *
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

CLASSNAME = "yuRUbf"

def ScrapGoogle():
    start_time = time.time()  # Start Timestamp
    links = []  # URLs
    sitetext = []  # Site Text
    uniqueURLs = []  # Unique URLs

    query = str(input("Enter search query: "))
    pages = int(input("How many pages should be scanned: "))

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

    # Creating the file
    currentTime = round(time.time() * 1000)
    filename = os.path.join("C:\\AntiCopyright", f"AntiCopyright_GSReport_{currentTime}")

    if not os.path.isdir("C:\\AntiCopyright"):
        os.mkdir("C:\\AntiCopyright")

    file = open(f"{filename}.txt", 'w', encoding="utf-8")

    # Appends every unique URL in the list
    for i in range(0, len(links)):
        parsed = urllib.parse.urlparse(links[int(i)])
        phn = parsed.hostname

        if phn not in uniqueURLs:
            uniqueURLs.append(phn)

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

    for i in range(0, len(uniqueURLs)):
        file.write(f"{uniqueURLs[int(i)]}\n")

    print(f"[Success] File can be found at: {file.name}")
    file.close()

    print(f"Successfully Scrapped! [{round(time.time() - start_time)}s]")

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
    ScrapGoogle()

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

        # Creating the file
        currentTime = round(time.time() * 1000)
        filename = os.path.join("C:\\AntiCopyright", f"AntiCopyright_GSReport_{currentTime}")

        if not os.path.isdir("C:\\AntiCopyright"):
            os.mkdir("C:\\AntiCopyright")

        print("Creating report file.")
        file = open(f"{filename}.txt", 'w', encoding="utf-8")
        file.write(f"""(c) Copyright {datetime.date.today().year} Agesoft. All Rights Reserved
AntiCopyright Google Scrapping report from {datetime.date.today()}\n
Details:
Query: "{query}"
Indexes Found: {len(links)}
Pages Scanned: {scannedpages}\n\n""")

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

if choice > 1:
    print("Error: Invalid Choice")
    exit(1)