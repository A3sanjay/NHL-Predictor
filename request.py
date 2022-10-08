from pickle import NONE
import requests
import json
import csv

parameters = {
    # "season": 20182019,
    
    'season': 20182019
}

URL = "https://statsapi.web.nhl.com/api/v1/standings/regularSeason?date=1917github-06-01"
response = requests.get(URL, params=parameters)

if response.status_code != 200:
    print("Can't find the url you're looking for")

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


standings = response.json()
# jprint(response.json())

csvfile = open('data.csv', 'w')
writer = csv.writer(csvfile)

index1 = 0
index2 = 0
initial = {}
while index1 < len(standings['records']):
    while index2 < len(standings['records'][index1]['teamRecords']):
        initial.update({int(standings['records'][index1]['teamRecords'][index2]['leagueRank']):str(standings['records'][index1]['teamRecords'][index2]['team']['name'])})

        index2 = index2 + 1
    
    index2 = 0
    index1 = index1 + 1
tmp = sorted(initial.items())
sorted = {}
for key, value in tmp:
    sorted[key] = value

for key, value in sorted.items():
    writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(f'{key} : {value}')
# writer.writerow(response.json())
csvfile.close()
