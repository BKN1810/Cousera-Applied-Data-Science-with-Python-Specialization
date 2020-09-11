
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[27]:


import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[21]:


# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[23]:


def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''   
    
    with open('university_towns.txt') as file:
        data = []
        for line in file:
            data.append(line[:-1])
            #print(data)
            
    state_town = []
    for line in data:
        if line.endswith('[edit]'):
            state=line[:line.find('[')].strip()
            #print(state)
            
        elif '(' in line:
            town = line[:(line.index('(')-1)]
            #print(town)
            state_town.append([state,town])
        else:
            town = line.rstrip()
            state_town.append([state,town])
            
    #print(state_town)
    df_town_state = pd.DataFrame(state_town, columns = ['State','RegionName']) 
    
    return df_town_state  ###ANSWER

get_list_of_university_towns()


# In[38]:


def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', skiprows = 7)
    df = df[['Unnamed: 4','Unnamed: 5']]
    df.columns = ['Quarter','GDP']
    #print(df.tail(10))
    ############################################################
    df = df.iloc[212:]
    df.reset_index(inplace=True, drop=True)
    #print(df.tail(10))
    
    recession_start = []
    for i in range(len(df) - 4):
        if ((df.iloc[i][1] > df.iloc[i+1][1]) & (df.iloc[i+1][1] > df.iloc[i+2][1])):
            recession_start.append(df.iloc[i][0])

    recession_quarter = recession_start[0]
    
    return recession_quarter    ###"ANSWER"

get_recession_start()


# In[39]:


def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', skiprows = 7)
    df = df[['Unnamed: 4','Unnamed: 5']]
    df.columns = ['Quarter','GDP']
    #print(df.tail(10))
    ############################################################
    df = df.iloc[212:]
    df.reset_index(inplace=True, drop=True)
    #print(df.tail(10))
    
    
    recession_end = []
    for i in range(len(df) - 4):
        if ((df.iloc[i][1] > df.iloc[i+1][1]) & (df.iloc[i+1][1] > df.iloc[i+2][1]) & (df.iloc[i+2][1] < df.iloc[i+3][1]) & (df.iloc[i+3][1] < df.iloc[i+4][1])):
            recession_end.append([df.iloc[i][0],df.iloc[i+1][0],df.iloc[i+2][0],df.iloc[i+3][0],df.iloc[i+4][0]])

    recession_end_quarter = recession_end[0][4]
       
    return recession_end_quarter   ###"ANSWER"

get_recession_end()


# In[40]:


def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', skiprows = 7)
    df = df[['Unnamed: 4','Unnamed: 5']]
    df.columns = ['Quarter','GDP']
    #print(df.tail(10))
    ############################################################
    df = df.iloc[212:]
    df.reset_index(inplace=True, drop=True)
    #print(df.tail(10))
    
    recession_end = []
    for i in range(len(df) - 4):
        if ((df.iloc[i][1] > df.iloc[i+1][1]) & (df.iloc[i+1][1] > df.iloc[i+2][1]) & (df.iloc[i+2][1] < df.iloc[i+3][1]) & (df.iloc[i+3][1] < df.iloc[i+4][1])):
            recession_end.append([df.iloc[i][0],df.iloc[i+1][0],df.iloc[i+2][0],df.iloc[i+3][0],df.iloc[i+4][0]])

    recession_bottom = recession_end[0][2]
       
    return recession_bottom   ###"ANSWER"
    
get_recession_bottom()


# In[41]:


def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    df = df.drop(df.columns[[0] + list(range(3,51))], axis=1)
    #print(df.head())
    df1=pd.DataFrame(df,columns=["State","RegionName"])
    #print(df1.head())
    ##################################################################################################
    
    for year in range(2000, 2016):
        df1[str(year) + 'q1'] = df[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis = 1)
        df1[str(year) + 'q2'] = df[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis = 1)
        df1[str(year) + 'q3'] = df[[str(year) + '-07', str(year) + '-08', str(year) + '-09']].mean(axis = 1)
        df1[str(year) + 'q4'] = df[[str(year) + '-10', str(year) + '-11', str(year) + '-12']].mean(axis = 1)
    
    year = 2016
    df1[str(year) + 'q1'] = df[[str(year) + '-01', str(year) + '-02', str(year) + '-03']].mean(axis = 1)
    df1[str(year) + 'q2'] = df[[str(year) + '-04', str(year) + '-05', str(year) + '-06']].mean(axis = 1)
    df1[str(year) + 'q3'] = df[[str(year) + '-07', str(year) + '-08']].mean(axis = 1)
    
    #############################################################################################################
    
    df1['State'] = [states[state] for state in df1['State']]
    df1 = df1.set_index(['State', 'RegionName'])
    #print(df1.shape)
    #print(type(df1))
    
    return  df1   ###"ANSWER"

convert_housing_data_to_quarters()


# In[42]:


def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    unitowns = get_list_of_university_towns()
    bottom = get_recession_bottom()
    start = get_recession_start()
    hdata = convert_housing_data_to_quarters()
    bstart = hdata.columns[hdata.columns.get_loc(start) - 1]
    
    hdata['ratio'] =  hdata[bstart] - hdata[bottom]
    hdata = hdata[[bottom, bstart, 'ratio']]
    hdata = hdata.reset_index()
    
    unitowns_hdata = pd.merge(hdata,unitowns,how='inner',on=['State','RegionName'])
    unitowns_hdata['uni'] = True
    hdata2 = pd.merge(hdata, unitowns_hdata, how='outer', on=['State','RegionName',bottom, bstart, 'ratio'])
    hdata2['uni'] = hdata2['uni'].fillna(False)
    
    ut = hdata2[hdata2['uni'] == True]
    nut = hdata2[hdata2['uni'] == False]
    
    t,p = ttest_ind(ut['ratio'].dropna(), nut['ratio'].dropna())
    
    different = True if p<0.01 else False
    better = "university town" if ut['ratio'].mean() < nut['ratio'].mean() else "non-university town"
    
    return(different, p, better)

run_ttest()


# In[ ]:




