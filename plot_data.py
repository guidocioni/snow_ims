import numpy as np
import pandas as pd
from mpl_toolkits.basemap import Basemap # Import the Basemap toolkit
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import datetime
import ims_reader
import map_projections_ims

def save_figure(folder, area, lon_to_plot, lat_to_plot, data_to_plot):
	bmap=map_projections_ims.get_projection(area)
	x,y=bmap(lon_to_plot, lat_to_plot)
	bmap.contourf(x, y, data_to_plot, levels=np.array([0,1,2,3,4,5]),\
 			 colors=('blue', 'darkgreen','cyan','white'), extend='min')
	cbar=bmap.colorbar(location='right')
	cbar.set_ticklabels(['Ocean','Land','Ice','Snow'])
	cbar.ax.set_xticklabels(['Water','Land','Ice','Snow'])
	plt.title(datetime.datetime.strptime(str(year)+str(doy),"%Y%j").strftime("%Y-%m-%d")+' - IMS 1km data - elaborated by www.guidocioni.it')

	DPI = 150
	plt.savefig(folder+"ims_"+area+"_"+datetime.datetime.strptime(str(year)+str(doy),"%Y%j").strftime("%Y%m%d")+".png"\
		, dpi=DPI, bbox_inches='tight')
	plt.close()

year=datetime.datetime.now().timetuple().tm_year
doy=datetime.datetime.now().timetuple().tm_yday-1

lon_4km=ims_reader.read_lons_4km(path='/work/mh0731/m300382/snow/')
lat_4km=ims_reader.read_lats_4km(path='/work/mh0731/m300382/snow/')
data_4km=ims_reader.read_data_4km(year=year, doy=doy)

save_figure('/work/mh0731/m300382/snow/', 'nh', lon_4km, lat_4km, data_4km)

lon_1km=ims_reader.read_lons_1km(path='/work/mh0731/m300382/snow/')
lat_1km=ims_reader.read_lats_1km(path='/work/mh0731/m300382/snow/')
data_1km=ims_reader.read_data_1km(year=year, doy=doy)

save_figure('/work/mh0731/m300382/snow/', 'eurasia', lon_1km, lat_1km, data_1km)
save_figure('/work/mh0731/m300382/snow/', 'italy', lon_1km, lat_1km, data_1km)
save_figure('/work/mh0731/m300382/snow/', 'alps', lon_1km, lat_1km, data_1km)