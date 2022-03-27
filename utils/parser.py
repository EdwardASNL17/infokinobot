from bs4 import BeautifulSoup
import requests

from utils.db_api.database import Movie


async def parsing_movies():
    url = f"https://www.afisha.ru/msk/schedule_cinema/na-segodnya/"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    if soup.find('div', class_='_3zDWC _3x7YU _2cFJG hkScZ'):
        count_pages = len(soup.find('div', class_='_3zDWC _3x7YU _2cFJG hkScZ').find_all('button')) - 2
    else:
        count_pages = 1
    for i in range(1, count_pages + 1):
        url = f"https://www.afisha.ru/msk/schedule_cinema/na-segodnya/page{i}/"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'lxml')
        movies = soup.findAll('div', class_='_1kwbj lkWIA _2Ds3f')
        for movie in movies:
            movie['link'] = "https://www.afisha.ru" + movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href')
            movie['id'] = int(movie['link'].split("/")[-2])
            movie['name'] = movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').find('h2', class_='_3Yfoo').text
            movie['year'] = movie.find('div', class_='_2jztV _2Nzs2 _2XtXq').find('span', class_='_1gC4P').text
            req = requests.get(movie['link'])
            soup = BeautifulSoup(req.text, 'lxml')
            if soup.find('h2', class_='_3Yfoo'):
                movie['header'] = soup.find('h2', class_='_3Yfoo').text
            else:
                movie['header'] = ""
            if soup.find('div', class_='_1kwbj lkWIA _2Ds3f').find('p'):
                movie['synopsis'] = soup.find('div', class_='_1kwbj lkWIA _2Ds3f').find('p').text
            else:
                movie['synopsis'] = ""
            infoCount = soup.find_all('span', class_='h1Lfd')
            info = soup.find_all('span', class_='_1gC4P')
            movie['country'] = info[0].text
            check = infoCount[2].text
            if check == "Режиссер" or check == "Режиссеры":
                movie['director'] = info[2].text
                if infoCount[3].text == "Продолжительность":
                    movie['duration'] = info[3].text
                else:
                    movie['duration'] = ''
            else:
                movie['director'] = ''
                movie['duration'] = info[2].text
            movie['age_rating'] = info[len(infoCount) - 2].text
            await Movie.get_or_create(id=movie['id'], name=movie['name'], year=movie["year"], header=movie["header"],
                                      synopsis=movie['synopsis'], country=movie['country'], director=movie['director'],
                                      duration=movie['duration'], age_rating=movie['age_rating'], url=movie['link'])
