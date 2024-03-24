import requests
from bs4 import BeautifulSoup
import csv

with open('data/all_data_csv.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(
        (
            'Бренд',
            'Название товара',
            'Описание',
            'Вариант: цвет',
            'Вариант: размер',
            'Материалы',
            'Розничная цена',
            'Изображение 1',
            'Изображение 2',
            'Изображение 3',
            'Изображение 4'
        )
    )

url = 'https://ieristore.com/collections/0711'
headers = {
    'Accept': '*/*',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                  'Safari/537.36 ',
}
req = requests.get(url, headers=headers)
src = req.text

with open('source.html', 'w', encoding='utf-8') as file:
    file.write(src)

base_url = 'https://ieristore.com'
with open('source.html', 'r', encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'html.parser')
table = soup.find(class_="grid grid--uniform grid--collection boost-pfs-filter-products")
products = table.find_all(class_="grid-product__content")

brand = '0711'

for product in products:
    product_href = base_url + product.find('a')['href']
    req = requests.get(product_href, headers=headers)
    product_src = req.text
    product_soup = BeautifulSoup(product_src, 'html.parser')

    image = product_soup.find(class_="image-wrap").find('img')['data-photoswipe-src'][2:]
    name = product_soup.find(class_='h2 product-single__title').text.strip()
    price = product_soup.find(class_='product__price').find_all('span')[0].text

    data = product_soup.find(class_="product-single__description rte").find_all('p')
    description = data[1].text
    if description == 'DETAILS':
        description = data[-4].text
    color = data[-1].text
    material = data[-2].text

    sizes = []
    join_string = ' '
    if color.startswith('Material') or color[0].isdigit():
        material = color
        color = 'None'
    elif color.startswith('Diameter') or color.startswith('Size') or color.startswith('Height'):
        sizes = color
        join_string = ''
        color = 'None'

    if not isinstance(sizes, str):
        data_sizes = product_soup.find(class_="product-single__variants no-js").find_all('option')
        for s in data_sizes:
            size = s.text.strip()
            if not size.endswith('Sold out'):
                index = size.index('-')
                size = size[0:index]
            if not size.startswith('Default') and not size.startswith('B'):
                sizes.append(size)
            else:
                sizes = 'None'
    if not isinstance(sizes, str):
        sizes = join_string.join(sizes)
    with open('data/all_data_csv.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                brand,
                name,
                description,
                color,
                sizes,
                material,
                price,
                image
            )
        )
