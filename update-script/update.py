import json
import os

with open('libraries.json', 'r') as f: libraries = json.load(f)

for lib in libraries: os.system(f'cd ..; python3 main.py --l {lib["name"]} --t {lib["type"]} -g -s -y')
