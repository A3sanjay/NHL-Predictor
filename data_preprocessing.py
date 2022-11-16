import pandas as pd
import numpy as np

def preprocessing(df):
    categories = []
    for column_header in df.columns:
        if column_header != 'League Rank' or column_header != 'Post Season Finish':
            categories.append(column_header)

    errors = []
    for i in range(1, 31):
        if 'League Rank' in df.columns:
            column = 'League Rank'
        else:
            column = 'Post Season Finish'
        values = df.loc[df[column] == i]
        # if i == 4 or i == 5:
        #     errors.append(values.index.tolist())
        mean = values.mean()
        standard_deviation = values.std()
        for category in categories:
            gte = values[values[category] > mean[category] + 0.5*standard_deviation[category]].index.tolist() 
            lte = values[values[category] < mean[category] - 0.5*standard_deviation[category]].index.tolist()
            
            if gte:
                errors.append(gte)
            if lte:
                errors.append(lte)
        
    flat_errors = [item for elem in errors for item in elem]
    errors = list(dict.fromkeys(flat_errors))

    for error in errors:
        df.drop(index = error, axis = 1, inplace = True)

    return df