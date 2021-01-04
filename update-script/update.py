import json
import os

with open('libraries.json', 'r') as f: libraries = json.load(f)

for lib in libraries: os.system(f'cd ..; python3 plexmngcollections.py --l {lib["name"]} --t {lib["type"]} -g -s -y')
