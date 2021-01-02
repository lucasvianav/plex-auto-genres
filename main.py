from args import SET_POSTERS, LIBRARY
from colors import bcolors
from setup import TYPE, PLEX_COLLECTION_PREFIX, PLEX_SERVER_NAME, PLEX_BASE_URL
from util import confirm
from plex import genCollections, updatePosters

if not SET_POSTERS:
    CONFIRMATION = "\nYou are about to create ["+bcolors.WARNING+TYPE+bcolors.ENDC+"] genre collection tags for the library ["+bcolors.WARNING+LIBRARY+bcolors.ENDC+"] on your server ["+bcolors.WARNING+(PLEX_SERVER_NAME or PLEX_BASE_URL)+bcolors.ENDC+"]."
    if len(PLEX_COLLECTION_PREFIX) > 0:
        CONFIRMATION += "With prefix ["+bcolors.WARNING+PLEX_COLLECTION_PREFIX+bcolors.ENDC+"]."
    print(CONFIRMATION)
    if confirm():
        genCollections()

if SET_POSTERS:
    print(f'You are about to update your {bcolors.WARNING}[{LIBRARY}]{bcolors.ENDC} collection posters to any matching image titles located at {bcolors.WARNING}posters/{TYPE}/{bcolors.ENDC}')
    if confirm():
        updatePosters()
