import requests
from bs4 import BeautifulSoup
import csv
import json

urls = ['https://ru.myfin.by/currency/novosibirsk', 'https://ru.myfin.by/currency/novosibirsk?page=2']

currency_data_json = []
banks_data_json = []

for url in urls:
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 '
                      'Safari/537.36',
    }
    req = requests.get(url, headers=headers)
    src = req.text

    with open('index.html', 'w', encoding='utf-8') as file:
        file.write(src)

    if url == 'https://ru.myfin.by/currency/novosibirsk':
        '''
        Currency info
        '''

        with open('index.html', 'r', encoding='utf-8') as file:
            src = file.read()

        soup = BeautifulSoup(src, 'html.parser')
        table = soup.find(class_="table-best yellow_bg").find_all('tr')

        titles = table[0].find_all('th')
        table.pop(0)
        title_currency = titles[0].text
        title_buy = titles[1].text
        title_sell = titles[2].text
        title_course_cb = titles[3].text

        with open('data/currency_data_csv.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    title_currency,
                    title_buy,
                    title_sell,
                    title_course_cb
                )
            )

        for item in table:
            data = item.find_all('td')
            currency = data[0].find('a').text
            buy = data[1].text
            sell = data[2].text
            course_cb = data[3].text
            with open('data/currency_data_csv.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (
                        currency,
                        buy,
                        sell,
                        course_cb
                    )
                )
            currency_data_json.append(
                {
                    title_currency: currency,
                    title_buy: buy,
                    title_sell: sell,
                    title_course_cb: course_cb
                }
            )

    '''
    Banks info
    '''

    with open('index.html', 'r', encoding='utf-8') as file:
        src = file.read()

    soup = BeautifulSoup(src, 'html.parser')
    table_1 = soup.find_all(class_="row body tr-turn odd")
    table_2 = soup.find_all(class_="row body tr-turn even")

    title_bank = 'Bank'
    title_usd_buy = 'USD buying rate'
    title_usd_sell = 'USD selling rate'
    title_euro_buy = 'Euro buying rate'
    title_euro_sell = 'Euro selling rate'
    title_update_time = 'Update time'

    with open('data/banks_data_csv.csv', 'a', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                title_bank,
                title_usd_buy,
                title_usd_sell,
                title_euro_buy,
                title_euro_sell,
                title_update_time
            )
        )

    for item in table_1:
        data = item.find_all('td')

        bank = data[0].find('a').text
        usd_buy = data[1].text
        usd_sell = data[2].text
        euro_buy = data[3].text
        euro_sell = data[4].text
        update_time = data[5].text

        banks_data_json.append(
            {
                title_bank: bank,
                title_usd_buy: usd_buy,
                title_usd_sell: usd_sell,
                title_euro_buy: euro_buy,
                title_euro_sell: euro_sell,
                title_update_time: update_time
            }
        )

        with open('data/banks_data_csv.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    bank,
                    usd_buy,
                    usd_sell,
                    euro_buy,
                    euro_sell,
                    update_time
                )
            )

    for item in table_2:
        data = item.find_all('td')

        bank = data[0].find('a').text
        usd_buy = data[1].text
        usd_sell = data[2].text
        euro_buy = data[3].text
        euro_sell = data[4].text
        update_time = data[5].text

        banks_data_json.append(
            {
                title_bank: bank,
                title_usd_buy: usd_buy,
                title_usd_sell: usd_sell,
                title_euro_buy: euro_buy,
                title_euro_sell: euro_sell,
                title_update_time: update_time
            }
        )

        with open('data/banks_data_csv.csv', 'a', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                    bank,
                    usd_buy,
                    usd_sell,
                    euro_buy,
                    euro_sell,
                    update_time
                )
            )

with open('data/currency_data_json.json', 'w', encoding='utf-8') as file:
    json.dump(currency_data_json, file, indent=4, ensure_ascii=False)

with open('data/banks_data_json.json', 'w', encoding='utf-8') as file:
    json.dump(banks_data_json, file, indent=4, ensure_ascii=False)
