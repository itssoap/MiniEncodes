from jikanpy import Jikan
import sys
from pprint import pprint
import json
from glob import glob
import requests
import os

api_key = str(input("Enter TMDB api key: "))
season = input("Enter Season Number (Specials are usually Season 0): ")
tmdb_id = input("Enter TMDB Show ID: ")


r = requests.get(url = f"https://api.themoviedb.org/3/tv/{tmdb_id}/season/{season}?api_key={api_key}")
parsed = json.loads(json.dumps(r.json(), indent=4))
print(parsed['episodes'][0]['name'])
	#print(i['title'])

files = glob('*.mkv')
i = 0
for file in files:
        name = parsed['episodes'][i]['name']
        print(f'{file[:-4]}{name}.mkv')
        name = "".join(j for j in name if j not in "\/:*?<>|")
        os.rename(file, f'{file[:-4]}{name}.mkv')
        i = i+1
