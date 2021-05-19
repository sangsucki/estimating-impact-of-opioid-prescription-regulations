import pandas as pd
from plotnine import *

df = pd.read_csv('full_merge.csv')
df['death_rate'] = df['Deaths']/df['population']
df['mme_rate'] = df['mme']/df['population']
flo = df[df['State'] == 'FL']
flo_range =[2010,2011,2012]
flo_1012 =flo[flo['Year'].isin(flo_range)]
flo_1012

all_1012 =df[df['Year'].isin(flo_range)]


#PA and MI seems have similar death trends with FL within 2006 - 2009 


all_flo_mme

compared_state = ['PA','FL','CA','MI','TN']
flo_compare =all_1012[all_1012['State'].isin(compared_state)]
#PA and TN seems have similar MME trengs with FL within 2006-2009

p1 = (ggplot(flo_compare, aes(x ='Year', y='death_rate',color = 'State')) +
        geom_line(alpha=1)
        #geom_smooth(method='lm',color= 'r')
)
p1
p2 = (ggplot(flo_compare, aes(x ='Year', y='mme_rate',color = 'State')) +
        geom_line(alpha=1)
        #geom_smooth(method='lm',color= 'r')
)
p2

p1.save('post_comparision_for_flo_death_rate')
p2.save('post_comparision_for_flo_mme_rate')
