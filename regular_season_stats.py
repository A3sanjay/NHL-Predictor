# This is a compilation of data that affects a team's regular season performance and writes it to the csv to train with

import requests
import csv
import random
import yearly_standings
import data_augmentation

cumulative_stats = []
year = 2020
# Takes the data for each team for the previous 3 years, but uses the CURRENT year's standings result
while year > 2002:
    tmp_year = year - 1
    # Taking the standings for the current year as we can't keep calling the present year for the standings after going back
    y_standings = yearly_standings.standings(year)

    while tmp_year > year - 3:
        # Accessing data in api
        URL = f"https://statsapi.web.nhl.com/api/v1/standings/regularSeason?date={tmp_year}-06-01"
        response = requests.get(URL)

        if response.status_code != 200:
            print("Can't find the url you're looking for")

        standings = response.json()

        # Organizing the categories of data inputs that we need
        categories = {
            1 : 'points',
            2 : 'wins',
            3 : 'pointsPercentage',  
            4 : 'goalsScored',  
            5 : 'goalsAgainst',
        }
        
        # Going through API to retrieve the correct columns of data
        index1 = 0
        index2 = 0
        while index1 < len(standings['records']):
            while index2 < len(standings['records'][index1]['teamRecords']):
                smaller_list = []
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[1]])
                smaller_list.append(standings['records'][index1]['teamRecords'][index2]['leagueRecord'][categories[2]])
                smaller_list.append(round(float(standings['records'][index1]['teamRecords'][index2][categories[3]]), 2))
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[4]])
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[5]])
                team_name = str(standings['records'][index1]['teamRecords'][index2]['team']['name'])
                # Utilizing the standings function to append standings data 
                if (team_name in y_standings):
                    smaller_list.append(y_standings[team_name])
                # Removing any lists with null values before pushing to list of lists
                if len(smaller_list) == 6:
                    cumulative_stats.append(smaller_list)
                index2 = index2 + 1
            
            index2 = 0
            index1 = index1 + 1

        tmp_year = tmp_year - 1    
    year = year - 1 

# Augmenting data and writing to csv
augmented_stats = data_augmentation.augmentation(cumulative_stats)
random.shuffle(augmented_stats)
csvfile = open('regular_season_data.csv', 'w')
writer = csv.writer(csvfile)
writer.writerow(['Points', 'Wins', 'Points Percentage', 'Goals For', 'Goals Against', 'League Rank'])
for team_stats in augmented_stats:
    writer.writerow(team_stats)
csvfile.close()