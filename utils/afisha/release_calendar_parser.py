import requests
from bs4 import BeautifulSoup


async def parsing_releases(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    lists = soup.find('li', class_='_15Vwt RDKna kWxBc').findAll('li')
    count = 0
    parsed_movies = []
    for li in lists:
        while count <= 1:
            if li.find('span', class_='_3iwYy _3Y-3V'):
                count += 1
                break
            else:
                parsed_movies.append(li)
                break
    movies = [
        {
            "id": parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href').split("/")[-2],
            "link": "afisha.ru" + parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href'),
            "name": parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').find('h2', class_='_3Yfoo').text
        } for parsed_movie in parsed_movies
    ]

    return movies
