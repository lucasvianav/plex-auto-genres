import json
import math
import os
from re import sub, search

from plexapi.myplex import MyPlexAccount, PlexServer

from src.args import DRY_RUN, LIBRARY, TYPE
from src.colors import bcolors
from src.genres import getGenres
from src.progress_bar import printProgressBar
from src.setup import (
    PLEX_BASE_URL,
    PLEX_COLLECTION_PREFIX,
    PLEX_PASSWORD,
    PLEX_SERVER_NAME,
    PLEX_TOKEN,
    PLEX_USERNAME,
    validateDotEnv
)
from src.util import *

validateDotEnv(TYPE)

def plexConnect():
    print('\nConnecting to Plex...')
    
    if PLEX_USERNAME is not None and PLEX_PASSWORD is not None and PLEX_SERVER_NAME is not None:
        account = MyPlexAccount(PLEX_USERNAME, PLEX_PASSWORD)
        plex = account.resource(PLEX_SERVER_NAME).connect()

    elif PLEX_BASE_URL is not None and PLEX_TOKEN is not None:
        plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN)

    else: raise Exception("No valid credentials found. See the README for more details.")
        
    return plex

def genCollections(plex):
    successfulMedia = []
    failedMedia = []

    if not DRY_RUN:
        if os.path.isfile(f'logs/plex-{TYPE}-successful.txt'):
            with open(f'logs/plex-{TYPE}-successful.txt', 'r') as f: successfulMedia = json.load(f)

        if os.path.isfile(f'logs/plex-{TYPE}-failures.txt'):
            with open(f'logs/plex-{TYPE}-failures.txt', 'r') as f: failedMedia = json.load(f)

    try:
        library = plex.library.section(LIBRARY).all()

        # media counters
        totalCount = len(library)
        unfinishedCount = len(list(filter(lambda media : media.title not in successfulMedia and media.title not in failedMedia, library)))
        finishedCount = totalCount - unfinishedCount

        # estimated time "of arrival"
        eta = ((unfinishedCount * getSleepTime(TYPE)) / 60) * 2

        if 'mixed-' in TYPE: 
            animeCount = len(list(filter(lambda media : media.title not in successfulMedia and isAnime(media), library)))
            nonAnimeCount = unfinishedCount - animeCount
            eta = ((animeCount * getSleepTime('anime') + nonAnimeCount * getSleepTime(TYPE)) / 60) * 2
        
        print(f'Found {totalCount} media entries under {LIBRARY} ({finishedCount}/{totalCount} completed).')
        print(f'Estimated time to completion: {math.ceil(eta)} minutes...\n')

        # i = current media's position
        for i, media in enumerate(library, 1):
            if media.title not in successfulMedia and media.title not in failedMedia:
                genres = getGenres(media, TYPE)

                if len(genres) == 0: failedMedia.append(media.title)

                else:
                    if not DRY_RUN:
                        for genre in genres:
                            genre = PLEX_COLLECTION_PREFIX + genre
                            media.addCollection(genre)

                    successfulMedia.append(media.title)

            printProgressBar(i, totalCount, prefix = 'Progress:', suffix = 'Complete', length = 50)

        if failedMedia: print(bcolors.FAIL + f'\nFailed to get genre information for {len(failedMedia)} entries. ' + bcolors.ENDC + f'See logs/plex-{TYPE}-failures.txt.')
        else: print(bcolors.OKGREEN + '\nSuccessfully got genre information for all entries. ' + bcolors.ENDC + f'See logs/plex-{TYPE}-successful.txt.')

    except KeyboardInterrupt: print('\n\nOperation interupted, progress has been saved.')

    # updates the finished and failures txt
    if not DRY_RUN:
        if successfulMedia:
            with open(f'logs/plex-{TYPE}-successful.txt', 'w') as f: json.dump(successfulMedia, f)

        if failedMedia:
            with open(f'logs/plex-{TYPE}-failures.txt', 'w') as f: json.dump(failedMedia, f)

    return

def updatePosters(plex):
    type = sub('^\S*-', '', type)
    postersDir = os.getcwd() + f'/posters/{type}'

    if not os.path.isdir(postersDir):
        print(bcolors.FAIL + f'Could not find poster art directory. Expected location: {postersDir}.' + bcolors.ENDC)
        return

    collections = plex.library.section(LIBRARY).collection()

    if not collections:
        print(bcolors.FAIL + f'Could not find any Plex collections.' + bcolors.ENDC)
        return

    print('\nUploading collection artwork...')

    for c in collections:
        # remove prefix characters and replace spaces with dashes
        title = sub(f'^{PLEX_COLLECTION_PREFIX}', '', c.title).replace(' ', '-')

        # path to the image
        posterPath = f'{postersDir}/{title.lower()}.png'

        if os.path.isfile(posterPath):
            print(f'Uploading {title}...', end='\r')

            c.uploadPoster(filepath=posterPath)

            print(f'Uploading {title}... {bcolors.OKGREEN}done!{bcolors.ENDC}', end='\r')
            print()

        else: print (f'No poster found for collection {bcolors.WARNING}{title}{bcolors.ENDC}, expected {bcolors.WARNING}posters/{type}/{title.lower()}.png{bcolors.ENDC}.')

    return

def sortCollections(plex):
    collections = plex.library.section(LIBRARY).collection()

    if not collections:
        print(bcolors.FAIL + f'Could not find any Plex collections.' + bcolors.ENDC)
        return

    totalCount = len(collections)

    print('\nUpdating collections\' sorting order...\n')

    for i, collection in enumerate(collections, 1):
        collectionItem = plex.fetchItem(collection.ratingKey)

        if collectionItem.title == 'Anime': edits = {'editSort.value': '02', 'editSort.locked': 1}
        elif collectionItem.title == 'Non-Anime': edits = {'editSort.value': '01', 'editSort.locked': 1}
        elif search('^\[A]\s.+', collectionItem.title): edits = {'editSort.value': 'zzzzzz' + sub('^\[A]\s', '', collectionItem.title), 'editSort.locked': 1}
        else: continue

        if not DRY_RUN:
            collectionItem.edit(**edits)
            collectionItem.reload()

        printProgressBar(i, totalCount, prefix = 'Progress:', suffix = 'Complete', length = 50)

    print(bcolors.OKGREEN + '\nSuccessfully update the collections\' sorting order.' + bcolors.ENDC)

    return