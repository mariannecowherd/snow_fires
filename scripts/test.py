#!/usr/bin/env bash
## process loaded data
from constants import *
import geopandas as gpd
import glob
import pandas as pd
from pyproj import crs

wgs_crs = crs.CRS('epsg:4326')

## run this if starting from scrach, otherwise load in processed files in next cell
#usgs reference basin boundaries
bas_ref = gpd.read_file(datadir + 'boundaries-shapefiles-by-aggeco/bas_ref_all.shp')
#usgs non-reference basin boundaries (entire US, multiple files by region)
bas_nonref_names = glob.glob(datadir + 'boundaries-shapefiles-by-aggeco/' + '*nonref*.shp')
bas_nonref=gpd.GeoDataFrame()
for f in bas_nonref_names:
    data = gpd.read_file(f)
    bas_nonref = pd.concat([bas_nonref,data])
    # bas_nonref = bas_nonref.append(data)
bas_all = pd.concat([bas_nonref,bas_ref])
# bas_all = bas_nonref.append(bas_ref)
bas_all = bas_all.set_crs(bas_ref.crs)
bas_all = bas_all.to_crs(wgs_crs) # with wgs 84 CRS

with open(datadir + 'streamflowdata/streamflow_metadata.pickle', 'rb') as handle:
    streamflow_metadata = pickle.load(handle)

gages_metadata = gpd.GeoDataFrame()
gages_metadata['geometry'] = [Point(xy) for xy in zip(md.Longitude, md.Latitude)] 
gages_metadata['gage_id'] = [val for val in md.Gauge_ID]
gages_metadata['fire_year'] = [val for val in md.Fire_Year]
gages_metadata = gages_metadata.set_crs(wgs_crs)

# save to files
bas_all.to_file(datadir + 'bas_all.gdf')
print('saved basins')
gages_metadata.to_file(datadir + 'gages_metadata.gdf')
print('saved gages locations and metadata')
fires_allyears.to_file(datadir + 'fires_allyears.gdf')
print('saved all years of fires')

ids = [str(val) for val in bas_all['GAGE_ID']]
gaged_basins = gpd.GeoDataFrame()
for i in range(len(md)):
    g = streamflow_metadata['Gauge_ID'][i]
    data = bas_all.loc[(bas_all['GAGE_ID']==g)]
    if len(data)==0: print('no watershed '+ g )
    gaged_basins = gaged_basins.append(data)
    gaged_basins = pd.concat([gaged_basins, data])

with open(data_dir + 'gaged_basins.pickle', 'wb') as handle:
    pickle.dump(gaged_basins, handle, protocol=pickle.HIGHEST_PROTOCOL)
    
gaged_basins_gdf = gpd.GeoDataFrame(data = gaged_basins[['AREA','PERIMETER','GAGE_ID']],geometry = gaged_basins['geometry'])
gaged_basins_gdf.to_file(datadir + 'gaged_basins_gdf.gdf')
print('saved gaged basins geodataframe')


