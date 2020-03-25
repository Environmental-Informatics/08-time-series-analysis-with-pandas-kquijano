# -*- coding: utf-8 -*-
"""
Karoll Quijano - kquijano

ABE 651: Environmental Informatics

Assignment 08
Time Series Analysis with Pandas

Data analysis

WabashRiver_DailyDischarge_20150317-20160324.txt
This file contains daily discharge for the Wabash River at the Lafayette, 
Indiana gauge from March 17, 2015 through March 24, 2016.
"""


import numpy as np 
import pandas as pd
from pandas import Series, DataFrame, Panel
import matplotlib.pyplot as plt


### Loading data 
wrdd = pd.read_table('WabashRiver_DailyDischarge_20150317-20160324.txt',
                     comment='#', header= 0, usecols= [2,4], delimiter='\t')                    # Import data
wrdd = wrdd.drop([0])                                                           # drop row 1
wrdd['datetime'] = pd.to_datetime(wrdd['datetime'])                             # set datetime as time series 
print(wrdd.dtypes)                                                              # Check type of data
wrdd['01_00060'] = wrdd['01_00060'].astype(float)                               # convert column 6 to float
wrdd = wrdd.set_index('datetime')                                               # set datetime as index column 
wrdd = wrdd.rename(columns={'01_00060':'Streamflow'})                          # Rename column 6
wrdd                                                                            # Check dataframe


### Create a plot of daily average streamflow for the period of record, written to a PDF or PS file.
wrdd_daily = wrdd.resample(rule='24H', closed='left', label='left').mean()      # Resample daily means and plot 
wrdd_daily.plot()
plt.title("Daily Average Streamflow")
plt.xlabel("Date")
plt.ylabel('Discharges ($ft^{3}/sec$)')
plt.savefig("Daily_average_streamflow.pdf", bbox_inches='tight')
plt.show()
#plt.close()


### Identify and plot the 10 days with highest flow
wrdd_max = wrdd_daily.nlargest(10, ['Streamflow'])                              # Select highest 10 records
fig, ax = plt.subplots()                                                        # Generate plot 
ax.plot(wrdd_daily, label='Daily average')
ax.plot(wrdd_max, marker='.', linestyle='None', markersize=8, label='Highest values')
plt.title('Daily Average Streamflow with 10 Highest Values')
plt.xlabel('Date')
plt.ylabel('Discharges ($ft^{3}/sec$)')
plt.legend()
plt.savefig('Daily_average_streamflow_high_values.pdf', bbox_inches='tight')
plt.show
#plt.close()


### Monthly average streamflow for the period of record
wrdd_m = wrdd.resample("M").median()                                                # Resample monthly median value and plot 
wrdd_m.plot()
plt.title('Monthly Average Streamflow')
plt.xlabel('Date')
plt.ylabel('Discharges ($ft^{3}/sec$)')
plt.savefig('Monthly_average_streamflow.pdf', bbox_inches='tight')
plt.show
#plt.close()















