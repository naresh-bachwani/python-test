# -*- coding: utf-8 -*-
"""
Created on Sat Apr  6 21:18:33 2019

@author: Naresh
"""
from nsepy import get_history
from datetime import date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics import tsaplots
from bokeh.plotting import figure, output_file, show


#PART 1 ###########################################################################################

#Retrieves data
def get_data(name):
    data = get_history(symbol=name, start=date(2015,1,1), end=date(2016,1,1))
    
    return data

#Moving Average
def moving_avg(mylist,Weeks):
    N=Weeks*7
    cumsum, moving_aves = [0], []
    
    for i, x in enumerate(mylist, 1):
        cumsum.append(cumsum[i-1] + x)
        if i>=N:
            moving_ave = (cumsum[i] - cumsum[i-N])/N
            #can do stuff with moving_ave here
            moving_aves.append(moving_ave)
#    plot(moving_aves)
    return moving_aves

#Rolling mean
def  rolling_mean(mylist,window):
    a = mylist.rolling(window).mean()
#    plot(a)
    return(a)
    
#Volume Shock
def volume_shock(mylist):
    vol_shock=[np.nan]
    vol_shock_dir=[np.nan]
    for i in range(1,len(mylist)+1):
        if(i!=len(mylist)):
            vol_shock.append(int(abs((mylist[i]-mylist[i-1])/mylist[i-1]*100)>10))
            vol_shock_dir.append(int(((mylist[i]-mylist[i-1])/mylist[i-1]*100)>0))
    
    return vol_shock,vol_shock_dir
 
#Price Shock    
def price_shock(mylist):
    pri_shock=[np.nan]
    pri_shock_dir=[np.nan]
    for i in range(1,len(mylist)+1):
        if(i!=len(mylist)):
            pri_shock.append(int(abs((mylist[i]-mylist[i-1])/mylist[i-1]*100)>2))
            pri_shock_dir.append(int(((mylist[i]-mylist[i-1])/mylist[i-1]*100)>0))
    
    return pri_shock,pri_shock_dir

# price blackswan   
def price_blackswan(mylist):
    pri_shock=[np.nan]
    pri_shock_dir=[np.nan]
    for i in range(1,len(mylist)+1):
        if(i!=len(mylist)):
            pri_shock.append(int(abs((mylist[i]-mylist[i-1])/mylist[i-1]*100)>2))
            pri_shock_dir.append(int(((mylist[i]-mylist[i-1])/mylist[i-1]*100)>0))
    
    return pri_shock,pri_shock_dir

# shock
def shock(vol_list,price_list):
    vol_shock = volume_shock(vol_list)[0]
    pri_shock = price_shock(price_list)[0]
    sho=[np.nan]
    for i in range(1,len(vol_shock)):
        a = bool((not(vol_shock[i])) and (pri_shock[i]))
        sho.append(a)
    return sho


#PART 2###########################################################################################

#Plot timeseries
def plt_timeseries(data):
    data['indexx']=data.index
    output_file("timeseries.html")
    p = figure(plot_width=1000, plot_height=500,x_axis_type="datetime"
               ,x_axis_label='Date',y_axis_label = "Closing Price")
    # add a line renderer
    p.line(x=data.index, y =data['Close'],line_width=2)
    p.title.text = "Time Series plot"
    p.title.align = "center"
    p.title.text_font_size = "25px"
    show(p)

# Plot timeseries with volume shock in red
def plt_timeseries_volshock(data):
    volumeShock,volumeDir = volume_shock(data['Volume'])
    x = pd.Series(volumeShock)
    t =list(data.index)
    slower = np.ma.masked_where(x == 0, data['Close'])
    output_file("volshock.html")
    p = figure(plot_width=1000, plot_height=500,x_axis_type="datetime",
               x_axis_label='Date',y_axis_label = "Closing Price")
    # add a line renderer
    p.line(x=t, y =data['Close'],line_width=2,color='red',legend = "Volume Shock")
    p.line(x=t, y =slower,line_width=2,color='blue')
    p.title.text = "Time Series plot with shocks"
    p.title.align = "center"
    p.title.text_font_size = "25px"
    show(p)

# plot timeseries with shock marked
def plt_timeseries_shock(data):
    Shock = shock(data['Volume'],data['Close'])

    newdf=pd.DataFrame()
    newdf['Close']=data['Close']
    newdf['shock']= Shock
    t =list(data.index)
    a = newdf[newdf['shock']==1]['Close']
    output_file("shock.html")
    p = figure(plot_width=1000, plot_height=500,x_axis_type="datetime",
               x_axis_label='Date',y_axis_label = "Closing Price")
    # add a line renderer
    p.line(x=t, y =data['Close'],line_width=2,color='blue',legend="Shock")
    p.circle(x=a.index, y =a, color='red',legend="Shock")
    p.title.text = "SHOCK"
    p.title.align = "center"
    p.title.text_font_size = "25px"
    show(p)

#Partial autocorreltion
def partial_acf(data):
    tsaplots.plot_pacf(x=data['Close'])
    
    


#Gather data
data_TCS = get_data('TCS')
data_INFY = get_data('INFY')
'''NIFTY IT Doesn't work and import nothing i.e. 0 rows are imported although called properly'''
data_NIFTY = get_data('NIFTY IT')

#calculate moving averages for all three
mylist=data_TCS['Close']
moving_averages_TCS = []
for i in range(4,53,4):
    moving_av = moving_avg(mylist,i)
    moving_averages_TCS.append(moving_av) 
    
mylist=data_INFY['Close']
moving_averages_INFY = []
for i in range(4,53,4):
    moving_av = moving_avg(mylist,i)
    moving_averages_INFY.append(moving_av) 

mylist=data_NIFTY['Close']
moving_averages_NIFTY = []
for i in range(4,53,4):
    moving_av = moving_avg(mylist,i)
    moving_averages_NIFTY.append(moving_av) 

#PART1#######################################
#caluclate rolling mean for all three    
mylist=data_TCS['Close']
rollmean10_TCS = rolling_mean(mylist,10)
rollmean75_TCS = rolling_mean(mylist,75)

mylist=data_INFY['Close']
rollmean10_INFY = rolling_mean(mylist,10)
rollmean75_INFY = rolling_mean(mylist,75)

mylist=data_NIFTY['Close']
rollmean10_NIFTY = rolling_mean(mylist,10)
rollmean75_NIFTY = rolling_mean(mylist,75)

#calculate shocks only for TCS
volumeShock,volumeDir = volume_shock(data_TCS['Volume'])
priceShock,priceDir = price_shock(data_TCS['Close'])
priceBlack,priceBlackDir = price_blackswan(data_TCS['Close'])
Shock = shock(data_TCS['Volume'],data_TCS['Close'])

#PART2###########################################
#plot timeseries
plt_timeseries(data_TCS)
#timeseries with shock in red
plt_timeseries_volshock(data_TCS)
#time series with volume shock
plt_timeseries_shock(data_TCS)
#Partial Autocorrelation
partial_acf(data_TCS)
plt.title('Patial Autocorrelation TCS')
partial_acf(data_INFY)
plt.title('Patial Autocorrelation INFY')
#    Doesn't work because 'NIFTY IT' key does not work
#partial_acf(data_NIFTY)

