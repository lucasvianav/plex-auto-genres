from colors import bcolors
from re import search

# tmdb doesn't have a rate limit, but we sleep for 0.5 anyways
# Jikan fetch requires 2 request with a 4 second sleep on each request
def getSleepTime(type: str): return 1 if search('^\S+shows$|^\S+movies$', type) else 8

def confirm():
    while True: 
        response = input(bcolors.WARNING + "Continue? y/n..." + bcolors.ENDC)

        if response.lower() == 'y': return True
        elif response.lower() == 'n': return False