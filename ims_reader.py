# Interfaces to read the data of IMS from the website
import numpy as np
import pandas as pd
import pickle

# index to subset data for the 1-km grid
min_ind_lons = 11000
max_ind_lons = 19000
min_ind_lats = 9000
max_ind_lats = 17000


def read_lats_1km(path, filename='IMS1kmLats.24576x24576x1.double'):
  nx = 24576
  ny = 24576
  with open(path + filename, 'rb') as f:
    data = np.fromfile(f, dtype='<d', count=nx * ny)
    lats = np.reshape(data, [nx, ny], order='F')
  return(lats[min_ind_lats:max_ind_lats, min_ind_lons:max_ind_lons])


def read_lons_1km(path, filename='IMS1kmLons.24576x24576x1.double'):
  nx = 24576
  ny = 24576
  with open(path + filename, 'rb') as f:
    data = np.fromfile(f, dtype='<d', count=nx * ny)
    lons = np.reshape(data, [nx, ny], order='F')
  return(lons[min_ind_lats:max_ind_lats, min_ind_lons:max_ind_lons] + 90.)


def read_coordinates_1km_compressed(path):
  lons = pickle.load( open( path+"lon_1km.pickle", "rb" ) )
  lats = pickle.load( open( path+"lat_1km.pickle", "rb" ) )
  return lons, lats


def read_lats_4km(path, filename='imslat_4km.bin'):
  nx = 6144
  ny = 6144
  with open(path + filename, 'rb') as f:
    data = np.fromfile(f, dtype='<f', count=nx * ny)
    lats = np.reshape(data, [nx, ny], order='F')
  return(lats)


def read_lons_4km(path, filename='imslon_4km.bin'):
  nx = 6144
  ny = 6144
  with open(path + filename, 'rb') as f:
    data = np.fromfile(f, dtype='<f', count=nx * ny)
    lons = np.reshape(data, [nx, ny], order='F')
  return(lons + 90.)


def read_data_1km(year=2017, doy=300):
  nx = 24576
  url = ("ftp://sidads.colorado.edu/pub/DATASETS/NOAA/G02156/1km/%s/ims%s%s_1km_v1.3.asc.gz" %
         (year, year, doy))
  widths = np.full((nx), 1, dtype=int).tolist()
  data = pd.read_fwf(url, skiprows=30, widths=widths,
                              lineterminator='\n', header=None, compression='gzip').values
  return(data[min_ind_lats:max_ind_lats, min_ind_lons:max_ind_lons])


def read_data_1km_compressed(filename):
  nx = 8000
  widths = np.full((nx), 1, dtype=int).tolist()
  data = pd.read_fwf(filename, widths=widths, lineterminator='\n', header=None).values
  return(data)


def read_data_4km(year=2017, doy=300):
  nx = 6144
#   url = ("ftp://sidads.colorado.edu/pub/DATASETS/NOAA/G02156/4km/%s/ims%s%s_4km_v1.3.asc.gz" %
#          (year, year, doy))
  url = ("https://usicecenter.gov/File/DownloadProduct?products=/ims/ims_v3/snow/6144asc/%s&fName=NIC.IMS_v3_%s%s00_4km.asc.gz" %
         (year, year, doy))
  widths = np.full((nx), 1, dtype=int).tolist()
  data = pd.read_fwf(url, skiprows=30, widths=widths,
                              lineterminator='\n', header=None, compression='gzip').values
  return(data)
