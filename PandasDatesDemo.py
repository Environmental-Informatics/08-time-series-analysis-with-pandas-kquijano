# -*- coding: utf-8 -*-
"""
Karoll Quijano - kquijano

ABE 651: Environmental Informatics

Assignment 08
Time Series Analysis with Pandas

Tutorial at http://earthpy.org/pandas-basics.html
time series analysis of Arctic Oscillation (AO) and North Atlantic Oscillation (NAO) data sets. 
"""


"""
NOTE:
    Line 32 and 65 must be run 
"""


### Import libraries

import numpy as np 
import pandas as pd
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt

pd.set_option('display.max_rows',15)                                # this limit maximum numbers of rows


### Loading data 
!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/daily_ao_index/monthly.ao.index.b50.current.ascii   ### RUN THIS LINE ALONE
ao = np.loadtxt('monthly.ao.index.b50.current.ascii')               # Import AO data


ao[0:2]

ao.shape


### Time Series

dates = pd.date_range('1950-01', periods=ao.shape[0], freq='M')     # create the range of dates for the time series
dates 
dates.shape


AO = Series(ao[:,2], index=dates)                                   # Creates the time series
AO

AO.plot()
plt.savefig('Daily_Atlantic_Oscillation_AO_plot_Out23.png')

AO['1980':'1990'].plot()                                            # plots a part of the data 
AO['1980-05':'1981-03'].plot()                                      # plots a smaller part of the data 

AO[120]                                                             # Rreferencing an individual value
AO['1960-01']                                                       # Rreferencing a value by its index
AO['1960']                                                          # Rreferencing values by a year 
AO[AO > 0]                                                          # Rreferencing values by a range


### Data Frame 

!wget http://www.cpc.ncep.noaa.gov/products/precip/CWlink/pna/norm.nao.monthly.b5001.current.ascii           ### RUN THIS LINE ALONE              
nao = np.loadtxt('norm.nao.monthly.b5001.current.ascii')            # Import NAO data 
dates_nao = pd.date_range('1950-01', periods=nao.shape[0], freq='M')# Create time series
NAO = Series(nao[:,2], index=dates_nao)

NAO.index



aonao = DataFrame({'AO' : AO, 'NAO' : NAO})                         # Creates data frame with AO and NAO data
aonao                                                               # last row is with empty values (NaN) for NAO data 

aonao.plot(subplots=True)                                           # Plot data 



aonao.head()
aonao.tail()

aonao['NAO']                                                        # Reference each column by its name
aonao.NAO                                                           # Reference each column by its name

aonao['Diff'] = aonao['AO'] - aonao['NAO']                          # Add a column to the Data Frame 
aonao.head()

del aonao['Diff']                                                   # Deletes a column in the Data Frame
aonao.tail()


aonao['1981-01':'1981-03']                                          # Slicing 

import datetime
aonao.loc[(aonao.AO > 0) & (aonao.NAO < 0)                          # Special intexing attribute 
        & (aonao.index > datetime.datetime(1980,1,1))               # Choose all NAO values in the 1980s for months where AO is positive 
        & (aonao.index < datetime.datetime(1989,1,1)),              # and NAO is negative
        'NAO'].plot(kind='barh')                                    # plots 


### Statistics 

aonao.mean()            # Column-wise. by default
aonao.max()
aonao.min()

aonao.mean(1)           # Row-wise

aonao.describe()        # Simple stats for the data frame



### Resampling 

AO = AO.iloc[:816]                                  # Removes last rows 
AO

AO_mm = AO.resample("A").mean()                     # Resamples annual means and plot
AO_mm.plot(style='g--')

AO_mm = AO.resample("A").median()                   # Resample annual median value and plot 
AO_mm.plot()
plt.savefig('Annual_median_values_for_AO_Out_48.png')

AO_mm = AO.resample("3A").apply(np.max)             # Resampling frecuency to 3 years
AO_mm.plot()

AO_mm = AO.resample("A").apply(['mean', np.min, np.max]) #Plot a list of functions
AO_mm['1900':'2020'].plot(subplots=True)
AO_mm['1900':'2020'].plot()

AO_mm


### Moving (Rolling) Statistics

aonao.rolling(window=12, center=False).mean().plot(style='-g')              # Rolling means 
plt.savefig('Rolling_mean_for_both_AO_and_NAO_Out_52.png')

aonao.AO.rolling(window=120).corr(other=aonao.NAO).plot(style='-g')         # Rolling correlation 

aonao.corr()                                                                # Correlation coefficients 