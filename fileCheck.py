
def getMovieList(file):

    with open(file) as f:
        lines = f.readlines()

    movieCount = 0
    movieList = []
    for i in lines:
        if i != '\n' and i[0] != '-':
            movieCount += 1
            movieList.append(i.strip('\n'))
    return movieList, movieCount

