# This is a compilation of data that affects a team's regular season performance and writes it to the csv to use

import pandas as pd
from multiprocessing.dummy import Value
from pickle import NONE
import requests
import csv
import yearly_standings
cumulative_stats = []
year = 2020
while year > 2002:
    tmp_year = year - 1
    y_standings = yearly_standings.standings(year)

    while tmp_year > year - 4:
        # Accessing data in api
        URL = f"https://statsapi.web.nhl.com/api/v1/standings/regularSeason?date={tmp_year}-06-01"
        response = requests.get(URL)

        if response.status_code != 200:
            print("Can't find the url you're looking for")

        standings = response.json()

        # Organizing the categories of data inputs that we need
        categories = {
            1 : 'points',
            2 : 'pointsPercentage',  
            3 : 'goalsAgainst',  
            4 : 'goalsScored',
        }
        
        index1 = 0
        index2 = 0
        i = 1
        while index1 < len(standings['records']):
            while index2 < len(standings['records'][index1]['teamRecords']):
                smaller_list = []
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[1]])
                smaller_list.append(standings['records'][index1]['teamRecords'][index2]['leagueRecord']['wins'])
                smaller_list.append(round(float(standings['records'][index1]['teamRecords'][index2][categories[2]]), 2))
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[3]])
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[4]])
                team_name = str(standings['records'][index1]['teamRecords'][index2]['team']['name'])
                if (team_name in y_standings):
                    smaller_list.append(y_standings[team_name])
                if len(smaller_list) == 6:
                    cumulative_stats.append(smaller_list)
                index2 = index2 + 1
            
            index2 = 0
            index1 = index1 + 1

        tmp_year = tmp_year - 1    
    year = year - 1 

print(cumulative_stats)
csvfile = open('data.csv', 'w')
writer = csv.writer(csvfile)
writer.writerow(['Points', 'Wins', 'Points Percentage', 'Goals Against', 'Goals For', 'League Rank'])
for team_stats in cumulative_stats:
    writer.writerow(team_stats)
csvfile.close()