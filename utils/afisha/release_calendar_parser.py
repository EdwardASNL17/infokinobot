import requests
from aiogram.utils.markdown import hlink
from bs4 import BeautifulSoup


async def parsing_releases(url):
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

    return movies
