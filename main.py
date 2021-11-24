
from getFilmData import getFilmData
from fileCheck import getMovieList
import json

# Things to do
# Selenium
# - foreign titles
# - incorrect classification
# - Katia's movie list


# files commented to avoid overwriting file
database = 'film database.json'
movie_file = 'movies I have seen.txt'
failed_queries_file = 'failed search queries.txt'
double_attempts_file = 'double attempts.txt'

all_films, movieCount = getMovieList(movie_file)
failed_search_queries = []
film_link_array = []
double_attempts = []
film_dict_list = []

print('\n' + movie_file)
print('->', database)
print('\n' + movieCount)

for index in range(len(all_films)):
    try:
        film_dict = getFilmData(all_films[index])
        if film_dict['link'] in film_link_array:
            print('DOUBLE RECORD ATTEMPTED:', film_dict['title'])
            double_attempts.append(all_films[index])
        else:
            film_link_array.append(film_dict['link'])
            film_dict_list.append(film_dict)
            print(json.dumps(film_dict, indent=4))
    except:
        print('FAILED QUERY')
        print('failure:', all_films[index])
        failed_search_queries.append(all_films[index])

film_dict_list = sorted(film_dict_list, key=lambda film_dict: film_dict['title'])
with open(database, 'w') as f:
    f.write('[')
    for i in range(len(film_dict_list)):
        json.dump(film_dict_list[i], f, indent=4)
        if i != len(film_dict_list) - 1:
            f.write(',\n')
    f.write(']')

with open(failed_queries_file, 'w') as f:
    for i in failed_search_queries:
        f.write(i + '\n')

with open(double_attempts_file, 'w') as f:
    for i in double_attempts:
        f.write(i + '\n')
