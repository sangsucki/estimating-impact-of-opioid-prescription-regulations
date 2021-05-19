import os
import pandas as pd
import numpy as np

# arcos shipments
shipments = pd.read_csv("../10_code/Concatenate/output.csv")
shipments.rename(columns={'BUYER_COUNTY':'county', 'BUYER_STATE':'state'}, inplace = True)
shipments['county'] = shipments['county'].str.lower()
shipments.head()

# populations
pop = pd.read_csv("../00_source/population/population_03-15.csv")
pop['county'] = pop['county'].str.lower()
pop.head()

pop_ship = pd.merge(shipments, pop, on=['county','state','year'], how='outer')
pop_ship.head(5)

pop_ship = pop_ship[['county', 'state', 'mme', 'year', 'countyfips', 'population']]
pop_ship.rename(columns={'countyfips':'FIPS'}, inplace = True)
    
pop_ship.sort_values(['county','state','year'], inplace = True)

pop_ship.to_csv("pop_ship.csv",index = False)
