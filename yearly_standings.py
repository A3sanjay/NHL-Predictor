from multiprocessing.dummy import Value
import requests

# This is a function to run the standings every year for the compilation of data 
def standings(year):

    URL = f"https://statsapi.web.nhl.com/api/v1/standings/regularSeason?date={year}-06-01"
    response = requests.get(URL)

    if response.status_code != 200:
        print("Can't find the url you're looking for")

    standings = response.json()

    index1 = 0
    index2 = 0
    initial_standings = {}
    while index1 < len(standings['records']):
        while index2 < len(standings['records'][index1]['teamRecords']):
            initial_standings.update({str(standings['records'][index1]['teamRecords'][index2]['team']['name']):int(standings['records'][index1]['teamRecords'][index2]['leagueRank'])})

            index2 = index2 + 1
        
        index2 = 0
        index1 = index1 + 1
    return initial_standings
