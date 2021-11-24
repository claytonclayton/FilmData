from getFilmData import getFilmData
from fileCheck import getMovieList
import json

def addNewMovie():
    movieFile = 'movies I have seen.txt'
    database = 'film database.json'

    with open(database, 'r') as f:
        all_film_dicts = json.load(f)
        link_list = [i['link'] for i in all_film_dicts]

    with open(movieFile, 'r') as f:
        all_movies = [i[:-1] for i in f.readlines()]

    final_say = 'n'
    while final_say == 'n':
        searchSuccess = False
        search_query = input("\nEnter a new movie: ")
        while not searchSuccess:
            try:
                print('loading...')
                film_dict = getFilmData(search_query)
            except:
                film_dict = ''
                print("ERROR: FILM NOT FOUND")
                search_query = input("Enter a new movie: ")
            if film_dict:
                searchSuccess = True

        print(json.dumps(film_dict, indent=4), end='')
        print(',')

        valid_responses = ['y', 'n']
        print('\nWould you like to add this film to the collection?')
        final_say = input("Type 'y' or 'n': ")
        while final_say not in valid_responses:
            print("INVALID RESPONSE")
            print('\nWould you like to add this film to the collection?')
            final_say = input("Type 'y' or 'n': ")

        if film_dict['link'] in link_list:
            print('This film is already in the collection')
            final_say = 'n'

    all_film_dicts.append(film_dict)
    all_film_dicts = sorted(all_film_dicts, key=lambda x: x['title'].casefold())
    all_movies.append(search_query)
    all_movies = sorted(all_movies, key=lambda i: i.casefold())
    with open(movieFile, 'w') as f:
        for i in all_movies:
            f.write(i + '\n')
    with open(database, 'w') as f:
        f.write('[')
        for i, movie in enumerate(all_film_dicts):
            f.write(',\n' * (i > 0))
            json.dump(movie, f, indent=4)
        f.write(']')
    print('\nsuccess. film added')

addNewMovie()