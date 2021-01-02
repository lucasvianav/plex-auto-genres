from args import SET_POSTERS, LIBRARY
from colors import bcolors
from setup import TYPE, PLEX_COLLECTION_PREFIX, PLEX_SERVER_NAME, PLEX_BASE_URL
from util import confirm
from plex import genCollections, updatePosters
from re import sub
from os import getcwd

if SET_POSTERS:
    print(f'You are about to update your {bcolors.WARNING}[{LIBRARY}]{bcolors.ENDC} collection\'s posters to any matching image titles located at {bcolors.WARNING}posters/{TYPE}/{bcolors.ENDC}.')
    if confirm(): updatePosters()

else:
    CONFIRMATION = f'\nYou are about to create [{bcolors.WARNING}{TYPE}{bcolors.ENDC}] genre collection tags for the library [{bcolors.WARNING}{LIBRARY}{bcolors.ENDC}] on your server [{bcolors.WARNING}{(PLEX_SERVER_NAME or PLEX_BASE_URL)}{bcolors.ENDC}].'
    if PLEX_COLLECTION_PREFIX: CONFIRMATION += 'With prefix ['+bcolors.WARNING+PLEX_COLLECTION_PREFIX+bcolors.ENDC+'].'
    
    print(CONFIRMATION)
    if confirm(): genCollections()