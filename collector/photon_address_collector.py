import requests
import re
import urllib.parse

VOIVODESHIPS = [
    "dolnośląskie", "kujawsko-pomorskie", "lubelskie", "lubuskie",
    "łódzkie", "małopolskie", "mazowieckie", "opolskie",
    "podkarpackie", "podlaskie", "pomorskie", "śląskie",
    "świętokrzyskie", "warmińsko-mazurskie", "wielkopolskie", "zachodniopomorskie"
]

class AddressClass:
    def __init__(self):
        self.street = ''
        self.district = ''
        self.city = ''
        self.state = ''

    def __repr__(self):
        return (
            f"street='{self.street}', "
            f"district='{self.district}', "
            f"city='{self.city}', "
            f"state='{self.state}'"
        )

def extract_street(address, assigned_address):
    address_list = [part.strip() for part in address.split(',')]
    for part in address_list:
        match = re.match(r'^ul\.?\s*(.+)', part)
        if match:
            assigned_address.street = match.group(1)
            address_list.remove(part)
            break
    return [a.strip() for a in address_list]

def find_voivodeship(address_list):
    for part in address_list:
        for voiv in VOIVODESHIPS:
            if voiv.lower() == part.lower():
                return voiv
    return None

def prepare_photon_url(parts, limit=10):
    query = urllib.parse.quote_plus(', '.join(parts))
    return f"http://localhost:2322/api?q={query}&limit={limit}"

def get_photon_features(url):
    resp = requests.get(url)
    return resp.json().get('features', [])



def remove_county_from_address(address_list, state):
    """
    Szuka pierwszego powiatu w address_list.
    Jeśli znajdzie, usuwa go z listy i kończy działanie.
    """
    for part in list(address_list):  # kopia, żeby bezpiecznie usuwać
        url = prepare_photon_url([part, state])
        features = get_photon_features(url)

        for f in features:
            props = f['properties']
            if props.get('type') == 'county':
                county_name = (props.get('name') or '').strip().lower()

                # dopasowanie całego słowa
                pattern = r'\b' + re.escape(part.strip().lower()) + r'\b'
                if re.search(pattern, county_name):
                    address_list.remove(part)
                    return  # KONIEC — usuwamy tylko jeden powiat

    # jeśli nic nie znaleziono — lista bez zmian
    return


def find_possible_cities(address_list, state):
    """
    Zwraca listę nazw miast, które pasują dokładnie do części adresu w danym województwie.
    """
    possible_cities = []
    for part in address_list:
        url = prepare_photon_url([part, state])
        features = get_photon_features(url)
        for f in features:
            props = f['properties']
            if props.get('type') == 'city':
                city_name = props.get('name', '').strip().lower()
                if city_name == part.lower().strip():
                    possible_cities.append(city_name)
    return possible_cities


def select_city_with_district(possible_cities, address_list, state):
    
    for city_name in possible_cities:
        for part in address_list:
            url = prepare_photon_url([part, city_name])
            features = get_photon_features(url)
            for f in features:
                props = f['properties']

                name = (props.get('name') or '').strip().lower()
                part_clean = part.strip().lower()
                city_prop = (props.get('city') or '').strip().lower()

                if props.get('type') in ('district', 'locality'):
                    if name == part_clean and city_prop == city_name.strip().lower():
                        district = name
                        return city_name, district

    # fallback — jeśli nie znaleziono dzielnicy
    if possible_cities:
        return possible_cities[0], ''

    return '', ''

def parse_address(address):
    assigned_address = AddressClass()
    address_list = extract_street(address, assigned_address)

    # 1. znajdź województwo
    voiv = find_voivodeship(address_list)
    if voiv:
        assigned_address.state = voiv
        address_list.remove(voiv)
    
    # 2. usuń powiaty z listy adresu
    remove_county_from_address(address_list, assigned_address.state)
    

    # 3. znajdź możliwe miasta
    possible_cities = find_possible_cities(address_list, assigned_address.state)

    # 4. wybierz miasto i dzielnicę
    city_name, district = select_city_with_district(possible_cities, address_list, assigned_address.state)
    assigned_address.city = city_name
    assigned_address.district = district

    return assigned_address

# if __name__ == "__main__":
#     address = "ul.tulipanowa ,koniuchy, toruń, toruński, kujawsko-pomorskie".lower()
#     result = parse_address(address)
#     print(result)

if __name__ == "__main__":
    test_addresses = [
    "ul. Marszałkowska 10, Śródmieście, Warszawa, warszawski, Mazowieckie",
    "ul. Piotrkowska 50, Śródmieście, Łódź, łódzki, Łódzkie",
    "ul. Grunwaldzka 100, Oliwa, Gdańsk, gdański, Pomorskie",
    "ul. Legnicka 20, Fabryczna, Wrocław, wrocławski, Dolnośląskie",
    "ul. Długa 5, Stare Miasto, Kraków, krakowski, Małopolskie",
    "ul. Katowicka 12, Załęże, Katowice, katowicki, Śląskie",
    "ul. Chorzowska 3, Śródmieście, Katowice, katowicki, Śląskie",
    "ul. Modlińska 200, Białołęka, Warszawa, warszawski, Mazowieckie",
    "ul. Puławska 15, Mokotów, Warszawa, warszawski, Mazowieckie",
    "ul. Półwiejska 2, Stare Miasto, Poznań, poznański, Wielkopolskie",
    "ul. Piastowska 8, Wrzeszcz, Gdańsk, gdański, Pomorskie",
    "ul. 3 Maja 10, Śródmieście, Gdynia, gdyński, Pomorskie",
    "ul. Zwycięstwa 15, Śródmieście, Gliwice, gliwicki, Śląskie",
    "ul. Mickiewicza 7, Śródmieście, Rzeszów, rzeszowski, Podkarpackie",
    "ul. Sienkiewicza 20, Śródmieście, Kielce, kielecki, Świętokrzyskie",
    "ul. Kościuszki 5, Śródmieście, Bielsko-Biała, bielski, Śląskie",
    "ul. Wojska Polskiego 12, Śródmieście, Olsztyn, olsztyński, Warmińsko-Mazurskie",
    "ul. Lipowa 3, Śródmieście, Białystok, białostocki, Podlaskie",
    "ul. Dworcowa 1, Śródmieście, Bytom, bytomski, Śląskie",
    "ul. 11 Listopada 6, Praga-Północ, Warszawa, warszawski, Mazowieckie",
    ]

    for address in test_addresses:
        result = parse_address(address.lower())
        print(address.lower())
        print(result,'\n')
