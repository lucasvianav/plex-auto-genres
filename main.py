from src.args import GENERATE, SET_POSTERS, LIBRARY, TYPE, NO_PROMPT, SORT
from src.colors import bcolors
from src.setup import PLEX_COLLECTION_PREFIX, PLEX_SERVER_NAME, PLEX_BASE_URL
from src.util import confirm
from src.plex import *

plex = plexConnect()

if GENERATE:
    CONFIRMATION = f'\nYou are about to create [{bcolors.WARNING}{TYPE}{bcolors.ENDC}] genre collection tags for the library [{bcolors.WARNING}{LIBRARY}{bcolors.ENDC}] on your server [{bcolors.WARNING}{(PLEX_SERVER_NAME or PLEX_BASE_URL)}{bcolors.ENDC}].'
    if PLEX_COLLECTION_PREFIX: CONFIRMATION += 'With prefix ['+bcolors.WARNING+PLEX_COLLECTION_PREFIX+bcolors.ENDC+'].'
    
    print(CONFIRMATION)
    if NO_PROMPT or confirm(): genCollections(plex)

if SET_POSTERS:
    print(f'You are about to update your {bcolors.WARNING}[{LIBRARY}]{bcolors.ENDC} collection\'s posters to any matching image titles located at {bcolors.WARNING}posters/{TYPE}/{bcolors.ENDC}.')
    if NO_PROMPT or confirm(): updatePosters(plex)

if SORT:
    print(f'\nYou are about to sort all [{bcolors.WARNING}{TYPE}{bcolors.ENDC}] collections in the library [{bcolors.WARNING}{LIBRARY}{bcolors.ENDC}] on your server [{bcolors.WARNING}{(PLEX_SERVER_NAME or PLEX_BASE_URL)}{bcolors.ENDC}].')
    if NO_PROMPT or confirm(): sortCollections(plex)

print()