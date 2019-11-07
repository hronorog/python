import requests
import csv
from multiprocessing import Pool


def get_html(url):
    r = requests.get(url)
    return r.text


# записываем данные в csv-файл
def write_csv(data):
    with open('websites.csv', 'a') as file:
        order = ['name', 'url', 'description', 'traffic', 'percent']
        writer = csv.DictWriter(file, fieldnames=order)
        writer.writerow(data)


# получаем со страницы ajax данные, выбираем нужные данные
def get_page_data(text):
    data = text.strip().split('\n')[1:]

    for row in data:
        columns = row.strip().split('\t')
        name = columns[0]
        url = columns[1]
        descriptions = columns[2]
        traffic = columns[3]
        percent = columns[4]

        data = {'name': name,
                'url': url,
                'description': descriptions,
                'traffic': traffic,
                'percent': percent}
        write_csv(data)


def make_all(url):
    text = get_html(url)
    get_page_data(text)


def main():
    url = 'https://www.liveinternet.ru/rating/ru//today.tsv?page={}'
    urls = [url.format(str(i)) for i in range(1, 501)]
    # запускаем 20 процессов одновременно
    with Pool(20) as p:
        try:
            p.map(make_all, urls)
        except:
            pass


if __name__ == '__main__':
    main()
