import argparse
import sys
import os

from src.colors import bcolors

example_text = '\nexample command: ' + bcolors.BOLD +  'python3 main.py --library "Anime Shows" --type anime' + bcolors.ENDC
parser = argparse.ArgumentParser(description='Adds genre tags (collections) to your Plex media.', epilog = example_text)

parser.add_argument(
    '-l', '--library', action='store', dest='library', nargs=1, 
    help='The exact name of the Plex library to generate genre collections for.'
)

parser.add_argument(
    '-t', '--type', dest='type', action='store', choices=('anime', 'standard-movies', 'standard-shows', 'mixed-movies', 'mixed-shows'), 
    nargs=1, help='The type of media contained in the library. \nMixed libraries contain both standard media and anime (\'Non-Anime\' and \'Anime\' collections will be generated and anime\'s genre collections will be preceded by \'[A]\').'
)

parser.add_argument('-p', '--set-posters', help='Uploads posters located in posters/$media-type - media-type {anime, movies, shows}. Supports .PNG', action='store_true')

parser.add_argument('-g', '--generate-collections', help='Generate genre collections for the selected media.', action='store_true')

parser.add_argument('-s', '--sort', help='Only applies to mixed libraries. Updates the collections\' sorting titles so that \'Non-Anime\' and \'Anime\' will be the first collections and the anime genre\'s collections will be the last.', action='store_true')

parser.add_argument('-n', '--nono', '-d', '--dry', help='Do not modify plex collections (debugging feature).', action='store_true')

parser.add_argument('-y', '--yes', help='Do not prompt.', action='store_true')

parser.add_argument('-f', '--force', help='Force proccess on all media (independently of proggress recorded in logs/).', action='store_true')

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

args = parser.parse_args()

if not args.type or not args.library: 
    print(f'\n{bcolors.FAIL}The parameters {bcolors.BOLD}--library{bcolors.ENDC}{bcolors.FAIL} and {bcolors.BOLD}--type{bcolors.ENDC}{bcolors.FAIL} are required.\n{bcolors.ENDC}')
    sys.exit(1)

LIBRARY = args.library[0]
TYPE = args.type[0]
DRY_RUN = args.nono
NO_PROMPT = args.yes
FORCE = args.force
GENERATE = args.generate_collections
SORT = args.sort
SET_POSTERS = args.set_posters

if not GENERATE and not SORT and not SET_POSTERS:
    print(f'\n{bcolors.FAIL}At least one action parameter ({bcolors.BOLD}-g{bcolors.ENDC}{bcolors.FAIL}, {bcolors.BOLD}-p{bcolors.ENDC}{bcolors.FAIL} or {bcolors.BOLD}-s{bcolors.ENDC}{bcolors.FAIL}) is required.\n{bcolors.ENDC}')
    sys.exit(1)

if FORCE:
    if os.path.isfile(f'logs/plex-{TYPE}-successful.txt'): os.remove(f'logs/plex-{TYPE}-successful.txt')
    if os.path.isfile(f'logs/plex-{TYPE}-failures.txt'): os.remove(f'logs/plex-{TYPE}-failures.txt')

if 'mixed-' not in TYPE: SORT = False