import requests
from bs4 import BeautifulSoup


async def notify_parser():
    url = "https://www.afisha.ru/data-vyhoda/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    lists = soup.find('li', class_='_15Vwt RDKna kWxBc').findAll('li')
    count = 0
    movies = []
    for li in lists:
        while count <= 1:
            if li.find('span', class_='_3iwYy _3Y-3V'):
                count += 1
                break
            else:
                movies.append(li)
                break
    for movie in movies:
        movie['link'] = "https://www.afisha.ru" + movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href')
        movie['id'] = int(movie['link'].split("/")[4])
        movie['name'] = movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').find('h2', class_='_3Yfoo').text
    return movies
