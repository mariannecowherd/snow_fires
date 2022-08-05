## imports
import json
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
import os
import pandas as pd
import pickle
import geopandas as gpd
from locale import atof, setlocale, LC_NUMERIC
from pyproj import crs
import sys
import contextily as cx

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


### directories
homedir = '/home/marianne/Documents/snow_fires/'
rawdatadir = '/home/marianne/Documents/data/'
datadir = homedir + 'data/'


os.chdir(homedir)


wgs_crs = crs.CRS('epsg:4326')
use_crs = wgs_crs

## load fire data
rawdatadir = '/home/marianne/data/'
datadir = '/home/marianne/Documents/snow_fires/data/'

gages_metadata = gpd.read_file(rawdatadir + 'snow_fires_data/gages_metadata.gdf').to_crs(wgs_crs)
fires_allyears = gpd.read_file(rawdatadir + 'snow_fires_data/fires_allyears.gdf').to_crs(wgs_crs)
gaged_basins_gdf = gpd.read_file(rawdatadir + 'snow_fires_data/gaged_basins_gdf.gdf').to_crs(wgs_crs)
snowzone = gpd.read_file('/home/marianne/data/snowzone/snowzone.shp').to_crs(wgs_crs)

mtbs = gpd.read_file(rawdatadir + 'mtbs/mtbs_perims_DD.shp')

with open(datadir + 'gaged_basins.pickle', 'rb') as handle:
    gaged_basins = pickle.load(handle)
    
with open(datadir + 'streamflow_metadata.pickle', 'rb') as handle:
    streamflow_metadata = pickle.load(handle)

gaged_fires = gpd.overlay(gaged_basins,mtbs)
snow_in = gpd.overlay(gaged_basins,snowzone)
## good up to here
""""
gages = np.unique(gaged_basins.GAGE_ID)
years = []
props_burned = []
gage_ids = []
burned_areas = []
basin_areas = []
snowy_areas = []
snowy_burned_areas = []
for i in gages:
    prop_burned = []
    fire_year = []
    fires_in = gaged_fires.loc[gaged_fires.GAGE_ID == i]
    snow_in_basin = snow_in.loc[snow_in.GAGE_ID == i]
    snowy_areas.append(np.nansum(snow_in_basin.to_crs('epsg:5070').area))
    yrs = np.unique(fires_in.FIRE_YEAR_)
    yrs = yrs[~np.isnan(yrs)]
    basin_area = np.nansum(gaged_basins.loc[gaged_basins.GAGE_ID==i].to_crs('epsg:5070').area)
    burned_areas_all = []
    snowy_yr = []
    for y in yrs:
        fires_tmp = fires_in[fires_in.FIRE_YEAR_ == y]
        burned_area = np.sum(fires_tmp.to_crs('epsg:5070').area)
        prop_burned.append(burned_area/basin_area)
        burned_areas_all.append(burned_area)
        snow_in_burn = gpd.overlay(fires_tmp,snow_in_basin)
        snowy_yr.append(np.nansum(snow_in_burn.to_crs('epsg:5070').area))
    years.append(yrs)
    props_burned.append(prop_burned)
    gage_ids.append(i)
    burned_areas.append(burned_areas_all)
    basin_areas.append(basin_area)
    snowy_burned_areas.append(snowy_yr)


burn_snow_history_all = pd.DataFrame({
            'year':years,
            'burned_area': burned_areas ,
            'basin_area':basin_areas,
            'burned_prop':props_burned,
            'gage_id':gage_ids,
            'snowy_area':snowy_areas,
            'snowy_burned_area': snowy_burned_areas
        })


burn_snow_history_all['snowy_prop'] = burn_snow_history_all.snowy_area/burn_snow_history_all.basin_area

sba_props = []
sba_xsprops = []
for j in range(len(burn_snow_history_all)):
    entry = burn_snow_history_all.loc[j]
    sba_prop = []
    sba_xs = []
    for i in range(len(entry.year)):
        batmp = entry.burned_area[i]
        sbatmp = entry.snowy_burned_area[i]
        sbaproptmp = sbatmp/batmp
        sba_prop.append(sbaproptmp)
        sba_xs.append(sbaproptmp - entry.snowy_prop)
    sba_props.append(sba_prop)
    sba_xsprops.append(sba_xs)

burn_snow_history_all['burned_snow_xs'] = sba_xsprops
burn_snow_history_all['snow_burned_prop'] = sba_props


with open(datadir + 'burn_snow_history_all.pickle', 'wb') as handle:
    pickle.dump(burn_snow_history_all, handle,protocol=pickle.HIGHEST_PROTOCOL)"""

## now just target


fyears = [int(d.split('-')[0]) for d in gaged_fires.Ig_Date]
gaged_fires['Fire_Year'] = fyears
gages = np.unique(gaged_basins.GAGE_ID)
years = []
props_burned = []
gage_ids = []
burned_areas = []
basin_areas = []
snowy_areas = []
snowy_burned_areas = []
fire_years = []
errs = []
erryrs=[]
sba_props = []
sba_xs_props = []
snow_props = []
nanids = []
goodids = []
for i in gages:
    match_year = (streamflow_metadata.loc[streamflow_metadata.Gauge_ID==i].Fire_Year.values[0])
    if np.isnan(match_year):
        nanids.append(i)
        continue
        '''years.append(np.nan)
        props_burned.append(np.nan)
        gage_ids.append(np.nan)
        burned_areas.append(np.nan)
        basin_areas.append(np.nan)
        
        snowy_areas.append(np.nan)
        snowy_burned_areas.append(np.nan)
        fire_years.append(np.nan)'''
    else:
        try:
            snow_in_basin = snow_in.loc[snow_in.GAGE_ID == i]
            basin_area = np.nansum(gaged_basins.loc[gaged_basins.GAGE_ID==i].to_crs('epsg:5070').area)
            fires_in = gaged_fires.loc[gaged_fires.GAGE_ID == i]
            fires_tmp = fires_in[fires_in.Fire_Year == match_year]
            burned_area = np.sum(fires_tmp.to_crs('epsg:5070').area)
            snow_in_burn = gpd.overlay(fires_tmp,snow_in_basin)
            snow_burned_area = np.nansum(snow_in_burn.to_crs('epsg:5070').area)
            snow_area = np.nansum(snow_in_basin.to_crs('epsg:5070').area)
            snow_prop = snow_area / basin_area
            prop_burned = (burned_area/basin_area)
            burned_areas_all = (burned_area)
            sba_prop = snow_burned_area / burned_area

            sba_xs = (sba_prop - snow_prop)
            # add
            snowy_areas.append(snow_area)
            snowy_burned_areas.append(snow_burned_area)
            props_burned.append(prop_burned)
            gage_ids.append(i)
            burned_areas.append(burned_areas_all)
            basin_areas.append(basin_area)
            fire_years.append(match_year)
            sba_xs_props.append(sba_xs)
            sba_props.append(sba_prop)
            snow_props.append(snow_prop)

            goodids.append(i)
        except:
            erryrs.append(match_year)
            errs.append(i)
            continue

burn_snow_history_target = pd.DataFrame({
            'gage_id':gage_ids,
            'year':fire_years,
            'burned_area': burned_areas ,
            'basin_area':basin_areas,
            'burned_prop':props_burned,
            'snowy_area':snowy_areas,
            'snowy_burned_area': snowy_burned_areas,
            'snowy_prop': snow_props,
            'sba_xs_prop': sba_xs_props,
            'sba_prop':sba_props
        })

with open(datadir + 'burn_snow_history_target.pickle', 'wb') as handle:
    pickle.dump(burn_snow_history_target, handle,protocol=pickle.HIGHEST_PROTOCOL)
