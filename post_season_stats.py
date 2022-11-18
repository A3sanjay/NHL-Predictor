# This is a compilation of data that affects a team's regular season performance and writes it to the csv to train with

import requests
import csv
import random
import yearly_standings
import data_augmentation

# Data had to be manually retrieved as API wasn't working for postseason stats
data = {2019: {1: 'St. Louis Blues', 2: 'Boston Bruins', 3: ['Carolina Hurricanes', 'San Jose Sharks'], 4: ['Colorado Avalanche', 'Columbus Blue Jackets', 'Dallas Stars', 'New York Islanders'], 5: ['Calgary Flames', 'Nashville Predators', 'Pittsburgh Penguins', 'Tampa Bay Lightning', 'Toronto Maple Leafs', 'Vegas Golden Knights', 'Winnipeg Jets', 'Washington Capitals']}, 2018: {1: 'Washington Capitals', 2: 'Vegas Golden Knights', 3: ['Tampa Bay Lightning', 'Winnipeg Jets'], 4: ['Boston Bruins', 'Nashville Predators', 'Pittsburgh Penguins', 'Vegas Golden Knights'], 5: ['Anaheim Ducks', 'Colorado Avalanche', 'Columbus Blue Jackets', 'Los Angeles Kings', 'Minnesota Wild', 'New Jersey Devils', 'Philadelphia Flyers', 'Toronto Maple Leafs']}, 2017: {1: 'Pittsburgh Penguins', 2: 'Nashville Predators', 3: ['Anaheim Ducks', 'Ottawa Senators'], 4: ['Edmonton Oilers', 'New York Rangers', 'St. Louis Blues', 'Washington Capitals'], 5: ['Boston Bruins', 'Calgary Flames', 'Chicago Blackhawks', 'Columbus Blue Jackets', 'Minnesota Wild', 'Montréal Canadiens', 'San Jose Sharks' 'Toronto Maple Leafs']},2016: {1: 'Pittsburgh Penguins', 2: 'San Jose Sharks', 3: ['St. Louis Blues', 'Tampa Bay Lightning'], 4: ['Dallas Stars', 'Nashville Predators', 'New York Islanders', 'Washington Capitals'], 5: ['Anaheim Ducks', 'Chicago Blackhawks', 'Detroit Red Wings', 'Florida Panthers', 'Los Angeles Kings', 'Minnesota Wild', 'New York Rangers' 'Philadelphia Flyers']}, 2015: {1: 'Chicago Blackhawks', 2: 'Tampa Bay Lightning', 3: ['Anaheim Ducks', 'New York Rangers'], 4: ['Calgary Flames', 'Minnesota Wild', 'Montréal Canadiens', 'Washington Capitals'], 5: ['Detroit Red Wings', 'Nashville Predators', 'New York Islanders', 'Ottawa Senators', 'Pittsburgh Penguins', 'St. Louis Blues', 'Vancouver Canucks', 'Winnipeg Jets']}, 2014: {1: 'Los Angeles Kings', 2: 'New York Rangers', 3: ['Chicago Blackhawks', 'Montréal Canadiens'], 4: ['Anaheim Ducks', 'Boston Bruins', 'Minnesota Wild', 'Pittsburgh Penguins'], 5: ['Colorado Avalanche', 'Columbus Blue Jackets', 'Dallas Stars', 'Detroit Red Wings', 'Philadelphia Flyers', 'San Jose Sharks', 'St. Louis Blues', 'Tampa Bay Lightning']}, 2013: {1: 'Chicago Blackhawks', 2: 'Boston Bruins', 3: ['Los Angeles Kings', 'Pittsburgh Penguins'], 4: ['Detroit Red Wings', 'Ottawa Senators', 'New York Rangers', 'San Jose Sharks'], 5: ['Anaheim Ducks', 'Minnesota Wild', 'Montréal Canadiens', 'New York Islanders', 'St. Louis Blues', 'Toronto Maple Leafs', 'Vancouver Canucks', 'Washington Capitals']}, 2012: {1: 'Los Angeles Kings', 2: 'New Jersey Devils', 3: ['New York Rangers', 'Phoenix Coyotes'], 4: ['Nashville Predators', 'Philadelphia Flyers', 'St. Louis Blues', 'Washington Capitals'], 5: ['Boston Bruins', 'Chicago Blackhawks', 'Detroit Red Wings', 'Florida Panthers', 'Ottawa Senators', 'Philadelphia Flyers', 'San Jose Sharks', 'Vancouver Canucks']}, 2011: {1: 'Boston Bruins', 2: 'Vancouver Canucks', 3: ['San Jose Sharks', 'Tampa Bay Lightning'], 4: ['Detroit Red Wings', 'Nashville Predators', 'Philadelphia Flyers', 'Washington Capitals'], 5: ['Anaheim Ducks', 'Buffalo Sabres', 'Chicago Blackhawks', 'Montréal Canadiens', 'New York Rangers', 'Phoenix Coyotes', 'Pittsburgh Penguins']}, 2010: {1: 'Chicago Blackhawks', 2: 'Philadelphia Flyers', 3: ['Montréal Canadiens', 'San Jose Sharks'], 4: ['Boston Bruins', 'Pittsburgh Penguins', 'Detroit Red Wings', 'Vancouver Canucks'], 5: ['Buffalo Sabres', 'Colorado Avalanche', 'Los Angeles Kings', 'Nashville Predators', 'New Jersey Devils', 'Ottawa Senators', 'Phoenix Coyotes', 'Washington Capitals']}}

import requests
import csv
import random
import yearly_standings
import data_augmentation

cumulative_stats = []
year = 2019
while year > 2009:
    tmp_year = year
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
            3 : 'leagueL10Rank'
        }
        # Going through API to retrieve the correct columns of data
        index1 = 0
        index2 = 0
        while index1 < len(standings['records']):
            while index2 < len(standings['records'][index1]['teamRecords']):
                smaller_list = []
                smaller_list.append(standings['records'][index1]['teamRecords'][index2][categories[1]])
                smaller_list.append(standings['records'][index1]['teamRecords'][index2]['leagueRecord'][categories[2]])
                smaller_list.append(int(standings['records'][index1]['teamRecords'][index2][categories[3]]))
                team_name = str(standings['records'][index1]['teamRecords'][index2]['team']['name'])
                for finish, teams in data[year].items():
                    if (team_name in teams):
                        smaller_list.append(finish)
                # Removing any lists with null values before pushing to list of lists
                if len(smaller_list) == 4:
                    cumulative_stats.append(smaller_list)
                index2 = index2 + 1
            
            index2 = 0
            index1 = index1 + 1

        tmp_year = tmp_year - 1    
    year = year - 1 

# Augmenting data and writing to csv
augmented_stats = data_augmentation.augmentation(cumulative_stats)
random.shuffle(augmented_stats)
csvfile = open('post_season_data.csv', 'w')
writer = csv.writer(csvfile)
writer.writerow(['Points', 'Wins', 'Last 10 Rank', 'Post Season Finish'])
for team_stats in augmented_stats:
    writer.writerow(team_stats)
csvfile.close()