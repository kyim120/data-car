import requests
from bs4 import BeautifulSoup
import os
import time

base_url = "https://stock.adobe.com/search?filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfree_collection%5D=0&filters%5Bcontent_type%3Aimage%5D=1&k=Car+accident&order=relevance&limit=100&search_page={}&search_type=pagination&get_facets=0"

downloaded = 0
target = 400

for page in range(1, 11):  # pages 1 to 10
    if downloaded >= target:
        break
    url = base_url.format(page)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    imgs = soup.find_all('img')
    for img in imgs:
        if downloaded >= target:
            break
        src = img.get('data-lazy') or img.get('src')
        if src and 'ftcdn.net' in src and not src.startswith('data:'):
            filename = src.split('/')[-1]
            if not os.path.exists(filename):
                try:
                    img_response = requests.get(src)
                    with open(filename, 'wb') as f:
                        f.write(img_response.content)
                    print(f"Downloaded {filename}")
                    downloaded += 1
                    time.sleep(0.5)  # delay to avoid blocking
                except Exception as e:
                    print(f"Failed to download {src}: {e}")
    print(f"Page {page} done, total downloaded: {downloaded}")

print(f"Total images downloaded: {downloaded}")
