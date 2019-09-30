#!/usr/local/intelpython3/bin/python
import json
import time
import numpy as np
import scipy as sp
import pandas as pd
import datetime as dt
import folium
import branca
from folium import plugins
import geopandas as gpd
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
import seaborn as sns
import geojsoncontour
from sklearn.linear_model import LinearRegression
import pickle
from darksky import forecast
from descartes import PolygonPatch
import pysal as ps
from matplotlib.patches import Polygon as mpl_Polygon
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, Polygon

def runmodel(input_date):
    date = (pd.to_datetime(input_date)).date()
    print(date)
    modelfilename = 'data/lin_model.sav'
    scalerfilename = 'data/lin_scaler.sav'
    lin = pickle.load(open(modelfilename, 'rb'))
    scaler = pickle.load(open(scalerfilename, 'rb'))
    testX = build_input(date)
    testx = testX[['TL1','Tmin','Tmax','d_lm','sqrt_dw','sqrt_dp']]
    X = scaler.transform(testx)
    Y = lin.predict(X)
    l= len(Y)
    for i in range(l):
        if Y[i] < 0:
            Y[i] = 0
    TT = Y.reshape(51,51).transpose()
    xx = np.linspace(min(testX['lon']),max(testX['lon']),51)
    yy = np.linspace(min(testX['lat']),max(testX['lat']),51)

    colors = ['darkgreen','green','yellow','orange','red','darkred']
    vmin = 0
    vmax = 50
    levels = len(colors)
    cfig = plt.contourf(xx, yy, TT, levels, alpha=1.0, colors=colors, linestyles='None', vmin=vmin, vmax=vmax)
    cm = branca.colormap.LinearColormap(colors, vmin=vmin, vmax=vmax,caption='Mosquito Activity Intensity').to_step(levels)    
    geojson = geojsoncontour.contourf_to_geojson(contourf=cfig, min_angle_deg=0.0, ndigits=5, stroke_width=0.5, fill_opacity=1.0)
    geomap = folium.Map(location=[41.89, -87.64], zoom_start=13, tiles="stamenterrain")
    folium.GeoJson(geojson,style_function=lambda x: {'color': x['properties']['stroke'],'weight': x['properties']['stroke-width'],'fillColor': x['properties']['fill'],'opacity': 1.0}).add_to(geomap)
    geomap.add_child(cm)
    plugins.Fullscreen(position='topright', force_separate_button=True).add_to(geomap)
    fname = 'static/'+str(dt.datetime.now())+'.html'
    geomap.save(f'flaskapp/'+fname)
    return fname

def get_weather(input_date):
    date = (pd.to_datetime(input_date)).date()
    print(date)
    dskey = '6864d54f724e54e7c3ae08094f523ff0'
    CHICAGO = dskey, 41.95, -87.80
    deltaT = (date - dt.date.today()).days
    prec = 0.0
    Tmax = 0.0
    Tmin = 100.0
    TH0 = 0.0
    TL1 = 0.0
    if deltaT > 0:
        fore_cast = forecast(*CHICAGO)
        TH0 = fore_cast.daily[deltaT].temperatureHigh
        TL1 = fore_cast.daily[deltaT-1].temperatureLow
        for i in range(deltaT):
            Tmax = max([fore_cast.daily[i].temperatureHigh, Tmax])
            Tmin = min([fore_cast.daily[i].temperatureLow, Tmin])
            prec += fore_cast.daily[i].precipIntensityMax
    elif deltaT == 0:
        fore_cast = forecast(*CHICAGO)
        TH0 = fore_cast.daily[deltaT].temperatureHigh
        Tmax = TH0
        Tmin = fore_cast.daily[deltaT].temperatureLow

    N = 10 - deltaT
    if N > 10:
        N = 10
    for i in range(N):
        bt = (dt.date.today() + pd.DateOffset(deltaT - i)).isoformat()
        backDay = forecast(*CHICAGO, time = bt)
        if deltaT <= 0:
            if i == 0:
                TH0 = backDay.daily[0].temperatureHigh
            elif i == 1:
                TL1 = backDay.daily[0].temperatureLow
        Tmax = max([Tmax,backDay.daily[0].temperatureHigh])
        Tmin = min([Tmin,backDay.daily[0].temperatureLow])
        prec += backDay.daily[0].precipIntensityMax
    A={}
    A['TH0']= TH0
    A['TL1']= TL1
    A['Tmax']= Tmax
    A['Tmin']= Tmin
    A['prec']= prec
    return A

def build_input(input_date):
    date = (pd.to_datetime(input_date)).date()
    print(date)
    A = get_weather(date)
    GD = pd.read_csv('data/gridlake.csv')
    GD['sqrt_dw']=np.sqrt(GD['d_water'])
    GD['sqrt_dp']=np.sqrt(GD['d_park'])
    GD['TH0'] = A['TH0']
    GD['TL1'] = A['TL1']
    GD['Tmax'] = A['Tmax']
    GD['Tmin'] = A['Tmin']
    return GD
