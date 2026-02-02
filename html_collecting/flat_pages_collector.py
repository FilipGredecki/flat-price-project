import requests
import random
import time
import os
import re
import csv
HEADERS_LIST = [
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


BASE_DIR = r"C:\Users\Filip\Desktop\flat_price_project"
PAGES_DIR = os.path.join(BASE_DIR, "otodom_pages")
CSV_PATH = os.path.join(BASE_DIR, "pages_status.csv")

os.makedirs(PAGES_DIR, exist_ok=True)

def make_otodom_link(i):
    return f"https://www.otodom.pl/pl/wyniki/sprzedaz/mieszkanie/cala-polska?fromInvalidLocation=true&limit=72&by=LATEST&direction=DESC&page={i}"

def get_last_saved_page():
    files = os.listdir(PAGES_DIR)
    max_page = 0
    for fname in files:
        m = re.match(r"page_(\d+)\.html", fname)
        if m:
            num = int(m.group(1))
            if num > max_page:
                max_page = num
    return max_page

def init_csv_if_needed():
    if not os.path.exists(CSV_PATH) or os.path.getsize(CSV_PATH) == 0:
        with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=";")
            writer.writerow(["page_file", "status"])

def append_page_to_csv(page_number):
    page_file = f"page_{page_number}.html"
    # sprawdzamy czy wpis już istnieje
    if os.path.exists(CSV_PATH):
        with open(CSV_PATH, encoding="utf-8") as f:
            for line in f:
                if line.startswith(page_file + ";"):
                    return
    with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=";")
        writer.writerow([page_file, "false"])

def save_page_html(page_number, html_text):
    file_path = os.path.join(PAGES_DIR, f"page_{page_number}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_text)
    append_page_to_csv(page_number)

def collect_page(page_number):
    headers = random.choice(HEADERS_LIST)
    url = make_otodom_link(page_number)
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        save_page_html(page_number, response.text)
        print(f"Zapisano stronę {page_number}")
    else:
        print(f"Błąd pobrania strony {page_number}, status: {response.status_code}")

def main(max_pages=2000):
    init_csv_if_needed()
    last_page = get_last_saved_page()
    print(f"Startujemy od strony {last_page + 1}")
    for i in range(last_page + 1, max_pages + 1):
        start_time = time.time()
        try:
            collect_page(i)
        except Exception as e:
            print(f"Błąd przy stronie {i}: {e}")
        elapsed = time.time() - start_time
        time.sleep(random.uniform(1, 2))  # losowe opóźnienie, żeby nie blokowali IP

if __name__ == "__main__":
    main()