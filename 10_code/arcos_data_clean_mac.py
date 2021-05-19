#from arcos_data_clean import clean
import pandas as pd
import os
dir_path = os.path.dirname(os.path.realpath('arcos_data_clean.py'))#set .py file path for future use
lst = ['ar','de','fl','tx','wa']
#lst = ['al','az','ca','co', 'ct','ga','hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md','me','mi','mn','mo','ms','mt','ne','nv', 'nh', 'nj','nm','ny','nc', 'nd', 'oh', 'ok', 'or', 'pa', 'pr', 'ri' , 'sc','sd','tn','ut','vt', 'va', 'wv', 'wi', 'wy'] 
#except Alaska and Washington D.c.
#create read list  ##backup 'fl','wa','tx','ak','al','az','ca','co', 'ct','ga','hi', 'ia', 'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md','me','mi','mn',
for i in lst:
    read_file = "/Users/josephlee/Downloads/arcos-{}-statewide-itemized.tsv.gz".format(i)#read file name
    print("now process {} data".format(i))
    df = pd.read_csv(read_file, sep="\t")#read files
#df.shape
#list(df.columns.values)
#take a look at elemants and column names
# since reporters are all distributer we can drop it
######drop columns that we think we don't need
    df1 = df.drop(columns = ['REPORTER_BUS_ACT','REPORTER_ADDRESS1', 'REPORTER_DEA_NO','REPORTER_NAME' ,'REPORTER_ADDL_CO_INFO' , 'REPORTER_ADDRESS1' , 'REPORTER_ADDRESS2' , 'REPORTER_CITY' ,'REPORTER_ZIP' , 'REPORTER_COUNTY' , 'BUYER_DEA_NO' , 'BUYER_ADDL_CO_INFO' , 'BUYER_ADDRESS1' , 'BUYER_ADDRESS2' , 'Product_Name' , 'Reporter_family'  , 'Combined_Labeler_Name' , 'Revised_Company_Name' , 'Measure' , 'ORDER_FORM_NO' , "CORRECTION_NO" , 'CORRECTION_NO' , 'ACTION_INDICATOR','ORDER_FORM_NO', 'CORRECTION_NO', 'STRENGTH', 'REPORTER_STATE', 'Combined_Labeler_Name','TRANSACTION_ID','Ingredient_Name', 'Measure', 'BUYER_NAME', 'BUYER_CITY','NDC_NO', 'Revised_Company_Name' , 'UNIT' , "DRUG_NAME" , "TRANSACTION_CODE","BUYER_ZIP"])##  this sounds important 'MME_Conversion_Factor'
#list(df1.columns.values)#check columns again
#df1.shape## check data frame size
#df1.head()
######or, we can just drop any columns that contains na value
#df1 = df.dropna(axis='columns')# might not be a good idea
#########

    df1["year"] = df1["TRANSACTION_DATE"]%10000 ##extract year
    #df1["month"] = (df1["TRANSACTION_DATE"]//10000)//100 ## extract month
    #df1["year/month"] = df1["year"] *100 + df1["month"]#combine year and month
    df1 = df1.drop(columns = ['TRANSACTION_DATE'])#drop original column       'month'
#df1.head()
######group data together#######
###### still in progress ######
    df2 = df1.copy() #mak a copy
    df2['quantity'] = df1.groupby(['BUYER_COUNTY', 'year', 'DRUG_CODE', "MME_Conversion_Factor"])["QUANTITY"].transform(sum)
#aggregation function and group data by county and month    ###I keep df1 unchanged for possible future need
#df2.head()
#df2 = df1.groupby([ 'BUYER_COUNTY', 'year/month', 'DRUG_CODE',"BUYER_STATE"], as_index = False).sum()
    df2 = df2.drop('QUANTITY',axis=1) 
    df2['MME'] = df2['CALC_BASE_WT_IN_GM'] * df2['MME_Conversion_Factor']
    df2 = df2.drop_duplicates(subset = ['BUYER_STATE','year', 'DRUG_CODE','quantity', 'MME'], keep='first').copy()
    write = "/Users/josephlee/Downloads/{}_cleaned_grouped.csv".format(i.upper())
    df2.to_csv(write, index =False)
######end of first clean stage##########






"""
#df2['dos_total'] = df2.apply(lambda x : (df2['CALC_BASE_WT_IN_GM'] * df2['DOSAGE_UNIT'] * df2['dos_str']))#dos total = calc wt in gm *unit * strength
#df2 = df2.drop(columns = ['CALC_BASE_WT_IN_GM','DOSAGE_UNIT','dos_str'])
#df3 = df2.drop_duplicates(subset = ['BUYER_COUNTY', 'year/month', 'DRUG_CODE','quantity','dos_total'], keep='first').copy()
#df3.shape
os.chdir(dir_path)#change directory to repository path
#df3.to_csv("CA_cleaned_grouped.csv")#save cleaned data to project folder



#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#===============================================================================
#######we don't need them... maybe, leave them in case we still need them####
############################################################################
######################### clean Product_Name column ########################
############################################################################
##change the column names to see if there's anything should be modified
#########use replace to merge data that represent same thing but in different string name#######
df1['Product_Name'] = df1['Product_Name'].replace(to_replace = ['HYDROCODONE BIT. 7.5MG/ACETAMINOPHEN', 'HYDROCODONE BIT.7.5MG/ACETAMINOPHEN','HYDROCODONE BITARTRATE & ACETA 7.5MG','HYDROCODONE BITARTRATE AND ACETA 7.5','HYDROCODONEBITARTRATE & ACETA  7.5MG'], value = 'HYDROCODONE BIT. 7.5MG/ACETAMINOPHEN').copy()
set(df1['Product_Name'])####after replace, we take a look of the column again to see if still need further modification
df1['Product_Name'] = df1['Product_Name'].replace(to_replace = [ 'HYDROCODONE BIT. 10MG/ACETAMINOPHEN','HYDROCODONE BITARTRATE 10MG/ACETAMIN','HYDROCODONE BITARTRATE AND ACETA 10M'], value = 'HYDROCODONE BIT. 10MG/ACETAMINOPHEN').copy()
set(df1['Product_Name'])
############################################################################

set(df1['BUYER_BUS_ACT'])
df1.loc[df1["BUYER_BUS_ACT"]=="CHAIN PHARMACY"]
df1.loc[df1["BUYER_BUS_ACT"]=="RETAIL PHARMACY"]
df1['BUYER_BUS_ACT'] = df1['BUYER_BUS_ACT'].replace(to_replace = ["PRACTITIONER-DW/275"], value = 'PRACTITIONER').copy()
set(df1['QUANTITY'])



datalist = list()
for row, date in enumerate(arcos_fl['TRANSACTION_DATE']):
    date_raw = str(date)
    date_object = datetime.strptime(date_raw, '%m%d%Y')
    #date_string = date_object.strftime('%m/%d/%Y')
    date_string = date_object.strftime('%Y')
    datalist.append(date_string)
arcos_fl['Year'] = pd.DataFrame(datalist)
arcos_fl = arcos_fl.drop(['TRANSACTION_DATE'], axis=1)

arcos_fl = arcos_fl.groupby(['BUYER_COUNTY','Year','DRUG_CODE'], as_index=False).sum()
#==========================================================================================


###############################################
###try to build a class for future use#########
###############################################
from arcos_data_clean import clean

#from point import Point
#from math import pi, acos, sqrt


class clean(object):
"""
#    """
#    This is class that will help you clean arcos data
#    """
"""
    #self will be a data frame
    import pandas as pd
    def read(self):
        assert self == pd.core.frame.DataFrame "input should be data frame"
        self = self.drop(columns = ['REPORTER_BUS_ACT','REPORTER_ADDRESS1', 'REPORTER_DEA_NO','REPORTER_NAME' ,'REPORTER_ADDL_CO_INFO' , 'REPORTER_ADDRESS1' , 'REPORTER_ADDRESS2' , 'REPORTER_CITY' ,'REPORTER_ZIP' , 'REPORTER_COUNTY' , 'BUYER_DEA_NO' , 'BUYER_ADDL_CO_INFO' , 'BUYER_ADDRESS1' , 'BUYER_ADDRESS2' , 'Product_Name' , 'Reporter_family' , 'MME_Conversion_Factor' , 'Combined_Labeler_Name' , 'Revised_Company_Name' , 'Measure' , 'ORDER_FORM_NO' , "CORRECTION_NO" , 'CORRECTION_NO' , 'ACTION_INDICATOR' , 'ORDER_FORM_NO', 'CORRECTION_NO', 'STRENGTH', 'Combined_Labeler_Name','TRANSACTION_ID','Ingredient_Name', 'Measure', 'BUYER_NAME', 'BUYER_CITY' , 'NDC_NO' , 'Revised_Company_Name' , 'UNIT' , "DRUG_NAME" , "TRANSACTION_CODE","BUYER_ZIP"])
#    def __init__(self, c=Point(), r=1):
#        assert(r >= 0)
#        self.center = c
#        self.radius = r
    def time(self):
        #df2 = df1[['TRANSACTION_DATE', "BUYER_STATE"]].copy() #create a data frame for computation need
        #df2.head()#take a look!
        df1["year"] = df1["TRANSACTION_DATE"]%10000 ##extract year
        df1["month"] = (df1["TRANSACTION_DATE"]//10000)//100 ##extract month and date to df2 for futher computation
        #df1["month"] = df2["month and date"]//100 ## extract month
        df1["year/month"] = df1["year"]*100 + df1["month"]#combine year and month
        df1 = df1.drop(columns = ['TRANSACTION_DATE', 'year', 'month'])#drop useless columns  ,'day'
    def agg(self):
        
        
    def __str__(self):
        return '({}, {})'.format(self.center, self.radius)

    def __repr__(self):
        return 'Circle' + Circle.__str__(self)

    def move(self, dx, dy):
        self.center.move(dx,dy)

    def intersection_area(self, another_circle):
        r = self.radius
        R = another_circle.radius
        d = self.center.distance_from(another_circle.center)

        if d <= abs(R-r):
           return pi*min(r, R)**2
        elif d >= r + R:
            return 0

        else:
            return ( r**2*acos((d**2 + r**2 - R**2)/(2*d*r)) + R**2*acos((d**2 + R**2 - r**2)/(2*d*R)) - 0.5*sqrt((R+r-d)*(d+r-R)*(d-r+R)*(d+r+R)) )#itr_csv = pd.read_csv("arcos-fl-statewide-itemized.tsv.gz", iterator=True, chunksize=500000, low_memory = False, encoding = 'utf-8',error_bad_lines=False) 
#df = pd.concat([chunk for chunk in itr_csv]) ##failed to load in chunk.... don't know why
#to_parquet(df, FL_drug, engine='auto', compression='snappy', index=None, partition_cols=None, **kwargs)### doesn't work....
"""
"""
from datetime import datetime
date = datetime.striptime(str(df1['ACTION_INDICATOR']),'%m%d%Y')####process with string data
date.strftime()####we can use datetime to process date data
"""