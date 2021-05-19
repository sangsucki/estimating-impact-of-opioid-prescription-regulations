import pandas as pd
import numpy as np
from plotnine import *

df = pd.read_csv('../20_intermediate_files/pop_ship_death.csv')
df.head()

# function to get grouped datasets

def grouped_data(df, state, comp_list):
    sub = df[df['State'].isin(comp_list)]
    sub['policy'] = np.where(sub['State'] == state, 'Policy', 'Non-policy')
    grouped_df = sub
    return grouped_df

# florida
fl_policy = 2010

fl_death_comp = ['FL', 'NV', 'PA', 'IN']
fl_mme_comp = ['FL', 'GA', 'CA', 'NM']

fl_death_grouped = grouped_data(df, 'FL', fl_death_comp)
fl_mme_grouped = grouped_data(df, 'FL', fl_mme_comp)

fl = df[df['State'] == 'FL']

# texas
tx_policy = 2007
tx_death_comp = ['TX', 'PA', 'OH', 'IL', 'CA']
tx_death_grouped = grouped_data(df, 'TX', tx_death_comp)
tx = df[df['State'] == 'TX']

# washington
wa_policy = 2012
wa_death_comp = ['WA', 'NC', 'MA', 'CO']
wa_death_grouped = grouped_data(df, 'WA', wa_death_comp)
wa = df[df['State'] == 'WA']

# scales
death_yrs = (2003,2015)
death_scale = np.arange(2003, 2016, 1)

ship_yrs = (2006, 2012)
ship_scale = np.arange(2006, 2013, 1)

# functions for plots

def did_plot_deaths(df, state, policy_year, state_title):
    print (ggplot(df, aes(x ='Year', y='deaths_percap',color = 'policy')) 
         + geom_point(alpha=.2) 
         + geom_vline(xintercept = policy_year) 
         + labs(title = '{0}: Diff-in-Diff Plot of Overdose Deaths'.format(state_title))
         + ylab('Overdose Deaths per Capita')
         + scale_x_continuous(breaks = death_scale, limits= death_yrs) 
         #+ scale_y_continuous(breaks = death_scale, limits= death_yrs) 
         + geom_smooth(data = df[(df['Year'] <= policy_year) &
                                 (df['policy'] == 'Policy')], color='turquoise', method='lm') 
         + geom_smooth(data = df[(df['Year'] >= policy_year) &
                                 (df['policy'] == 'Policy')], color='turquoise', method='lm')
         + geom_smooth(data = df[(df['Year'] <= policy_year) &
                                 (df['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm', se = True)
         + geom_smooth(data = df[(df['Year'] >= policy_year) &
                                 (df['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm'))
#          + ylim(0, .0004))
    pass

def did_plot_mme(df, state, policy_year, state_title):
    print (ggplot(df, aes(x ='Year', y='mme_percap',color = 'policy')) 
         + geom_point(alpha=.2) 
         + geom_vline(xintercept = policy_year) 
         + labs(title = '{0}: Diff-in-Diff Plot of Opioid Shipments'.format(state_title))
         + ylab('Opioid Shipments per Capita')
         + scale_x_continuous(breaks = ship_scale, limits= ship_yrs) 
         + geom_smooth(data = state[state['Year'] <= policy_year], 
                       color='turquoise', method='lm') 
         + geom_smooth(data = state[state['Year'] >= policy_year], 
                       color='turquoise', method='lm')
         + geom_smooth(data = df[(df['Year'] <= policy_year) &
                                 (df['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm', se = True)
         + geom_smooth(data = df[(df['Year'] >= policy_year) &
                                 (df['policy'] == 'Non-policy')], 
               color = 'red', method = 'lm', se = True))

def prepost_plot_deaths(state, policy_year, state_title):
    print (ggplot(state, aes(x ='Year', y='deaths_percap', color = 'State')) 
         + geom_point(alpha=.2, show_legend = False) 
         + scale_x_continuous(breaks = death_scale, limits = death_yrs) 
         + geom_vline(xintercept = policy_year) 
         + labs(title = '{0}: Pre-Post Plot of Overdose Deaths'.format(state_title))
         + ylab('Overdose Deaths per Capita')
         + geom_smooth(data = state[state['Year'] <= policy_year], color='red', method='lm') 
         + geom_smooth(data = state[state['Year'] >= policy_year], color='red', method='lm'))
#          + geom_text(aes(label='FIPS')))
    pass

def prepost_plot_mme(state, policy_year, state_title):
    print (ggplot(state, aes(x ='Year', y='mme_percap',color = 'State')) 
         + geom_point(alpha=.2, show_legend = False) 
         + scale_x_continuous(breaks = ship_scale, limits = ship_yrs) 
         + geom_vline(xintercept = policy_year) 
         + labs(title = '{0}: Pre-Post Plot of Opioid Shipments'.format(state_title))
         + ylab('Opioid Shipments per Capita')
         + geom_smooth(data = state[state['Year'] <= policy_year], color='red', method='lm') 
         + geom_smooth(data = state[state['Year'] >= policy_year], color='red', method='lm'))
    pass

# Florida
did_plot_deaths(fl_death_grouped, fl, fl_policy, 'Florida')
did_plot_mme(fl_mme_grouped, fl, fl_policy, 'Florida')
prepost_plot_deaths(fl, fl_policy, 'Florida')
prepost_plot_mme(fl, fl_policy, 'Florida')
# need to fix florida deaths
# outliers: 12039, 12075

# Texas
did_plot_deaths(tx_death_grouped, tx, tx_policy, 'Texas')
prepost_plot_deaths(tx, tx_policy, 'Texas')

# Washington
did_plot_deaths(wa_death_grouped, wa, wa_policy, 'Washington')
# might help to set ylim(0, .0004)
prepost_plot_deaths(wa, wa_policy, 'Washington')
