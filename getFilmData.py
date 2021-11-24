
import requests
from bs4 import BeautifulSoup
import time

def getFilmData(search_query):
    t0 = time.perf_counter()

    film_dict = {}

    if search_query[0] != '/':
        search_url = f'https://www.imdb.com/find?q={search_query}&ref_=nv_sr_sm'
        search_html = requests.get(search_url).text
        soup = BeautifulSoup(search_html, 'lxml')
        film_link = soup.find('td', class_='result_text').a['href']
        film_site_url = f'https://www.imdb.com{film_link}'
        film_dict['link'] = film_link
    else:
        film_link = search_query
        film_site_url = f'https://www.imdb.com{search_query}'
        film_dict['link'] = film_link

    film_html = requests.get(film_site_url).text
    soup = BeautifulSoup(film_html, 'lxml')

    title_wrapper = soup.find('div', class_='title_wrapper')
    credit_summary_items = soup.find_all('div', class_='credit_summary_item')
    subtext = soup.find('div', class_='subtext')
    film_dict['title'] = title_wrapper.h1.text.replace(u'\u00A0', ' ').strip()
    film_dict['year'] = int(title_wrapper.span.text.strip('(').strip(')'))
    # film_dict['director'] = credit_summary_items[0].a.text
    film_dict['rating'] = float(soup.find('span', itemprop='ratingValue').text)
    film_dict['classification'] = subtext.find(text=True).strip()
    film_dict['runtimeString'] = subtext.time.text.strip()

    runtime_simple = film_dict['runtimeString'].replace('h', '').replace('min', '')
    hoursEnd = False
    hours = ''
    minutes = ''
    for i, char in enumerate(runtime_simple):
        if char == ' ':
            hoursEnd = True
        if not hoursEnd:
            hours += char
        else:
            minutes += char
    if minutes == '' and int(hours) > 3:
        film_dict['runtimeMins'] = int(hours)
    elif minutes == '':
        film_dict['runtimeMins'] = int(hours) * 60
    else:
        film_dict['runtimeMins'] = int(hours) * 60 + int(minutes)

    monies = soup.find_all('div', class_='txt-block')
    budgetSuccess = False
    grossSuccess = False
    for i in monies:
        try:
            inline = i.h4.text
            if inline == 'Budget:':
                budgetSuccess = True
                film_dict['budget'] = i.text.replace(' ', '').replace('\n', '').strip(inline).strip('(estimated)')
            if inline == 'Cumulative Worldwide Gross:':
                grossSuccess = True
                film_dict['gross'] = i.text.strip('\n').strip(inline)
        except:
            pass
    if not budgetSuccess:
        film_dict['budget'] = 'NA'
    if not grossSuccess:
        film_dict['gross'] = 'NA'

    genre_list = soup.find_all('div', class_='see-more inline canwrap')[1].find_all('a')
    genre_string = ''
    genre = []
    for i, genreSingle in enumerate(genre_list):
        genre_string += ', ' * (i > 0) + genreSingle.text.strip()
        genre.append(genreSingle.text.strip())
    film_dict['genre'] = genre

    stars_list = credit_summary_items[2].find_all('a')
    n = len(stars_list) - 1 * (len(stars_list) >= 4)
    stars_string = ''
    stars = []
    for i in range(n):
        stars_string += ', ' * (i > 0) + stars_list[i].text
        stars.append(stars_list[i].text)
    film_dict['stars'] = stars

    # look closer. len(actor) > 1 a little too unspecific
    cast_list = soup.find('table', class_='cast_list').find_all('tr')
    cast = []
    for i in cast_list:
        actor = i.find_all('td')
        if len(actor) > 1:
            actor = actor[1].text.strip()
            if actor not in stars:
                cast.append(actor)
    film_dict['cast'] = cast

    slashCount = 0
    link_section = ''
    for i, character in enumerate(film_link):
        link_section += character
        if character == '/':
            slashCount += 1
        if slashCount == 3:
            full_cast_link = 'https://www.imdb.com' + link_section + 'fullcredits/?ref_=tt_ov_st_sm'
            break

    full_cast_html = requests.get(full_cast_link).text
    soup = BeautifulSoup(full_cast_html, 'lxml')

    # x = soup.find('h4', id='director').find_next_sibling('table', class_='simpleTable simpleCreditsTable').text.strip()
    directors = soup.find('table', class_='simpleTable simpleCreditsTable').find_all('tr')
    film_dict['director'] = [i.find('td').text.strip() for i in directors]

    music_list = soup.find_all('table', class_='simpleTable simpleCreditsTable')[3].find_all('td', class_='name')
    music_string = ''
    music = []
    for i, composer in enumerate(music_list):
        music_string += ', ' * (i > 0) + composer.text.strip()
        music.append(composer.text.strip())
    film_dict['music'] = music

    # t2 = time.perf_counter()
    # print('code time:', t2 - t0)

    return film_dict

# film_dict = getFilmData('batman begins')
# print(json.dumps(film_dict, indent=2))