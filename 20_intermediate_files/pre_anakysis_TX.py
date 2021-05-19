import pandas as pd
from plotnine import *

df = pd.read_csv('full_merge.csv')
df['death_rate'] = df['Deaths']/df['population']
df['mme_rate'] = df['mme']/df['population']
tx = df[df['State'] == 'TX']
tx_range =[2003,2004,2005,2006]
tx_0306 =tx[tx['Year'].isin(tx_range)]
tx_0306
tx_min = tx_0306['Deaths'].min()
tx_max = tx_0306['Deaths'].max()
all_0306 =df[df['Year'].isin(tx_range)]
all_tx = all_0306[(all_0306['Deaths'] > tx_min * 0.5) & (all_0306['Deaths'] < tx_max * 1.5)]

all_tx
#CA and IL seems have similar death trends with TX within 2003 - 2006 


compared_state = ['PA','TX','OH','CA','MI','TN','NY','IL','NJ']
tx_compare =all_0306[all_0306['State'].isin(compared_state)]

(ggplot(tx_compare, aes(x ='Year', y='Deaths',color = 'State')) +
        geom_line(alpha=1)
        #geom_smooth(method='lm',color= 'r')
)

#The seletion of comparision can tell from the plots
p.save('comparision_for_tx')
