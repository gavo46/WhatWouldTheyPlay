import requests
import csv
import random
import time
from bs4 import BeautifulSoup


headers = {"User-Agent": "Mozilla/5.0"}

def scrape(url, writer):
#def scrape(url):
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print("Failed:", url)
        return

    if response.status_code == 429:
        print("Rate limited, backing off:", url)
        time.sleep(random.uniform(60, 90))
        response = requests.get(url, headers=headers, timeout=10)

    soup = BeautifulSoup(response.text, 'html.parser')
    songs = soup.find_all('td', class_='setheadercell sticky-song')
    numbers = soup.find_all('td', class_='setheadercell sticky-num')
    num_list = []
    for num in numbers:
        add = num.get_text(strip=True)
        if add:
            num_list.append(int(add))
        else:
            num_list.append(-1)

    prelim_gaps = soup.find_all('td', attrs = {'class': 'setcell', 'align': 'center', 'style': 'width:0.1%;'})

    gaps = []

    for gap in prelim_gaps:
        num = gap.find('span', class_='bodytext')
        debut = gap.find('span', class_='setitem')
        if num:
            gaps.append(num.text)
        if debut:
            gaps.append('-1')
        if not num and not debut:
            gaps.append('-1')

    if len(songs) != len(gaps) or len(songs) != len(num_list):
        print(f"Skipping {url}: mismatched lengths (songs={len(songs)}, gaps={len(gaps)}, nums={len(num_list)})")
        return

    contenders = soup.find_all('option', selected=True)
    date = contenders[2].get_text()

    increment = 0

    for song in songs:
        title = song.get_text()
        if gaps[increment] and num_list[increment] != -1:
            # print([date, title.replace("»", "").replace(",", "").strip(), gaps[increment].replace(", TD", "").strip()])
            writer.writerow([date, title.replace("»", "").replace(",", "").strip(), gaps[increment].replace(", TD", "").strip()])
        elif not gaps[increment] and num_list[increment] != -1:
            # print([date, title.replace("»", "").replace(",", "").strip(), '-1'])
            writer.writerow([date, title.replace("»", "").replace(",", "").strip(), '-1'])
        increment += 1

with open('allshows.csv', 'a', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Date', 'Song', 'Last Played'])
    with open('showurls.csv', newline='', encoding='utf-8') as url_file:
        reader = csv.reader(url_file)
        for row in reader:
            url = "https://dmbalmanac.com" + row[0]
            print("Scraping:", url)
            scrape(url, writer)
            time.sleep(random.uniform(8, 15)) # nosec

# scrape("https://dmbalmanac.com/TourShowSet.aspx?id=453055508&tid=51&where=1993")