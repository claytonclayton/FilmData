
import matplotlib.pyplot as plt
import numpy as np
import json
from statistics import leadFreq
from statistics import actorFreq
from statistics import classFreq
from statistics import yearFreq
from statistics import genreFreq
from statistics import budgetRank
from statistics import getFilmDictList

database = 'film database.json'

def leadPlot(n):
    topActors = leadFreq()
    all_names = list(topActors.keys())
    nameChunk = ''
    names = []
    for i, name in enumerate(all_names):
        if i > 0:
            if topActors[all_names[i - 1]] != topActors[all_names[i]]:
                nameChunk = nameChunk[:-1]
                names.append(nameChunk)
                nameChunk = ''
        if len(names) == n:
            break
        nameChunk += name + '\n'

    values = []
    all_values = list(topActors.values())
    for i in all_values:
        if i not in values:
            values.append(i)
        if len(values) == n:
            break

    values = values[::-1]
    names = names[::-1]

    # Nice Styles
    # seaborn-dark
    # seaborn-pastel
    # seaborn-whitegrid ?
    plt.rcParams.update({'figure.autolayout': True})
    plt.style.use('seaborn-dark')
    fig, ax = plt.subplots()
    ax.barh(names, values)
    labels = ax.get_xticklabels()
    # plt.setp(labels, rotation=45, horizontalalignment='right')
    ax.set(xlabel='Number of appearances', ylabel='Lead actors', title='Actors with most lead roles in films I have seen')
    print(plt.xlim())
    plt.show()


def actorPlot(n):
    topActors = actorFreq()
    all_names = list(topActors.keys())
    nameChunk = ''
    names = []
    for i, name in enumerate(all_names):
        if i > 0:
            if topActors[all_names[i - 1]] != topActors[all_names[i]]:
                nameChunk = nameChunk[:-1]
                names.append(nameChunk)
                nameChunk = ''
        if len(names) == n:
            break
        nameChunk += name + '\n'

    values = []
    all_values = list(topActors.values())
    for i in all_values:
        if i not in values:
            values.append(i)
        if len(values) == n:
            break

    values = values[::-1]
    names = names[::-1]

    plt.style.use('seaborn-whitegrid')
    fig, ax = plt.subplots()
    ax.barh(names, values)
    plt.show()

def classPlot():
    class_dict = {k: v for k, v in list(classFreq().items())[:5]}
    plt.style.use('seaborn-dark')
    plt.bar(*zip(*class_dict.items()))
    print(plt.style.available)
    plt.show()

def yearPlot():
    # plt.style.use('seaborn-dark')
    plt.bar(*zip(*yearFreq().items()))
    plt.xlabel('Years')
    plt.ylabel('Number of films made in each year')
    plt.title('')
    plt.show()

def genrePlot():
    # plt.style.use('seaborn-dark')
    genre_dict = {k: v for k, v in list(genreFreq().items())[:10]}
    plt.bar(*zip(*genre_dict.items()))
    plt.show()

def budgetGrossScatter():
    budget_list = []
    gross_list = []
    for i in budgetRank():
        if i['grossInt'] != -1:
            budget_list.append(i['budgetInt'])
            gross_list.append(i['grossInt'])
    #plt.style.use('seaborn-dark')
    plt.scatter(budget_list, gross_list)
    plt.show()

def budgetRatingScatter():
    budget_list = [i['budgetInt'] for i in budgetRank()]
    rating_list = [i['rating'] for i in budgetRank()]
    plt.scatter(budget_list, rating_list)
    plt.show()


def ISPlot():
    record_list = [25575, 30000, 30000, 30000, 30000]
    names = ['average\nrecords\nlost', 'cadt', 'cagt', 'caht', 'at3']
    # plt.style.use('seaborn-pastel')
    # plt.bar(names, record_list, color=(0.1, 0.1, 0.1, 0.1, 0.1))
    plt.bar(names, record_list)
    plt.show()

# classPlot()
# leadPlot(4)
# genrePlot()
# yearPlot()
# budgetGrossScatter()
# budgetRatingScatter()
ISPlot()
