import argparse
import sys

from src.colors import bcolors

example_text = '\nexample command: ' + bcolors.BOLD +  'python3 main.py --library "Anime Shows" --type anime' + bcolors.ENDC
parser = argparse.ArgumentParser(description='Adds genre tags (collections) to your Plex media.', epilog = example_text)

parser.add_argument(
    '--library', action='store', dest='library', nargs=1, 
    help='The exact name of the Plex library to generate genre collections for.'
)

parser.add_argument(
    '--type', dest='type', action='store', choices=('anime', 'standard-movies', 'standard-shows', 'mixed-movies', 'mixed-shows'), 
    nargs=1, help='The type of media contained in the library'
)

parser.add_argument('--set-posters', help='Uploads posters located in posters/$media-type - media-type {anime, movies, shows}. Supports .PNG', action='store_true')

parser.add_argument('--dry', help='Do not modify plex collections (debugging feature)', action='store_true')

parser.add_argument('-y', help='Do not prompt.', action='store_true')

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

LIBRARY = args.library[0]
TYPE = args.type[0]
DRY_RUN = args.dry
SET_POSTERS = args.set_posters
NO_PROMPT = args.y