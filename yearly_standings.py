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

    #     # Sorting based on season finish for simplicity
    #     tmp = sorted(initial_standings.items())
    #     sorted_1 = {}
    #     for key, value in tmp:
    #         sorted_1[key] = value

    #     # Replacing the finish with a tuple of multiple statistics 
    #     tmp_val = 0
    #     new_sorted = {}
    #     for key, value in sorted_1.items():        
    #         tmp_val = tmp_val + 1   
    #         key = tmp_val
    #         tmp = []
    #         tmp.append(key)
    #         tmp.append(other_stats[2 * key - 2])
    #         tmp.append(other_stats[2 * key - 1])
    #         tmp_tuple = tuple(tmp)
    #         new_sorted.update({tmp_tuple: value})
    #         del tmp_tuple
    #         if tmp_val > len(sorted_1):
    #             break

    #     # Actually writing to csv
    #     # Create a data set with all the teams and their place finishes in a given season and train model to recognize the #1 team in a season 
    #     for key, value in new_sorted.items():
    #         tmp = [key[0], key[1], key[2]]
    #         data.append(tmp)
    #         # writer = csv.writer(csvfile)
    #         # writer.writerow(f'{key} : {value}')
    #     csvfile.close()
    