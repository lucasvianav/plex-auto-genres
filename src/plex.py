import sys

from plexapi.myplex import MyPlexAccount, PlexServer

from setup import (
    PLEX_BASE_URL, 
    PLEX_PASSWORD, 
    PLEX_SERVER_NAME, 
    PLEX_TOKEN, 
    PLEX_USERNAME
)


def plexConnect():
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
