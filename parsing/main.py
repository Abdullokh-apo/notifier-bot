import os.path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
import lxml


class Anime:
    URL = 'https://animego.org/anime/status/latest?sort=a.createdAt' \
          '&direction=desc '
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/99.0.4844.84 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
                  'image/avif,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9 '
    }
    key = ''
    key_file = ''

    def __init__(self, key_file):
        self.key_file = key_file

        if os.path.exists(key_file):
            self.key = open(key_file, 'r').read()
        else:
            f = open(key_file, 'w')
            self.key = self.get_key()
            f.write(self.key)
            f.close()

    def new_films(self):
        r = requests.get(self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(r.content, 'lxml')
        new = []
        items = soup.select('.animes-list > .row > .col-12 '
                            '> .animes-list-item > '
                            '.media-body > '
                            '.h5 > a')
        for i in items:
            l_key = self.parse_href(i['href'])
            if self.key < l_key:
                new.append(i['href'])
        return new

    def film_info(self, uri):
        r = requests.get(uri).content
        html = BeautifulSoup(r, 'lxml')

        id_ = uri.split('-')[-1]
        title = html.find('div', class_='anime-title').find('h1').text
        # link
        description = html.find('div', class_='description pb-3').text

        try:
            genre = html.find('dt', class_='col-6 col-sm-4 font-weight-normal '
                                           'text-gray-dark-6', text='Жанр'). \
                find_next('dd').text.replace('                             ',
                                             ' ')
        except:
            genre = ''
        image = html.find('div', class_='anime-poster').find('img').get('src')
        info = {
            'id': id_,
            'title': title,
            'genre': genre,
            'description': description,
            'link': uri,
            'image': image
        }
        return info

    def download_image(self, url):
        r = requests.get(url, allow_redirects=True)

        a = urlparse(url)
        filename = os.path.basename(a.path)
        open(filename, 'wb').write(r.content)

        return filename

    def get_key(self):
        r = requests.get(self.URL, headers=self.HEADERS)
        soup = BeautifulSoup(r.text, 'lxml')  # r.text
        items = soup.select('.animes-list > .row > .col-12 '
                            '> .animes-list-item > '
                            '.media-body > '
                            '.h5> a')
        return self.parse_href(items[0]['href'])

    def parse_href(self, href):
        result = str(href).split('-')[-1]
        return result

    def update_lastkey(self, new_key):
        self.key = new_key

        with open(self.key_file, "r+") as f:
            data = f.read()
            f.seek(0)
            f.write(str(new_key))
            f.truncate()

        return new_key


