import os
import glob
import pandas as pd
import numpy as np

os.getcwd()
os.chdir("/Users/josephlee/estimating-impact-of-opioid-prescription-regulations-team-7/10_code/Concatenate")
#os.chdir("C:/Duke/2019_fall/690_python/estimating-impact-of-opioid-prescription-regulations-team-7/10_code/Concatenate")

# concatenate 51 files and export : "output.csv"
interesting_files = glob.glob("/Users/josephlee/estimating-impact-of-opioid-prescription-regulations-team-7/10_code/Concatenate/*grouped.csv") 
#interesting_files = glob.glob("C:/Duke/2019_fall/690_python/estimating-impact-of-opioid-prescription-regulations-team-7//10_code/Concatenate/*grouped.csv") 

df = pd.concat((pd.read_csv(f, header = 0,index_col=False) for f in interesting_files), )
df.to_csv("output.csv",index = False)


#
df1 = pd.read_csv("output.csv",index_col = False)
df1.head()

