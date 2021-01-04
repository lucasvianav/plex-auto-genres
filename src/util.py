from re import search

from src.colors import bcolors


# tmdb doesn't have a rate limit, but we sleep for 0.5 anyways
# Jikan fetch requires 2 request with a 4 second sleep on each request
def getSleepTime(type: str): return 1 if search('^\S*shows$|^\S*movies$', type) else 8

def confirm():
    while True: 
        response = input(bcolors.WARNING + "Continue? y/n... " + bcolors.ENDC)

        if response.lower() == 'y': return True
        elif response.lower() == 'n': return False

def isAnime(media):
    if media.type == 'movie':
        media.labels
        countries = [e.tag for e in media.countries]
        genres = [e.tag for e in media.genres]

        return True if 'Anime' in genres or ('Animation' in genres and 'Japan' in countries) else False

    elif media.type == 'show':
        media.labels
        genres = [e.tag for e in media.genres]

        return True if 'Anime' in genres else False