## for the snow fires project
## data file import and reproject
## marianne cowherd
import numpy as np
import matplotlib.pyplot as plt
import os, glob
import geopandas as gpd
import rioxarray as rxr
import rasterio
from rasterio.plot import show, adjust_band
from matplotlib import cm
import matplotlib
from scipy import stats
from pyproj import crs
import pickle

homedir = '/global/home/users/cowherd/snow_fires/'
datadir = '/global/scratch/users/cowherd/'

wgs_crs = crs.CRS('epsg:4326')

## load fire data
# wfigs 2021 fires perimeters
wfigs21 = gpd.read_file(datadir + 'InteragencyPerimeters2021/FH_Perimeter.shp').to_crs(wgs_crs)
# interagency historic record fire preimeters
fires_allyears = gpd.read_file(datadir + 'Interagency_Fire_Perimeter_History/InteragencyFirePerimeterHistory.shp').to_crs(wgs_crs)

gages_metadata = gpd.read_file(datadir + 'gages_metadata.gdf').to_crs(wgs_crs)
fires_allyears = gpd.read_file(datadir + 'fires_allyears.gdf').to_crs(wgs_crs)
bas_all = gpd.read_file(datadir + 'bas_all.gdf').to_crs(wgs_crs)
gaged_basins_gdf = gpd.read_file(datadir + 'gaged_basins_gdf.gdf').to_crs(wgs_crs)
snowzone = gpd.read_file(datadir + 'snowzone/snowzone.shp').to_crs(wgs_crs)

with open(datadir + 'streamflowdata/gaged_basins.pickle', 'rb') as handle:
    gaged_basins = pickle.load(handle)
