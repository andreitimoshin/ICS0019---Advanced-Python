"""
@author: antimo
"""
import json
import requests
from bs4 import BeautifulSoup
import time

# Set URL
start_url = "https://arvutitark.ee/nutiseadmed/telefonid/1?brands=samsung,xiaomi&sort=top"


def parse(url):
    data_list = []
    # Make the request
    page = requests.get(url)
    # Parse the HTML content
    soup = BeautifulSoup(page.text, 'html.parser')
    # Extract data from each product
    telephones = soup.select(".catalogue-product-wrapper")
    for telephone in telephones:
        title = telephone.select_one('h4._name')['title'].strip()
        price = telephone.select_one('._main-price .price-html').get_text().strip()
        image = telephone.select_one('._image-wrapper img')['src']

        data = {
            'Title': title,
            'Price': price,
            'Picture href': image
        }
        data_list.append(data)
        print(data)

    # Find next page URL
    try:
        next_page = 'https://arvutitark.ee' + soup.select_one('._pagination-button.-arrow.-right a')['href']
        if next_page:
            time.sleep(3)
            print("-------------NEXT--------------", next_page, "--------------PAGE-------------")
            data_list.extend(parse(next_page))
    except:
        print("No more pages")

    return data_list


if __name__ == "__main__":
    data = parse(start_url)
    with open("soup_telephones.json", "w", encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
