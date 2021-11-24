
from getFilmData import getFilmData
import json

def getFilmDictList():
    database = 'film database.json'
    with open(database, 'r') as f:
        return json.load(f)

def testTitle(search_query):
    film_dict = getFilmData(search_query)
    print(json.dumps(film_dict, indent=4), end='')
    print(',')

def ratingRank():
    film_dict_list = getFilmDictList()
    film_dict_list = sorted(film_dict_list, key=lambda x: x['rating'], reverse=True)
    tuple_list = []
    for i in film_dict_list:
        ratingTuple = (i['title'], i['rating'])
        tuple_list.append(ratingTuple)
        print(ratingTuple)
    return tuple_list

def runtimeRank():
    film_dict_list = getFilmDictList()
    film_dict_list = sorted(film_dict_list, key=lambda x: x['runtimeMins'], reverse=True)
    tuple_list = []
    for i in film_dict_list:
        runtimeTuple = (i['title'], i['runtimeString'])
        tuple_list.append(runtimeTuple)
        print(runtimeTuple)
    return tuple_list

def directorFreq():
    director_list = [i['director'][j] for i in getFilmDictList() for j in range(len(i['director']))]
    freq_dict = {}
    for i in director_list:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[0].split()[-1])}
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    print(json.dumps(freq_dict, indent=4))
    return freq_dict

def containDirector(director):
    title_list = []
    for i in getFilmDictList():
        director_list = [j.casefold() for j in i['director']]
        if director.casefold() in director_list:
            title_list.append(i['title'])
    if len(title_list) > 0:
        for i in title_list:
            print(i)
    else:
        print("NO FILMS")

def leadFreq():
    all_actors = [i['stars'][j] for i in getFilmDictList() for j in range(len(i['stars']))]
    freq_dict = {}
    for i in all_actors:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[0].split()[-1])}
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    print(json.dumps(freq_dict, indent=4))
    return freq_dict

def actorFreq():
    all_actors = []
    for i in getFilmDictList():
        for j in i['stars']:
            all_actors.append(j)
        for j in i['cast']:
            all_actors.append(j)
    freq_dict = {}
    for i in all_actors:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[0].split()[-1])}
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    print(json.dumps(freq_dict, indent=4))
    return freq_dict

def containLead(actor):
    title_list = []
    for i in getFilmDictList():
        actor_list = [j.casefold() for j in i['stars']]
        if actor.casefold() in actor_list:
            title_list.append(i['title'])
    if len(title_list) > 0:
        for i in title_list:
            print(i)
    else:
        print("NO FILMS")

def containActor(actor):
    title_list = []
    for i in getFilmDictList():
        lead_list = [j.casefold() for j in i['stars']]
        cast_list = [j.casefold() for j in i['cast']]
        if actor.casefold() in lead_list or actor.casefold() in cast_list:
            title_list.append(i['title'])
    if len(title_list) > 0:
        for i in title_list:
            print(i)
    else:
        print("NO FILMS")

def budgetRank():
    film_dict_list = [i for i in getFilmDictList() if i['budget'][0] == '$']
    film_dict_list = sorted(film_dict_list, key=lambda x: int(x['budget'].strip('$').replace(',', '')))
    rankList = []
    for i in film_dict_list:
        film_dict = {}
        film_dict['title'] = i['title']
        film_dict['rating'] = i['rating']
        film_dict['budget'] = i['budget']
        film_dict['gross'] = i['gross']
        film_dict['budgetInt'] = int(i['budget'].strip('$').replace(',', ''))
        if '$' in film_dict['gross']:
            film_dict['grossInt'] = int(i['gross'].strip('$').replace(',', ''))
        else:
            film_dict['grossInt'] = -1
        rankList.append(film_dict)
        print(json.dumps(film_dict, indent=4), end=',\n')
    return rankList

def grossRank():
    film_dict_list = [i for i in getFilmDictList() if i['gross'][0] == '$']
    film_dict_list = sorted(film_dict_list, key=lambda x: int(x['gross'].strip('$').replace(',', '')))
    rankList = []
    for i in film_dict_list:
        film_dict = {}
        film_dict['title'] = i['title']
        film_dict['budget'] = i['budget']
        film_dict['gross'] = i['gross']
        rankList.append(film_dict)
        print(json.dumps(film_dict, indent=4), end=',\n')

def profitRank():
    film_dict_list = [i for i in getFilmDictList() if i['budget'][0] == '$' and i['gross'][0] == '$']
    film_dict_list = sorted(film_dict_list, key=lambda x: int(x['gross'].strip('$').replace(',', '')) - int(x['budget'].strip('$').replace(',', '')))
    rankList = []
    for i in film_dict_list:
        film_dict = {}
        film_dict['title'] = i['title']
        film_dict['budget'] = i['budget']
        film_dict['gross'] = i['gross']
        intProfit = int(film_dict['gross'].strip('$').replace(',', '')) - int(film_dict['budget'].strip('$').replace(',', ''))
        sepString = format(intProfit, ',')
        if sepString[0] == '-':
            profit = '-$' + sepString[1:]
        else:
            profit = '$' + sepString
        film_dict['profit'] = profit
        rankList.append(film_dict)
        print(json.dumps(film_dict, indent=4), end=',\n')
    return rankList

def profitRatioRank():
    film_dict_list = [i for i in getFilmDictList() if i['budget'][0] == '$' and i['gross'][0] == '$']
    film_dict_list = sorted(film_dict_list, key=lambda x: int(x['gross'].strip('$').replace(',', '')) / int(x['budget'].strip('$').replace(',', '')))
    rankList = []
    for i in film_dict_list:
        film_dict = {}
        film_dict['title'] = i['title']
        film_dict['budget'] = i['budget']
        film_dict['gross'] = i['gross']
        film_dict['ratio'] = 'x' + str(round(int(film_dict['gross'].strip('$').replace(',', '')) / int(film_dict['budget'].strip('$').replace(',', '')), 2))
        rankList.append(film_dict)
        print(json.dumps(film_dict, indent=4), end=',\n')
    return rankList

def classFreq():
    all_class = [i['classification'] for i in getFilmDictList()]
    freq_dict = {}
    for i in all_class:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    class_order = ['G', 'PG', 'M', 'MA15+', 'R',  'MA', 'A', 'NRC', '']
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda x: class_order.index(x[0]))}
    freq_dict['R'] += freq_dict['MA']
    freq_dict.pop('MA')
    print(json.dumps(freq_dict, indent=4))
    return freq_dict

def containClass(classification):
    title_list = [i['title'] for i in getFilmDictList() if i['classification'].casefold() == classification.casefold()]
    if len(title_list) > 0:
        for i in title_list:
            print(i)
    else:
        print("NO FILMS")

def composerFreq():
    all_class = [i['music'][j] for i in getFilmDictList() for j in range(len(i['music']))]
    freq_dict = {}
    for i in all_class:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    print(json.dumps(freq_dict, indent=4))
    return freq_dict

def containComposer(composer):
    title_list = [i['title'] for i in getFilmDictList() for j in range(len(i['music'])) if i['music'][j].casefold() == composer.casefold()]
    if len(title_list) > 0:
        for i in title_list:
            print(i)
    else:
        print('NO FILMS')

def yearFreq():
    all_class = [i['year'] for i in getFilmDictList()]
    freq_dict = {}
    for i in all_class:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[0], reverse=True)}
    print(json.dumps(freq_dict, indent=4))
    return freq_dict

def containYear(*year):
    if len(year) <= 2:
        if len(year) == 2:
            if year[0] > year[1]:
                year[0], year[1] = year[1], year[0]
            year_list = [i for i in getFilmDictList() if year[0] <= i['year'] <= year[1]]
            year_list = [i['title'] for i in sorted(year_list, key=lambda x: x['year'], reverse=True)]
        else:
            year_list = [i['title'] for i in getFilmDictList() if i['year'] == year[0]]
        if len(year_list) > 0:
            for i in year_list:
                print(i)
        else:
            print('NO FILMS')
    else:
        print('INVALID ENTRY')

def genreFreq():
    genre_list = [i['genre'][j] for i in getFilmDictList() for j in range(len(i['genre']))]
    freq_dict = {}
    for i in genre_list:
        if i in freq_dict:
            freq_dict[i] += 1
        else:
            freq_dict[i] = 1
    freq_dict = {k: v for k, v in sorted(freq_dict.items(), key=lambda item: item[1], reverse=True)}
    print(json.dumps(freq_dict, indent=4))
    return freq_dict


# testTitle('crouching tiger hidden dragon')
# containYear(1980, 1990)
genreFreq()
#budgetRank()
#containClass('ma15+')
#testTitle('toy story 4')
#containDirector('hayao miyazaki')
#ratingRank()

# containActor("will smith")

