import requests
from bs4 import BeautifulSoup


async def parsing_afisha(url):
    r = requests.get(url)
    if len(r.history) == 0:
        soup = BeautifulSoup(r.text, 'lxml')
        parsed_movies = soup.findAll('div', class_='_1kwbj lkWIA _2Ds3f')
        movies = [
            {
                "id": parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href').split("/")[-3],
                "link": "afisha.ru" + parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href'),
                "name": parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').find('h2', class_='_3Yfoo').text
            } for parsed_movie in parsed_movies
        ]
    else:
        movies = []
    return movies


async def parsing_pushkard(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    parsed_movies = soup.findAll('div', class_='_1kwbj lkWIA _2Ds3f')
    movies = [
        {
            "id": parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href').split("/")[-3],
            "link": "afisha.ru" + parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').get('href'),
            "name": parsed_movie.find('a', class_='_3NqYW DWsHS _3lmHp wkn_c').find('h2', class_='_3Yfoo').text
        } for parsed_movie in parsed_movies
    ]
    return movies


async def parsing_movie(movie_id):
    movie = {'link': f"https://www.afisha.ru/movie/{movie_id}", 'id': int(movie_id)}

    req = requests.get(movie['link'])

    soup = BeautifulSoup(req.text, 'lxml')

    movie['name'] = soup.find('h1', class_='KOq_N').findAll('span')[-1].text
    year_text = soup.find('h2', class_='_3Di4D _2qUBY').find('span').text
    year_text = year_text.split('(')[1] if '(' in year_text else year_text
    movie['year'] = year_text.split(',')[0]

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

    return movie
