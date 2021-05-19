import pandas as pd
import numpy as np

# loading the merged population/shipments data
pop_ship = pd.read_csv('pop_ship.csv')
pop_ship = pop_ship[pop_ship['state'] != 'PR']
pop_ship = pop_ship[pd.notnull(pop_ship['county'])]
pop_ship['FIPS'] = pop_ship['FIPS'].fillna(value = '05099')
pop_ship['FIPS'] = pop_ship['FIPS'].astype(int)

# loading the cleaned vital statistics data by county, state, and year
# sorted to make checking easier
vitalstats = pd.read_csv('../10_code/vs_county_state_year.csv', index_col='Unnamed: 0')
vitalstats['State'] = vitalstats['State'].str.replace(' ', '')
vitalstats.sort_values(['County', 'State', 'Year'], inplace = True)
vitalstats['County'] = vitalstats['County'].str.lower()

# grouping original merged data by state and year
# original = original.groupby([original['BUYER_STATE'], original['year']], as_index = False).sum()

# renaming columns to match pop ship
vitalstats.rename(columns={'County':'county', 'State':'state', 'Year':'year'}, inplace = True)

# merge population/shipments data with vital stats data on fips and year
# sorted to make checking easier
pop_ship_death = pd.merge(pop_ship, vitalstats, how = 'outer', on = ['FIPS', 'year'])
# pop_ship_death.sort_values(['county', 'state', 'year'], inplace = True)
# pop_ship_death.reset_index(inplace = True, drop = True)

pop_ship_death.drop(['county_y', 'state_y'], axis = 1, inplace = True)
pop_ship_death.rename(columns={'county_x':'county', 'state_x':'state'}, inplace = True)

pop_ship_death['deaths_percap'] = pop_ship_death['Deaths']/pop_ship_death['population']

pop_ship_death['mme_percap'] = pop_ship_death['mme']/pop_ship_death['population']

pop_ship_death.rename(columns={'county':'County', 'state':'State', 'year':'Year'}, inplace = True)

pop_ship_death.to_csv('pop_ship_death.csv', index = False)


