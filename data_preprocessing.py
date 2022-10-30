import pandas as pd
import numpy as np

def preprocessing(df):

    categories = {
        1: 'Points',
        2: 'Wins',
        3: 'Points Percentage',
        4: 'Goals For',
        5: 'Goals Against',
    }

    errors = []
    for i in range(1, 31):
        values = df.loc[df['League Rank'] == i]
        # if i == 4 or i == 5:
        #     errors.append(values.index.tolist())
        mean = values.mean()
        standard_deviation = values.std()
        for key, value in categories.items():
            gte = values[values[value] > mean[value] + 0.5*standard_deviation[value]].index.tolist() 
            lte = values[values[value] < mean[value] - 0.5*standard_deviation[value]].index.tolist()
            
            if gte:
                errors.append(gte)
            if lte:
                errors.append(lte)
        
    flat_errors = [item for elem in errors for item in elem]
    errors = list(dict.fromkeys(flat_errors))

    for error in errors:
        df.drop(index = error, axis = 1, inplace = True)

    return df