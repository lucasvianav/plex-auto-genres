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
    print(bcolors.OKBLUE + '\nConnecting to Plex...' + bcolors.ENDC, end = ' ')
    
    # Checks username, password and server name
    if PLEX_USERNAME is not None and PLEX_PASSWORD is not None and PLEX_SERVER_NAME is not None:
        try:
            account = MyPlexAccount(PLEX_USERNAME, PLEX_PASSWORD)
            plex = account.resource(PLEX_SERVER_NAME).connect()

        except Exception as e:
            raise Exception(f'{bcolors.FAIL}failed!{bcolors.ENDC} {bcolors.WARNING}See error:{bcolors.ENDC} {e}')

        else:
            print(f'{bcolors.OKGREEN}done!{bcolors.ENDC}')

    # Alternatively, checks base url and plex auth token
    elif PLEX_BASE_URL is not None and PLEX_TOKEN is not None:
        try: plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN)
        
        except Exception as e:
            raise Exception(f'{bcolors.FAIL}failed!{bcolors.ENDC} {bcolors.WARNING}See error:{bcolors.ENDC} {e}')

        else:
            print(f'{bcolors.OKGREEN}done!{bcolors.ENDC}')

    else: raise Exception(f"{bcolors.FAIL}failed!{bcolors.ENDC} {bcolors.WARNING}No valid credentials found.{bcolors.ENDC} See the README for more details.")
        
    return plex

def genCollections(plex):
    successfulMedia = [] # media which's collections were successfully edited
    failedMedia = [] # media which's collections couldn't be edited

    # if it's not a dry-run, gets progress from the logs
    if not DRY_RUN:
        # if the 
        if not os.path.isdir('./logs'): os.mkdir('./logs')

        if os.path.isfile(f'logs/plex-{TYPE}-successful.txt'):
            with open(f'logs/plex-{TYPE}-successful.txt', 'r') as f: successfulMedia = json.load(f)

        if os.path.isfile(f'logs/plex-{TYPE}-failures.txt'):
            with open(f'logs/plex-{TYPE}-failures.txt', 'r') as f: failedMedia = json.load(f)

    try:
        # plex library
        library = plex.library.section(LIBRARY).all()

        # media counters
        totalCount = len(library)
        unfinishedCount = len(list(filter(lambda media: f'{media.title} ({media.year})' not in successfulMedia and f'{media.title} ({media.year})' not in failedMedia, library)))
        finishedCount = totalCount - unfinishedCount

        # estimated time "of arrival"
        eta = ((unfinishedCount * getSleepTime(TYPE)) / 60) * 2

        # if it's a mixed type, corrects the ETA
        if 'mixed-' in TYPE: 
            animeCount = len(list(filter(lambda media : f'{media.title} ({media.year})' not in successfulMedia and f'{media.title} ({media.year})' not in failedMedia and isAnime(media), library)))
            nonAnimeCount = unfinishedCount - animeCount
            eta = ((animeCount * getSleepTime('anime') + nonAnimeCount * getSleepTime(TYPE)) / 60) * 2
        
        print(f'Found {totalCount} media entries under {LIBRARY} ({finishedCount}/{totalCount} completed).')
        print(f'Estimated time to completion: {math.ceil(eta)} minutes...\n')

        # i = current media's position
        for i, media in enumerate(library, 1):
            mediaIdentifier = f'{media.title} ({media.year})'

            if mediaIdentifier not in successfulMedia and mediaIdentifier not in failedMedia:
                genres = getGenres(media, TYPE)

                if not genres: failedMedia.append(mediaIdentifier)

                else:
                    if not DRY_RUN:
                        for genre in genres:
                            genre = PLEX_COLLECTION_PREFIX + genre
                            media.addCollection(genre)

                    successfulMedia.append(mediaIdentifier)

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
    type = sub('^\S*-', '', TYPE) # standard-movies or mixed-movies --> movies (same for shows)
    postersDir = os.getcwd() + f'/posters/{type}' # complete path to the posters directory

    # if there is no posters/ directory
    if not os.path.isdir(postersDir):
        print(bcolors.FAIL + f'Could not find poster art directory. Expected location: {postersDir}.' + bcolors.ENDC)
        return

    collections = plex.library.section(LIBRARY).collection()

    # if there are no collections (same as len(collections) == 0)
    if not collections:
        print(bcolors.FAIL + f'Could not find any Plex collections.' + bcolors.ENDC)
        return

    print('\nUploading collection artwork...')

    for c in collections:
        # remove prefix characters and replace spaces with dashes
        title = sub(f'^{PLEX_COLLECTION_PREFIX}', '', c.title)

        # path to the image
        posterPath = f'{postersDir}/' + title.lower().replace(' ', '-') + '.png'

        # if it's a mixed library, look for the anime genre collections ('[A] ...') and the Anime and Non-Anime collections
        if 'mixed-' in TYPE:
            if search('^\[A]-.+', title): posterPath = sub(f'{type}$', 'anime', postersDir) + '/' + sub('^\[A]-', '', title).lower().replace(' ', '-') + '.png'
            elif search('^.*Anime$', title): posterPath = sub(f'{type}$', 'general', postersDir) + '/' + title.lower().replace(' ', '-') + '.png'

        # If the poster exists, upload it
        if os.path.isfile(posterPath):
            print(f'Uploading {title}...', end = ' ')
            
            try: c.uploadPoster(filepath = posterPath)
            except Exception as e: print(f'{bcolors.FAIL}failed!{bcolors.ENDC} {bcolors.WARNING}See error:{bcolors.ENDC}{e}')
            else: print(f'{bcolors.OKGREEN}done!{bcolors.ENDC}')

        # If it doesn't, print 404
        else: print (f'No poster found for collection {bcolors.WARNING}{title}{bcolors.ENDC}, expected {bcolors.WARNING}' + sub(f'^{os.getcwd()}','',posterPath) + f'{bcolors.ENDC}.')

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

        printProgressBar(i, totalCount, prefix = 'Progress:', suffix = 'Complete', length = 50)

        if collectionItem.title == 'Anime': edits = {'titleSort.value': '02', 'titleSort.locked': 1}
        elif collectionItem.title == 'Non-Anime': edits = {'titleSort.value': '01', 'titleSort.locked': 1}
        elif search('^\[A]\s.+', collectionItem.title): edits = {'titleSort.value': 'zzzzzz' + sub('^\[A]\s', '', collectionItem.title), 'titleSort.locked': 1}
        else: continue

        if not DRY_RUN:
            collectionItem.edit(**edits)
            collectionItem.reload()


    print(bcolors.OKGREEN + '\nSuccessfully update the collections\' sorting order.' + bcolors.ENDC)

    return