#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import os

# os.listdir('./00_source/population/')


# ### 2015

# In[2]:


df_2015 = pd.read_csv('./00_source/population/nhgis0002_ds215_20155_2015_county.csv', encoding='latin-1')


# In[3]:


is_none = df_2015.columns[df_2015.isna().any()].tolist()


# In[4]:


df_cleaned_2015 = df_2015.drop(columns=is_none)


# In[5]:


df_2015 = df_cleaned_2015.drop(columns=['GISJOIN', 'NAME_M', 'ADKWM001'])


# In[6]:


df_2015 = df_2015.rename(columns={'ADKWE001': 'population'})


# In[7]:


df_2015['year'] = 2015


# In[8]:


df_2015 = df_2015.drop(columns='YEAR')


# In[9]:


df_2015['countyfips'] = df_2015['STATEA'] * 1000 + df_2015['COUNTYA']


# In[10]:


statea_name_dict = dict(zip(df_2015['STATEA'], df_2015['STATE']))


# ### 2006 - 2012

# In[11]:


data_all = pd.read_csv('./00_source/population/pop_counties_20062012.csv')


# In[12]:


data_all = data_all.reset_index(drop=True)


# In[13]:


statea_code_dict = dict(zip(data_all['STATE'], data_all['BUYER_STATE']))
county_dict = dict(zip(data_all['COUNTY'], data_all['county_name']))


# In[14]:


df_2012 = data_all[data_all['year'] == 2012]


# ### 2013 - 2015

# In[15]:


data_main = df_2012.copy()


# In[16]:


data_main = data_main.rename(columns={'population':'population_2012'})


# In[17]:


a = data_main['countyfips'].reset_index(0)


# In[18]:


df_2015 = df_2015.rename(columns={'population': 'population_2015'})


# In[19]:


data_merged = data_main.merge(df_2015, how='outer', on='countyfips', indicator=True)


# In[20]:


data_merged = data_main.merge(df_2015, how='left', on='countyfips', indicator=True)


# In[21]:


data_main = data_main.set_index('countyfips')


# In[22]:


data_merged = data_merged.set_index('countyfips')


# In[23]:


data_main['population_2015'] = data_merged['population_2015']


# In[24]:


data_main['population_2013'] = round((data_main['population_2015'] - data_main['population_2012']) / 3 + data_main['population_2012'])


# In[25]:


data_main['population_2014'] = round((data_main['population_2015'] - data_main['population_2012']) / 3 + data_main['population_2013'])


# In[26]:


df_13 = data_all.copy()


# In[27]:


df_13 = data_main.copy()
df_13 = df_13.drop(columns=['population_2015', 'population_2014', 'population_2012'])
df_13['year'] = 2013
df_13 = df_13.reset_index()
df_13 = df_13.rename(columns={'population_2013': 'population'})


# In[28]:


df_14 = data_main.copy()
df_14 = df_14.drop(columns=['population_2015', 'population_2013', 'population_2012'])
df_14['year'] = 2014
df_14 = df_14.reset_index()
df_14 = df_14.rename(columns={'population_2014': 'population'})


# In[29]:


df_15 = data_main.copy()
df_15 = df_15.drop(columns=['population_2013', 'population_2014', 'population_2012'])
df_15['year'] = 2015
df_15 = df_15.reset_index()
df_15 = df_15.rename(columns={'population_2015': 'population'})


# In[30]:


data_all = data_all.append(df_13, sort=True)


# In[31]:


data_all = data_all.append(df_14, sort=True)


# In[32]:


data_all = data_all.append(df_15, sort=True)


# In[33]:


data_all = data_all.drop(columns=['BUYER_COUNTY', 'NAME', 'variable'])
data_all = data_all.rename(columns={'STATE': 'STATEA', 'BUYER_STATE':'STATE', 'COUNTY': 'COUNTYA'})


# ### 2003

# In[34]:


df_03 = pd.read_csv('./00_source/population/nhgis0002_ds231_2003_county.csv')
df_03 = df_03.reset_index(drop=True)
df_03 = df_03.drop(columns=['GISJOIN', 'DATAFLAG', 'NOTECODE', 'AREANAME', 'STATE'])
df_03 = df_03.rename(columns={'YEAR': 'year', 'AGWD001': 'population', 'COUNTY': 'county_name'})
df_03['STATEA'] = df_03['STATEA'].apply(lambda x: x//10)
df_03['COUNTYA'] = df_03['COUNTYA'].apply(lambda x: x//10)
df_03['STATE'] = df_03['STATEA'].apply(lambda x: statea_code_dict[x])
df_03['countyfips'] = df_03['STATEA'] * 1000 + df_03['COUNTYA']


# In[35]:


data_all = data_all.append(df_03, sort=True)


# ### 2004

# In[36]:


df_04 = pd.read_csv('./00_source/population/nhgis0002_ds231_2004_county.csv')
df_04 = df_04.reset_index(drop=True)
df_04 = df_04.drop(columns=['GISJOIN', 'DATAFLAG', 'NOTECODE', 'AREANAME', 'STATE'])
df_04 = df_04.rename(columns={'YEAR': 'year', 'AGWD001': 'population', 'COUNTY': 'county_name'})
df_04['STATEA'] = df_04['STATEA'].apply(lambda x: x//10)
df_04['COUNTYA'] = df_04['COUNTYA'].apply(lambda x: x//10)
df_04['STATE'] = df_04['STATEA'].apply(lambda x: statea_code_dict[x])
df_04['countyfips'] = df_04['STATEA'] * 1000 + df_04['COUNTYA']


# In[37]:


data_all = data_all.append(df_04, sort=True)


# ### 2005

# In[38]:


df_05 = pd.read_csv('./00_source/population/nhgis0002_ds231_2005_county.csv')
df_05 = df_05.reset_index(drop=True)
df_05 = df_05.drop(columns=['GISJOIN', 'DATAFLAG', 'NOTECODE', 'AREANAME', 'STATE'])
df_05 = df_05.rename(columns={'YEAR': 'year', 'AGWD001': 'population', 'COUNTY': 'county_name'})
df_05['STATEA'] = df_05['STATEA'].apply(lambda x: x//10)
df_05['COUNTYA'] = df_05['COUNTYA'].apply(lambda x: x//10)
df_05['STATE'] = df_05['STATEA'].apply(lambda x: statea_code_dict[x])
df_05['countyfips'] = df_05['STATEA'] * 1000 + df_05['COUNTYA']


# In[39]:


data_all = data_all.append(df_05, sort=True)


# #### clean all data

# In[40]:


data_all = data_all.sort_values(by=['year', 'STATEA'])
data_all = data_all.reset_index(drop=True)


# In[46]:


data_all = data_all.rename(columns={'county_name': 'county', 'STATE': 'state'})


# In[47]:


data_all


# In[51]:


cols=['year', 'state', 'county', 'STATEA', 'COUNTYA', 'countyfips', 'population']
data_all.to_csv('./00_source/population/population_03-15.csv', index=False, columns=cols)


# ## group by state

# In[56]:


data_all


# In[61]:


data_state = data_all.groupby(['state', 'year'], as_index=False)['population'].agg('sum')


# In[63]:


data_state.to_csv('./00_source/population/state_population_03-15.csv', index=False)


# In[ ]:




