## for the snow fires project
## data file import and reproject
## marianne cowherd
import os, glob
import geopandas as gpd
from pyproj import crs
import pickle
from constants import *


rawdatadir = '~/Documents/data/'
wgs_crs = crs.CRS('epsg:4326')

## load fire data
# wfigs 2021 fires perimeters
wfigs21 = gpd.read_file(rawdatadir + 'InteragencyPerimeters2021/FH_Perimeter.shp').to_crs(wgs_crs)
# interagency historic record fire preimeters
fires_allyears = gpd.read_file(rawdatadir + 'Interagency_Fire_Perimeter_History/InteragencyFirePerimeterHistory.shp').to_crs(wgs_crs)

gages_metadata = gpd.read_file(rawdatadir + 'snow_fires_data/gages_metadata.gdf').to_crs(wgs_crs)
fires_allyears = gpd.read_file(rawdatadir + 'snow_fires_data/fires_allyears.gdf').to_crs(wgs_crs)
bas_all = gpd.read_file(rawdatadir + 'snow_fires_data/bas_all.gdf').to_crs(wgs_crs)
gaged_basins_gdf = gpd.read_file(rawdatadir + 'snow_fires_data/gaged_basins_gdf.gdf').to_crs(wgs_crs)
snowzone = gpd.read_file(rawdatadir + 'snowzone/snowzone.shp').to_crs(wgs_crs)

with open(datadir + 'gaged_basins.pickle', 'rb') as handle:
    gaged_basins = pickle.load(handle)
    
with open(datadir + 'streamflow_metadata.pickle', 'rb') as handle:
    streamflow_metadata = pickle.load(handle)
    
with open(datadir + 'target_basins.pickle', 'rb') as handle:
    target_basins = pickle.load(handle)