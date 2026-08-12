import requests
import csv
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0"}

year_urls = ['https://dmbalmanac.com/TourShow.aspx?where=1991&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=1992&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=1993&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=1994&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=1995&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=1996&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=1997&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=1998&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=1999&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2000&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2001&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2002&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2003&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2004&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2005&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2006&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2007&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2008&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2009&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2010&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2011&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2012&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2013&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2014&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2015&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2016&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2017&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2018&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2019&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2020&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2021&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2022&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2023&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2024&aid=1', 'https://dmbalmanac.com/TourShow.aspx?where=2025&aid=1', 
'https://dmbalmanac.com/TourShow.aspx?where=2026&aid=1']



for url in year_urls:
    urls = []
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')
    body = soup.find('tbody')
    shows = body.find_all('tr', class_=['', 'tr', 'to', 'lc', 'lo', 'bc', 'misc'])
    for show in shows:
        check = show.find('td', class_='p-1 d-none d-sm-table-cell')
        link = show.find('a', href=True)
        final_link = link['href']
        add = True
        if check:
            cell_html = str(check)
            if '[Set Unknown]' in cell_html or '[Rescheduled]' in cell_html or '[Cancelled]' in cell_html:
                add = False
            text_check = link.span
            if 'grey4' in text_check['class']:
                add = False
        if add:
            urls.append(final_link)
        
    with open('showurls.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        for link in urls:
            writer.writerow([link])


    