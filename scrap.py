import csv
import requests
from bs4 import BeautifulSoup
import time

def scrape_product_listings(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = soup.find_all('div', {'data-component-type': 's-search-result'})

    data = []
    for product in products:
        product_url = 'https://www.amazon.in' + product.find('a', {'class': 'a-link-normal'})['href']
        product_name = product.find('span', {'class': 'a-size-medium'}).text.strip()
        product_price = product.find('span', {'class': 'a-offscreen'}).text.strip()
        product_rating = product.find('span', {'class': 'a-icon-alt'}).text.strip().split()[0]
        product_reviews = product.find('span', {'class': 'a-size-base'}).text.strip()

        data.append([product_url, product_name, product_price, product_rating, product_reviews])

    return data

def scrape_product_details(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        description = soup.find('span', {'class': 'a-list-item'}).text.strip()
    except AttributeError:
        description = ''

    try:
        asin = soup.find('th', text='ASIN').find_next('td').text.strip()
        print(asin)
    except AttributeError:
        asin = ''

    try:
        product_description = soup.find('span', {'class': 'a-list-item'}).text.strip()
    except AttributeError:
        product_description = ''

    try:
        manufacturer = soup.find('a', {'id': 'bylineInfo'}).text.strip()
    except AttributeError:
        manufacturer = ''

    return description, asin, product_description, manufacturer

def scrape_amazon_products():
    base_url = 'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_'
    total_pages = 20

    all_data = []
    for page in range(1, total_pages + 1):
        print(f"Scraping page {page}...")
        url = base_url + str(page)
        data = scrape_product_listings(url)

        for item in data:
            product_url = item[0]
            details = scrape_product_details(product_url)
            item.extend(details)
            all_data.append(item)
            time.sleep(1)  # Delay to avoid overwhelming the server

    return all_data

def save_to_csv(data):
    headers = ['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
               'Description', 'ASIN', 'Product Description', 'Manufacturer']

    with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as file:
       csv_writer = csv.writer(file)
       csv_writer.writerow(headers)
       csv_writer.writerows(data)

    print("Data saved to amazon_products.csv")

# Scrape Amazon products and save data to CSV
all_data = scrape_amazon_products()
save_to_csv(all_data)