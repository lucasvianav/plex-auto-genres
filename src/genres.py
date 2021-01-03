import re
from time import sleep

from src.setup import jikan, movie, tv


def getAnimeGenres(title):
    title = title.split(' [')[0]
    if len(title.split()) > 10: title = " ".join(title.split()[0:10])

    sleep(4) # sleeps 4s
    
    query = jikan.search('anime', title, page=1) # search result
    id = query['results'][0]['mal_id'] # anime's MyAnimeList ID
    
    sleep(4)

    anime = jikan.anime(id) # all of the anime's info
    genres = [ e['name'] for e in anime['genres'] ] # list comprehension

    return genres

def getStandardGenres(title, type):
    try:
        db = movie if re.search('^\S+movies$', type) else tv

        sleep(0.5)

        query = db.search(title)
        if len(query) == 0: return []

        sleep(0.5)

        details = db.details(query[0].id)
        genres = [ e['name'].split(' & ') for e in details.genres ]
        
        return genres

    except Exception as e:
        print(f'\n\n{str(e)}, when searching for entry: {title}, of type {type}.')
        print('This entry has been added to the failures.txt - once the issue is corrected in your library remove it from there and try again.')
        
        return []

def getGenres(title, type): return getAnimeGenres(title) if type == 'anime' else getStandardGenres(title, type)
