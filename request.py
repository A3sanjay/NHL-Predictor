from multiprocessing.dummy import Value
from pickle import NONE
import requests
import json
import csv

# parameters = {    
#     'season': 20182019
# }

# Accessing data in api
URL = "https://statsapi.web.nhl.com/api/v1/standings/regularSeason?date=2019-06-01"
response = requests.get(URL)

if response.status_code != 200:
    print("Can't find the url you're looking for")

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


standings = response.json()

csvfile = open('data.csv', 'w')
writer = csv.writer(csvfile)

# Organizing the categories of data that we need. I'll loop through categories later
categories = {
    1 : 'leagueRank',
    2 : 'points',
    3 : 'pointsPercentage',     
}
index1 = 0
index2 = 0
initial_standings = {}
other_stats = []
while index1 < len(standings['records']):
    while index2 < len(standings['records'][index1]['teamRecords']):
        initial_standings.update({int(standings['records'][index1]['teamRecords'][index2][categories[1]]):str(standings['records'][index1]['teamRecords'][index2]['team']['name'])})
        other_stats.append(int(standings['records'][index1]['teamRecords'][index2][categories[2]]))
        other_stats.append(float(standings['records'][index1]['teamRecords'][index2][categories[3]]))

        index2 = index2 + 1
    
    index2 = 0
    index1 = index1 + 1

# Sorting based on season finish for simplicity
tmp = sorted(initial_standings.items())
sorted = {}
for key, value in tmp:
    sorted[key] = value

# Replacing the finish with a tuple of multiple statistics 
tmp_val = 1
for key, value in sorted.items():
    key = tmp_val
    tmp_val = tmp_val + 1   
    tmp = []
    tmp.append(key)
    tmp.append(other_stats[2 * key - 2])
    tmp.append(other_stats[2 * key - 1])
    tmp_tuple = tuple(tmp)
    sorted.update({tmp_tuple: value})
    sorted.pop(key)
    del tmp_tuple
    if tmp_val > len(sorted):
        break

print(sorted)

# Actually writing to csv
for key, value in sorted.items():
    writer = csv.writer(csvfile, delimiter=' ', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
    writer.writerow(f'{key} : {value}')
csvfile.close()
