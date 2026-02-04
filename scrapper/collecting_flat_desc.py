import pandas as pd
import os
import requests
from bs4 import BeautifulSoup
import random
import time
import csv
import sys

sys.path.append(r"C:\Users\Filip\Desktop\flat_price_project\collector")
from flat_desc_collector import flat_desc_collecting
from photon_address_collector import parse_address
WEB_HEADERS = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/90.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Opera/77.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Edge/90.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36 Chrome/80.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/88.0"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/89.0"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; AS; rv:11.0) like Gecko"},
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/87.0"}
]

def create_csv_if_not_exist():
    filepath = r"csv_folder\basic.csv"
    HEADERS = ['state','city','locality','street','price','home_area','rooms_count','floor','building_height','finishing_standard','ownership_type','building_type','elevator']
    if not os.path.exists(filepath):
        df = pd.DataFrame(columns=HEADERS)
        df.to_csv(filepath, sep=';',index=False)
        
    
def collect_links(page_file):
    path_to_html = fr"otodom_pages\{page_file}"
    with open(path_to_html, 'r',encoding='utf-8', errors="ignore") as f:
        response = f.read()
        soup = BeautifulSoup(response, 'lxml')
        links = [
        div.find("a")["href"]
            for div in soup.find_all("div", class_="css-17rb9mp")
            if div.find("a", href=True)
        ]

        return set(links)

def main():
    page_status_data_frame = pd.read_csv(r'C:\Users\Filip\Desktop\flat_price_project\pages_status.csv',delimiter=';') 
    create_csv_if_not_exist()
    basic_data_frame = pd.read_csv(r'csv_folder\basic.csv', delimiter=';')
    for idx, row in page_status_data_frame.iterrows():
        if not row['status']:
            xx = time.time()
            batch = []
            links = collect_links(row['page_file'])
            for link in links:
                try:
                    full_link = r'https://www.otodom.pl' + link
                    flat_description = flat_desc_collecting(full_link,random.choice(WEB_HEADERS))
                    assigned_address = parse_address(flat_description.address)
                    flat_data = {
                        "state": assigned_address.state,
                        "city": assigned_address.city,
                        "locality": assigned_address.district,
                        "street": assigned_address.street,
                        "price": flat_description.price,
                        "home_area": flat_description.home_area,
                        "rooms_count": flat_description.rooms_count,
                        "floor": flat_description.floor,
                        "building_height": flat_description.building_height,
                        "finishing_standard": flat_description.finishing_standard,
                        "ownership_type": flat_description.ownership_type,
                        "building_type": flat_description.building_type,
                        "elevator": flat_description.elevator
                    }
                    batch.append(flat_data)
                except:
                    continue
            df_batch = pd.DataFrame(batch)
            basic_data_frame = pd.concat([basic_data_frame, df_batch], ignore_index=True)
            basic_data_frame.to_csv(r'csv_folder\basic.csv', sep=';', index=False)
            page_status_data_frame.at[idx, 'status'] = True
            page_status_data_frame.to_csv(
            r'C:\Users\Filip\Desktop\flat_price_project\pages_status.csv',
            sep=';',
            index=False
            )
            elapsed = time.time() - xx
            estimated = ((1999 - idx) * elapsed) // 60

            print(f"Processed {row['page_file']} in {elapsed:.2f}s   estimated time {estimated:.2f} min")

main()
