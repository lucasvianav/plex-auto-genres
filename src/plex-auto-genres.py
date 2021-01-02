import os
import sys
import math
import time
import json
import datetime
from plexapi.myplex import MyPlexAccount, PlexServer
from colors import bcolors
from setup import *
from args import LIBRARY, TYPE, DRY_RUN, SET_POSTERS
from progress_bar import printProgressBar

validateDotEnv(TYPE)

def connect_to_plex():
    print('\nConnecting to Plex...')
    try:
        if PLEX_USERNAME is not None and PLEX_PASSWORD is not None and PLEX_SERVER_NAME is not None:
            account = MyPlexAccount(PLEX_USERNAME, PLEX_PASSWORD)
            plex = account.resource(PLEX_SERVER_NAME).connect()
        elif PLEX_BASE_URL is not None and PLEX_TOKEN is not None:
            plex = PlexServer(PLEX_BASE_URL, PLEX_TOKEN)
        else:
            raise Exception("No valid credentials found. See the README for more details.")
    except Exception as e:
        print(str(e))
        sys.exit(0)
    return plex


def get_sleep_time(type):
    if type == 'standard-movies':
        return 1 # tmdb doesn't have a rate limit, but we sleep for 0.5 anyways
    elif type == 'standard-shows':
        return 1 # tmdb
    else:
        return 8 #Jikan fetch requires 2 request with a 4 second sleep on each request

def fetch_anime(title):
    title = title.split(' [')[0]
    if len(title.split()) > 10:
        title = " ".join(title.split()[0:10])
    time.sleep(4)
    search_result = jikan.search('anime', title, page=1)
    result_id = search_result['results'][0]['mal_id']
    time.sleep(4)
    anime_jikan = jikan.anime(result_id)
    genres = anime_jikan['genres']
    genres_list = []
    for genre in genres:
        genres_list.append(genre['name'])
    return genres_list

def fetch_standard(title, type):
    try:
        if type == 'standard-movies':
            db = movie
        else:
            db = tv
        time.sleep(0.5)
        search = db.search(title)
        if len(search) == 0:
            return []
        time.sleep(0.5)
        details = db.details(search[0].id)
        genre_list = []
        for genre in details.genres:
            genre_list.extend(genre['name'].split(' & '))
        return genre_list
    except Exception as e:
        print('\n\n{}, when searching for entry: {}, of type {}\nThis entry has been added to the failures.txt once the issue is corrected in your library remove the entry from failures.txt and try again.'.format(str(e), title, type))
        return []

def generate():
    plex = connect_to_plex()
    finished_media = []
    failed_media = []
    if not DRY_RUN:
        if os.path.isfile('plex-'+TYPE+'-finished.txt'):
            with open('plex-'+TYPE+'-finished.txt') as save_data:
                finished_media = json.load(save_data)
        if os.path.isfile('plex-'+TYPE+'-failures.txt'):
            with open('plex-'+TYPE+'-failures.txt') as save_data:
                failed_media = json.load(save_data)
    try:
        medias = plex.library.section(LIBRARY).all()
        total_count = len(medias)
        unfinished_count = 0
        for m in medias:
            if m.title not in finished_media:
                unfinished_count += 1
        finished_count = total_count - unfinished_count

        eta = ((unfinished_count * get_sleep_time(TYPE)) / 60) * 2
        time_now = datetime.datetime.now()
        time_done = time_now + datetime.timedelta(minutes=eta)
        print("Found {} media entries under {} ({}/{} completed), estimated time to completion ~{} minutes ({})...\n".format(total_count, LIBRARY, finished_count, total_count, math.ceil(eta), time_done.strftime("%I:%M %p")))

        working_index = 0
        for m in medias:
            working_index += 1
            if m.title in finished_media or m.title in failed_media:
                printProgressBar(working_index, total_count, prefix = 'Progress:', suffix = 'Complete', length = 50)
                continue
            if TYPE == 'anime':
                genres = fetch_anime(m.title)
            else:
                genres = fetch_standard(m.title, TYPE)

            if len(genres) == 0:
                failed_media.append(m.title)
                continue
            if not DRY_RUN:
                for genre in genres:
                    if len(PLEX_COLLECTION_PREFIX) > 0:
                        genre = PLEX_COLLECTION_PREFIX + genre
                    m.addCollection(genre.strip())

            finished_media.append(m.title)
            printProgressBar(working_index, total_count, prefix = 'Progress:', suffix = 'Complete', length = 50)
        print('\n'+bcolors.FAIL+'Failed to get genre information for '+str(len(failed_media))+' entries. '+bcolors.ENDC+'See '+'plex-'+TYPE+'-failures.txt')

    except KeyboardInterrupt:
        print('\n\nOperation interupted, progress has been saved.')
        pass
    except Exception as e:
        print(str(e))

    if not DRY_RUN:
        if len(finished_media) > 0:
            with open('plex-'+TYPE+'-finished.txt', 'w') as filehandle:
                json.dump(finished_media, filehandle)
        if len(failed_media) > 0:
            with open('plex-'+TYPE+'-failures.txt', 'w') as filehandle:
                json.dump(failed_media, filehandle)
    
    sys.exit(0)


def confirm():
    acceptable_responses = ['y', 'n', 'Y', 'N']
    response = ""
    while (response not in acceptable_responses):
        response = input(bcolors.WARNING+"Continue? y/n..."+bcolors.ENDC)
    if response == 'y' or response == 'Y':
        return True
    else:
        return False

def upload_collection_art():
    #collection_name, libtype='collection'
    if not os.path.isdir(f'{os.getcwd()}/posters/{TYPE}'):
        print(f'{bcolors.FAIL}Could not find poster art directory. Expected location {os.getcwd()}/posters/{TYPE}{bcolors.ENDC}')
        sys.exit(1)
    plex = connect_to_plex()
    collections = plex.library.section(LIBRARY).collection()
    print('\nUploading collection artwork...')
    for c in collections:
        # remove prefix characters
        title = c.title.lower()
        if title[0] == PLEX_COLLECTION_PREFIX:
            title = title[1:]
        # replace spaces with dashes
        title = title.replace(' ', '-')
        poster_path = f'{os.getcwd()}/posters/{TYPE}/{title}.png'
        if os.path.isfile(poster_path):
            print(f'Uploading {title}...', end='\r')
            c.uploadPoster(filepath=poster_path)
            print(f'Uploading {title}... {bcolors.OKGREEN}done!{bcolors.ENDC}', end='\r')
            print()
        else:
            print (f'No poster found for collection {bcolors.WARNING}{title}{bcolors.ENDC}, expected {bcolors.WARNING}posters/{TYPE}/{title}.png{bcolors.ENDC}')

if __name__ == '__main__':
    if not SET_POSTERS:
        CONFIRMATION = "\nYou are about to create ["+bcolors.WARNING+TYPE+bcolors.ENDC+"] genre collection tags for the library ["+bcolors.WARNING+LIBRARY+bcolors.ENDC+"] on your server ["+bcolors.WARNING+(PLEX_SERVER_NAME or PLEX_BASE_URL)+bcolors.ENDC+"]."
        if len(PLEX_COLLECTION_PREFIX) > 0:
            CONFIRMATION += "With prefix ["+bcolors.WARNING+PLEX_COLLECTION_PREFIX+bcolors.ENDC+"]."
        print(CONFIRMATION)
        if confirm():
            generate()

    if SET_POSTERS:
        print(f'You are about to update your {bcolors.WARNING}[{LIBRARY}]{bcolors.ENDC} collection posters to any matching image titles located at {bcolors.WARNING}posters/{TYPE}/{bcolors.ENDC}')
        if confirm():
            upload_collection_art()