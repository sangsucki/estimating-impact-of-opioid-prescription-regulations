import pandas as pd
from plotnine import *

df = pd.read_csv('full_merge.csv')
df['death_rate'] = df['Deaths']/df['population']
df['mme_rate'] = df['mme']/df['population']
flo = df[df['State'] == 'FL']
flo_range =[2006,2007,2008,2009]
flo_0710 =flo[flo['Year'].isin(flo_range)]
flo_0710
flo_min = flo_0710['Deaths'].min()
flo_max = flo_0710['Deaths'].max()
all_0710 =df[df['Year'].isin(flo_range)]
all_flo = all_0710[(all_0710['Deaths'] > flo_min * 0.3) & (all_0710['Deaths'] < flo_max * 1.7)]

#'GA','IN', 'KS', 'MT','NV', 'PA' seems have similar death trends with FL within 2006 - 2009 

flo_min_mme = flo_0710['mme'].min()
flo_max_mme = flo_0710['mme'].max()
all_flo_mme = all_0710[(all_0710['mme'] > flo_min_mme * 0.3) & (all_0710['mme'] < flo_max_mme * 2)]

all_flo_mme
compared_state = ['FL','GA','IN', 'KS', 'MT','NV', 'PA']
flo_compare =all_0710[all_0710['State'].isin(compared_state)]

#'PA','OH','TN', 'KY','AL', 'AZ', 'CA', 'CO',"GA", 'NM', 'SC', 'TN' seems have similar MME trengs with FL within 2006-2009

p1 = (ggplot(flo_compare, aes(x ='Year', y='death_rate',color = 'State')) +
        geom_line(alpha=1)
        #geom_smooth(method='lm',color= 'r')
)

compared_state = ['FL','GA','IN', 'KS', 'MT','NV', 'PA']
flo_compare =all_0710[all_0710['State'].isin(compared_state)]

p2 = (ggplot(flo_compare, aes(x ='Year', y='mme_rate',color = 'State')) +
        geom_line(alpha=1)
        #geom_smooth(method='lm',color= 'r')
)

p1.save('comparision_for_flo_death_rate_1')
p2.save('comparision_for_flo_mme_rate_1')
