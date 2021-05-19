import pandas as pd
from plotnine import *

df = pd.read_csv('full_merge.csv')
df['death_rate'] = df['Deaths']/df['population']
df['mme_rate'] = df['mme']/df['population']
wa = df[df['State'] == 'WA']
wa_range =[2008,2009,2010,2011]
wa_0811 =wa[wa['Year'].isin(wa_range)]
wa_0811
wa_min = wa_0811['Deaths'].min()
wa_max = wa_0811['Deaths'].max()
all_0811 =df[df['Year'].isin(wa_range)]
all_wa = all_0811[(all_0811['Deaths'] > wa_min * 0.7) & (all_0811['Deaths'] < wa_max * 1.3)]

all_wa
#NC and MA seems have similar death trends with TX within 2003 - 2006 


compared_state = ['CO','NC','AZ','GA','NV','MA','WA']
wa_compare =all_0811[all_0811['State'].isin(compared_state)]

p = (ggplot(wa_compare, aes(x ='Year', y='Deaths',color = 'State')) +
        geom_line(alpha=1)
        #geom_smooth(method='lm',color= 'r')
   )

p.save('comparision_for_wa')
#The seletion of comparision can tell from the plots