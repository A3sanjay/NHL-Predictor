# API data is not sufficient for the ML model, so data augmentation will be needed 
# This will be done by scanning the existing data and then finding entries with the same League Rank and creating a new entry by averaging all the other values

import numpy as np

def augmentation (cumulative_stats):
    index1 = 0
    index2 = 0
    length = len(cumulative_stats)
    while index1 < length: 
        stats1 = cumulative_stats[index1]
        while index2 < length:
            stats2 = cumulative_stats[index2]
            if index1 != index2:
                if stats1[-1] == stats2[-1]:
                    data = np.array([stats1, stats2])
                    tmp = np.average(data, axis=0).tolist()

                    new_stats = []
                    i = 0
                    while i < len(tmp):
                        if i == 2:
                            rounded = round(tmp[i], 2)
                        else:
                            rounded = round(tmp[i])
                        new_stats.append(rounded)
                        i = i + 1
                    
                    cumulative_stats.append(new_stats)

            index2 = index2 + 1
        
        index2 = index1
        index1 = index1 + 1

    
    return(cumulative_stats)
