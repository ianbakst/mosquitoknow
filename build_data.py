#!/usr/local/bin/python

import numpy as np
import pandas as pd
import geopandas as gpd
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
from darksky import forecast
import datetime as dt
from noaa_sdk import noaa
import pickle
import descartes
import geopandas as gpd
from shapely.geometry import Point, Polygon

n = noaa.NOAA()
noaakey = 'LsIneJLfjoLBjuBphdeUGyJLVJdXWRpK'
dskey = '6864d54f724e54e7c3ae08094f523ff0'

data = pd.read_csv('data/West_Nile_Virus__WNV__Mosquito_Test_Results.csv')
data = data.rename(columns={"TEST DATE": "date",
                            "NUMBER OF MOSQUITOES":"num",
                            "LATITUDE":"lat","LONGITUDE":"lon",
                            "TRAP":"trap",
                            "SEASON YEAR":"year",
                            "WEEK":"week",
                            "Census Tracts":"tract",
                            "Zip Codes":"zip",
                            "Community Areas":"community",
                            "Historical Wards 2003-2015":"ward"})
data['date'] = pd.to_datetime(data['date'])
data['date'] = data['date'].dt.date
data = data.dropna()
sum_traps = data.groupby(["trap","date"]).sum().reset_index()
data = data.groupby(["trap","date"]).mean().reset_index()
data['num'] = sum_traps['num']

crs = {'init': 'epsg:4326'}
water_map = gpd.read_file('water/chicago_latlon.shp')
park_map = gpd.read_file('parks/chicago_parks1.shp')
forest_map =gpd.read_file('forest/forest.shp')
by_trap = data.groupby('trap').mean()
by_trap = by_trap.reset_index(drop=False)
geometry = [Point(xy) for xy in zip(by_trap.lon,by_trap.lat)]
geo_traps = gpd.GeoDataFrame(by_trap, crs = crs, geometry = geometry)
geo_traps = geo_traps.reset_index(drop=False)

green_geo = park_map.geometry.append(forest_map.geometry)

green_map = gpd.GeoDataFrame(crs = crs, geometry = green_geo)
green_map = green_map.reset_index(drop=False)

data_geometry = [Point(xy) for xy in zip(data.lon,data.lat)]
geo_data = gpd.GeoDataFrame(data, crs = crs, geometry = data_geometry)

geo_traps['d_water'] = 0.
geo_traps['d_park'] = 0.

for i,point in geo_traps.iterrows():
    distw = np.ones(shape=(len(water_map),1))
    distf = np.ones(shape=(len(green_map),1))
    for j,lake in water_map.iterrows():
        distw[j] = point['geometry'].distance(lake['geometry'])
    for j,tree in green_map.iterrows():
        distf[j] = point['geometry'].distance(tree['geometry'])
    geo_traps.loc[i,'d_water'] = min(distw)
    geo_traps.loc[i,'d_park'] = min(distf)

geo_data['d_water'] = 0.
geo_data['d_park'] = 0.
for i,point in geo_data.iterrows():
    geo_data.loc[i,'d_water']=geo_traps[geo_traps.trap==point.trap]['d_water'].values[0]
    geo_data.loc[i,'d_park']=geo_traps[geo_traps.trap==point.trap]['d_park'].values[0]

geo_data['since']=100.
group_trap = geo_data.groupby('trap')
for trap,tdata in group_trap:
    T = tdata.sort_values(by = 'date', ascending = False)
    l = len(T) - 1
    for i in range(l):
        date = T.date.iloc[i]
        DT = (date - T.date.iloc[i+1]).total_seconds()/86400.
        ind = ((geo_data.date == date)&(geo_data.trap == trap))
        p = np.where(ind)[0]
        geo_data.since.iloc[p] = DT

w1=pd.read_csv('w1.csv')
w2=pd.read_csv('w2.csv')
w=pd.concat([w1, w2])
w.info
w = w.reset_index(drop=False)
w = w.rename(columns={"DATE": "date",
                            "PRCP":"p",
                            "TAVG":"Tavg","TMAX":"Tmax",
                            "TMIN":"Tmin","AWND":"w_sp","WDF5":"w_d"})
w['date'] = pd.to_datetime(w['date'])
w['date'] = w['date'].dt.date

geo_data['TH0']=0.
geo_data['TL0']=0.
geo_data['TH1']=0.
geo_data['TL1']=0.
geo_data['TH2']=0.
geo_data['TL2']=0.
geo_data['TH3']=0.
geo_data['TL3']=0.
geo_data['TH4']=0.
geo_data['TL4']=0.
geo_data['TH5']=0.
geo_data['TL5']=0.
geo_data['TH6']=0.
geo_data['TL6']=0.
geo_data['TH7']=0.
geo_data['TL7']=0.
geo_data['TH8']=0.
geo_data['TL8']=0.
geo_data['TH9']=0.
geo_data['TL9']=0.
geo_data['TH10']=0.
geo_data['TL10']=0.
geo_data['p0']=0.
geo_data['p1']=0.
geo_data['p2']=0.
geo_data['p3']=0.
geo_data['p4']=0.
geo_data['p5']=0.
geo_data['p6']=0.
geo_data['p7']=0.
geo_data['p8']=0.
geo_data['p9']=0.
geo_data['p10']=0.
geo_data['Tmax']=0.
geo_data['Tmin']=0.
geo_data['prec']=0.
geo_data['w_sp']=0.
geo_data['w_d']=0.
geo_data['dtm']=0.
geo_data['dtl']=0.
geo_data = geo_data[(geo_data['date'] > pd.to_datetime('2007-06-11'))]

for i in range(len(geo_data)):
    d0 = geo_data['date'].iloc[i]
    d1 = d0 + pd.DateOffset(-1)
    d2 = d0 + pd.DateOffset(-2)
    d3 = d0 + pd.DateOffset(-3)
    d4 = d0 + pd.DateOffset(-4)
    d5 = d0 + pd.DateOffset(-5)
    d6 = d0 + pd.DateOffset(-6)
    d7 = d0 + pd.DateOffset(-7)
    d8 = d0 + pd.DateOffset(-8)
    d9 = d0 + pd.DateOffset(-9)
    d10 = d0 + pd.DateOffset(-10)
    TH0 = w[w.date == d0]['Tmax'].values[0]
    TL0 = w[w.date == d0]['Tmin'].values[0]
    TH1 = w[w.date == d1]['Tmax'].values[0]
    TL1 = w[w.date == d1]['Tmin'].values[0]
    TH2 = w[w.date == d2]['Tmax'].values[0]
    TL2 = w[w.date == d2]['Tmin'].values[0]
    TH3 = w[w.date == d3]['Tmax'].values[0]
    TL3 = w[w.date == d3]['Tmin'].values[0]
    TH4 = w[w.date == d4]['Tmax'].values[0]
    TL4 = w[w.date == d4]['Tmin'].values[0]
    TH5 = w[w.date == d5]['Tmax'].values[0]
    TL5 = w[w.date == d5]['Tmin'].values[0]
    TH6 = w[w.date == d6]['Tmax'].values[0]
    TL6 = w[w.date == d6]['Tmin'].values[0]
    TH7 = w[w.date == d7]['Tmax'].values[0]
    TL7 = w[w.date == d7]['Tmin'].values[0]
    TH8 = w[w.date == d8]['Tmax'].values[0]
    TL8 = w[w.date == d8]['Tmin'].values[0]
    TH9 = w[w.date == d9]['Tmax'].values[0]
    TL9 = w[w.date == d9]['Tmin'].values[0]
    TH10 = w[w.date == d10]['Tmax'].values[0]
    TL10 = w[w.date == d10]['Tmin'].values[0]
    Tmax = max([TH0,TH1,TH2,TH3,TH4,TH5,TH6,TH7,TH8,TH9,TH10])
    Tmin = min([TL0,TL1,TL2,TL3,TL4,TL5,TL6,TL7,TL8,TL9,TL10])
    p0 = w[w.date == d0]['p'].values[0]
    p1 = w[w.date == d1]['p'].values[0]
    p2 = w[w.date == d2]['p'].values[0]
    p3 = w[w.date == d3]['p'].values[0]
    p4 = w[w.date == d4]['p'].values[0]
    p5 = w[w.date == d5]['p'].values[0]
    p6 = w[w.date == d6]['p'].values[0] 
    p7 = w[w.date == d7]['p'].values[0]
    p8 = w[w.date == d8]['p'].values[0]
    p9 = w[w.date == d9]['p'].values[0]
    p10 = w[w.date == d10]['p'].values[0]
    precip = [p0,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10]
    prec=sum(precip)
    geo_data['TH0'].iloc[i]=TH0
    geo_data['TH1'].iloc[i]=TH1
    geo_data['TH2'].iloc[i]=TH2
    geo_data['TH3'].iloc[i]=TH3
    geo_data['TH4'].iloc[i]=TH4
    geo_data['TH5'].iloc[i]=TH5
    geo_data['TH6'].iloc[i]=TH6
    geo_data['TH7'].iloc[i]=TH7
    geo_data['TH8'].iloc[i]=TH8
    geo_data['TH9'].iloc[i]=TH9
    geo_data['TH10'].iloc[i]=TH10
    geo_data['TL0'].iloc[i]=TL0
    geo_data['TL1'].iloc[i]=TL1
    geo_data['TL2'].iloc[i]=TL2
    geo_data['TL3'].iloc[i]=TL3
    geo_data['TL4'].iloc[i]=TL4
    geo_data['TL5'].iloc[i]=TL5
    geo_data['TL6'].iloc[i]=TL6
    geo_data['TL7'].iloc[i]=TL7
    geo_data['TL8'].iloc[i]=TL8
    geo_data['TL9'].iloc[i]=TL9
    geo_data['TL10'].iloc[i]=TL10
    geo_data['p0'].iloc[i] = p0
    geo_data['p1'].iloc[i] = p1
    geo_data['p2'].iloc[i] = p2
    geo_data['p3'].iloc[i] = p3
    geo_data['p4'].iloc[i] = p4
    geo_data['p5'].iloc[i] = p5
    geo_data['p6'].iloc[i] = p6
    geo_data['p7'].iloc[i] = p7
    geo_data['p8'].iloc[i] = p8
    geo_data['p9'].iloc[i] = p9
    geo_data['p10'].iloc[i] = p10
    geo_data['Tmax'].iloc[i] = Tmax
    geo_data['Tmin'].iloc[i] = Tmin
    geo_data['prec'].iloc[i] = prec
    geo_data['w_sp'].iloc[i] = w[w.date == d0]['w_sp'].values[0]
    geo_data['w_d'].iloc[i] = w[w.date == d0]['w_d'].values[0]
    geo_data['dtm'].iloc[i] = Tmax - Tmin
    geo_data['dtl'].iloc[i] = TH0 - TL1

geo_data.to_csv('geo_weather_data.csv')
print('Done')
