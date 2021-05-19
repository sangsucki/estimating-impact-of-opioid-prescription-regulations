import pandas as pd
import os

# Folder where all vital statistics txt files are held
directory = '/Users/vanessatang/estimating-impact-of-opioid-prescription-regulations-team-7/00_source/US_VitalStatistics/'

# Loop through directory to get list of filenames 
all_vs_fn = []

for filename in os.listdir(directory):
    if filename.endswith(".txt"): 
         all_vs_fn.append(filename)

# Loop through list of filenames and add directory to get filepath for each txt file
all_vs_fp = []

for file in all_vs_fn:
    fp = directory + file
    all_vs_fp.append(fp)
        
# Loop through list of filepaths
# Append each dataframe with columns of interest (cols)

all_vital_statistics = pd.DataFrame()

cols = ['County', 'County Code', 'Year', 'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code', 'Deaths']

for fp in all_vs_fp:
    df = pd.read_csv(fp, sep = '\t', usecols = cols)
    all_vital_statistics = all_vital_statistics.append(df, ignore_index = True)

all_vital_statistics.head()

# Rename County Code colunn to FIPS to be able to merge in the future
all_vital_statistics = all_vital_statistics.rename(columns={"County Code": "FIPS"})

all_vital_statistics.sample(10)
all_vital_statistics.shape

# saving uncollapsed data to new csv
# all_vital_statistics.to_csv('all_vital_statistics.csv')

vs = pd.read_csv('all_vital_statistics.csv', index_col=0)
vs.head()

# grouping uncollapsed data by FIPS, year, death cause, and summing all deaths
vs_collapsed = vs.groupby(['FIPS', 'Year', 'Drug/Alcohol Induced Cause', 'Drug/Alcohol Induced Cause Code'], as_index = False).sum()

# 'Drug poisonings (overdose) Unintentional (X40-X44)': D1
# 'Drug poisonings (overdose) Suicide (X60-X64)': D2
# 'Drug poisonings (overdose) Homicide (X85)': D3
# 'Drug poisonings (overdose) Undetermined (Y10-Y14)': D4

state = vs_collapsed['County'].str.split(',', expand=True)
vs_collapsed['State'] = state[1]
vs_collapsed['County'] = state[0]

drug_codes = ['D1', 'D2', 'D3', 'D4']
vs_collapsed = vs_collapsed[vs_collapsed['Drug/Alcohol Induced Cause Code'].isin(drug_codes)]
vs_collapsed = vs_collapsed.drop(['Drug/Alcohol Induced Cause'], axis=1)
vs_collapsed['Deaths'] = vs_collapsed['Deaths'].replace('Missing', 0)
vs_collapsed['Deaths'] = vs_collapsed['Deaths'].astype(float)
vs_collapsed['Year'] = vs_collapsed['Year'].astype(int)

vs_collapsed.head()
print(vs_collapsed.dtypes)

# vs_state_year = vs_collapsed.groupby(['State', 'Year']).sum()
# vs_state_year.reset_index(inplace=True)
# vs_state_year.head()

vs_county_state_year = vs_collapsed.groupby(['County', 'State', 'Year', 'FIPS']).sum()
vs_county_state_year.reset_index(inplace=True)
vs_county_state_year['FIPS'] = vs_county_state_year['FIPS'].astype(int)

vs_county_state_year.sort_values(['County', 'State', 'Year'], inplace = True)

vs_county_state_year.head()

vs_county_state_year.to_csv('vs_county_state_year.csv')
