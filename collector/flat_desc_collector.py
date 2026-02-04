import requests
from bs4 import BeautifulSoup
import re

HEADER = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0 Safari/537.36"}


class FlatDescription:
    def __init__(self):
        self.address = '-'
        self.price = '-'
        self.rooms_count = '-'
        self.floor = '-'
        self.building_height = '-'
        self.finishing_standard = '-'
        self.ownership_type = '-'
        self.building_type = '-'
        self.elevator = '-'
        self.home_area = '-'
    
    def separate_floor(self):
        if self.floor and '/' in self.floor:
            flr = self.floor.split('/')
            if len(flr) == 2:
                self.floor = flr[0].strip()
                self.building_height = flr[1].strip()
    
    def area__and_price_into_number(self):
        self.home_area = re.sub(r"[^0-9.]", "", self.home_area)
        self.price = re.sub(r"[^0-9.]", "", self.price)


    def __repr__(self):
        return (
            f"address='{self.address}'\n"
            f"price='{self.price}'\n"
            f"home_area='{self.home_area}'\n"
            f"rooms_count='{self.rooms_count}'\n"
            f"floor='{self.floor}',\n"
            f"building_height='{self.building_height}'\n"
            f"finishing_standard='{self.finishing_standard}'\n"
            f"ownership_type='{self.ownership_type}'\n"
            f"building_type='{self.building_type}'\n"
            f"elevator='{self.elevator}')"
        )

LABEL_TO_ATTR = {
    'Piętro:': 'floor',
    'Stan wykończenia:': 'finishing_standard',
    'Forma własności:': 'ownership_type',
    'Rodzaj zabudowy:': 'building_type',
    'Winda:': 'elevator',
    'Liczba pokoi:': 'rooms_count',
    'Powierzchnia:': 'home_area'
}

def flat_desc_collecting(url, header):
    # with open(file_name, 'r', encoding="utf-8", errors="ignore") as f:
    #     response = f.read()
    response = requests.get(url, headers=header)


    soup = BeautifulSoup(response.text, 'lxml')
    flat_description = FlatDescription()
    address = soup.find('a',class_='css-1eowip8 e1aypsbg1').text
    flat_description.address = address
    flat_description.price = soup.find('strong', class_='css-1o51x5a elm6lnc1').text
    


    elems = soup.find_all('div', class_='css-1okys8k e178zspo0')
    for info in elems:
        label = info.get_text(strip=True)
        if label in LABEL_TO_ATTR:
            value_elem = info.find_next_sibling('div')          
            if value_elem:
                value = value_elem.get_text(strip=True)
                setattr(flat_description, LABEL_TO_ATTR[label], value)
    flat_description.area__and_price_into_number()
    flat_description.separate_floor()
    return flat_description

