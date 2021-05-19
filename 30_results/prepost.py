import pandas as pd
import numpy as np
from plotnine import *

df = pd.read_csv('../20_intermediate_files/pop_ship_death.csv')
df.head()

# florida
fl_death_comp = ['FL', 'NV', 'PA', 'IN']
fl_mme_comp = ['FL', 'GA', 'CA', 'NM']

fl_death = df[df['State'].isin(fl_death_comp)]
fl_death['policy'] = np.where(fl_death['State'] == 'FL', 'Policy', 'Non-policy')
fl_death_grouped = fl_death.groupby(['policy','Year']).mean()
fl_death_grouped = fl_death_grouped.reset_index()

fl_mme = df[df['State'].isin(fl_mme_comp)]
fl_mme['policy'] = np.where(fl_mme['State'] == 'FL', 'Policy', 'Non-policy')
fl_mme_grouped = fl_mme.groupby(['policy','Year']).mean()
fl_mme_grouped = fl_mme_grouped.reset_index()

fl = df[df['State'] == 'FL']

# texas
tx_death_comp = ['TX', 'PA', 'OH', 'IL', 'CA']
tx_death = df[df['State'].isin(tx_death_comp)]
tx_death['policy'] = np.where(tx_death['State'] == 'TX', 'Policy', 'Non-policy')
tx_death_grouped = tx_death.groupby(['policy','Year']).mean()
tx_death_grouped = tx_death_grouped.reset_index()
tx = df[df['State'] == 'TX']

# washington
wa_death_comp = ['WA', 'NC', 'MA', 'CO']
wa_death = df[df['State'].isin(wa_death_comp)]
wa_death['policy'] = np.where(wa_death['State'] == 'WA', 'Policy', 'Non-policy')
wa_death_grouped = wa_death.groupby(['policy','Year']).mean()
wa_death_grouped = wa_death_grouped.reset_index()
wa = df[df['State'] == 'WA']

###

# ANALYSIS PLOTS

death_yrs = (2003,2015)
death_scale = np.arange(2003, 2016, 1)

ship_yrs = (2006, 2012)
ship_scale = np.arange(2006, 2013, 1)

# FLORIDA 

fl_policy = 2010

# FLORIDA DEATHS

# diff in diff (death)
(ggplot(fl_death_grouped, aes(x ='Year', y='deaths_percap',color = 'policy')) 
 + geom_line(alpha=1) 
 + geom_vline(xintercept = fl_policy) 
 + labs(title = 'Florida: Diff-in-Diff Plot of Overdose Deaths') 
 + ylab('Overdose Deaths per Capita') 
 + scale_x_continuous(breaks = death_scale, limits= death_yrs) 
 + geom_smooth(data = fl[fl['Year'] <= fl_policy], color='turquoise', method='lm') 
 + geom_smooth(data = fl[fl['Year'] >= fl_policy], color='turquoise', method='lm')
 + geom_smooth(data = fl_death_grouped[(fl_death_grouped['Year'] <= fl_policy) &
                                        (fl_death_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm')
 + geom_smooth(data = fl_death_grouped[(fl_death_grouped['Year'] >= fl_policy) &
                                        (fl_death_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm'))

# prepost (death)
(ggplot(fl, aes(x ='Year', y='deaths_percap', color = 'State')) 
 + geom_line(alpha=1, show_legend=False) 
 + labs(title = 'Florida: Pre-Post Plot of Overdose Deaths') 
 + ylab('Overdose Deaths per Capita') 
 + scale_x_continuous(breaks = death_scale, limits = death_yrs) 
 + geom_vline(xintercept = fl_policy) 
 + geom_smooth(data = fl[fl['Year'] <= fl_policy], color='red', method = 'lm')
 + geom_smooth(data = fl[fl['Year'] >= fl_policy], color='red', method = 'lm'))

# FLORIDA SHIPMENTS

# prepost (shipment)
(ggplot(fl, aes(x ='Year', y='mme_percap', color = 'State')) 
 + geom_line(alpha=1, show_legend = False) 
 + geom_vline(xintercept = fl_policy) 
 + labs(title = 'Florida: Pre-Post Plot of Opioid Shipments') 
 + ylab('Morphine Equivalents per Capita') 
 + scale_x_continuous(breaks = ship_scale, limits = ship_yrs) 
 + geom_smooth(data = fl[fl['Year'] <= fl_policy], color='red', method='lm') 
 + geom_smooth(data = fl[fl['Year'] >= fl_policy], color='red', method='lm'))

# diff in diff (shipment)
(ggplot(fl_mme_grouped, aes(x ='Year', y='mme_percap',color = 'policy')) 
 + geom_line(alpha=1) 
 + geom_vline(xintercept = fl_policy) 
 + labs(title = 'Florida: Diff-in-Diff Plot of Opioid Shipments') 
 + ylab('Morphine Equivalents per Capita') 
 + scale_x_continuous(breaks = ship_scale, limits = ship_yrs)
 + geom_smooth(data = fl[fl['Year'] <= fl_policy], color='turquoise', method='lm') 
 + geom_smooth(data = fl[fl['Year'] >= fl_policy], color='turquoise', method='lm')
 + geom_smooth(data = fl_mme_grouped[(fl_mme_grouped['Year'] <= fl_policy) &
                                        (fl_mme_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm')
 + geom_smooth(data = fl_mme_grouped[(fl_mme_grouped['Year'] >= fl_policy) &
                                        (fl_mme_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm'))


# TEXAS

tx_policy = 2007

# diff in diff
(ggplot(tx_death_grouped, aes(x ='Year', y='deaths_percap', color = 'policy')) 
 + geom_line(alpha=1) 
 + scale_x_continuous(breaks = death_scale, limits = death_yrs) 
 + geom_vline(xintercept = tx_policy)
 + labs(title = 'Texas: Diff-in-Diff Plot of Overdose Deaths') 
 + ylab('Overdose Deaths per Capita')
 + geom_smooth(data = tx[tx['Year'] <= tx_policy], color='turquoise', method='lm') 
 + geom_smooth(data = tx[tx['Year'] >= tx_policy], color='turquoise', method='lm')
 + geom_smooth(data = tx_death_grouped[(tx_death_grouped['Year'] <= tx_policy) &
                                        (tx_death_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm')
 + geom_smooth(data = tx_death_grouped[(tx_death_grouped['Year'] >= tx_policy) &
                                        (tx_death_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm'))

# prepost
(ggplot(tx, aes(x ='Year', y='deaths_percap',color = 'State')) 
 + geom_line(alpha=1) 
 + scale_x_continuous(breaks = death_scale, limits = death_yrs) 
 + geom_vline(xintercept = tx_policy) 
 + labs(title = 'Texas: Pre-Post Plot of Overdose Deaths') 
 + ylab('Overdose Deaths per Capita') 
 + geom_smooth(data = tx[tx['Year'] <= tx_policy], color='red', method='lm') 
 + geom_smooth(data = tx[tx['Year'] >= tx_policy], color='red', method='lm'))

# WASHINGTON

wa_policy = 2012

# diff in diff
(ggplot(wa_death_grouped, aes(x ='Year', y='deaths_percap',color = 'policy')) 
 + geom_line(alpha=1) 
 + scale_x_continuous(breaks = death_scale, limits = death_yrs) 
 + geom_vline(xintercept = wa_policy) 
 + labs(title = 'Washington: Diff-in-Diff Plot of Overdose Deaths') 
 + ylab('Overdose Deaths per Capita')
 + geom_smooth(data = wa[wa['Year'] <= wa_policy], color='turquoise', method='lm') 
 + geom_smooth(data = wa[wa['Year'] >= wa_policy], color='turquoise', method='lm')
 + geom_smooth(data = wa_death_grouped[(wa_death_grouped['Year'] <= wa_policy) &
                                        (wa_death_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm')
 + geom_smooth(data = wa_death_grouped[(wa_death_grouped['Year'] >= wa_policy) &
                                        (wa_death_grouped['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm'))

# prepost
(ggplot(wa, aes(x ='Year', y='deaths_percap',color = 'State')) 
 + geom_line(alpha=1) 
 + scale_x_continuous(breaks = death_scale, limits = death_yrs) 
 + geom_vline(xintercept = wa_policy) 
 + labs(title = 'Washington: Pre-Post Plot of Overdose Deaths') 
 + ylab('Overdose Deaths per Capita') 
 + geom_smooth(data = wa[wa['Year'] <= wa_policy], color='red', method='lm') 
 + geom_smooth(data = wa[wa['Year'] >= wa_policy], color='red', method='lm'))