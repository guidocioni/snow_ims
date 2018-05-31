from mpl_toolkits.basemap import Basemap # Import the Basemap toolkit
import numpy as np

def get_projection(projection="eurasia"):
	if projection=="nh":
		bmap = Basemap(projection="npstere", lon_0=20, lat_0=90, boundinglat=30,\
               rsphere=6378160.0, ellps="WGS84",k_0=0.9330127018922193)
		bmap.drawcoastlines(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawcountries(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawparallels(np.arange(-80.,81.,30),linewidth=0.2,labels=[True, False, False, True])
		bmap.drawmeridians(np.arange(-180.,181.,30),linewidth=0.2,labels=[True, False, False, True])
	elif projection=="eurasia":
		bmap = Basemap(projection="stere", lon_0=20, lat_0=55, boundinglat=0,\
                rsphere=6378160.0, ellps="WGS84",k_0=0.9330127018922193,\
                width=6000000,height=4000000, resolution='i')
		bmap.drawcoastlines(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawcountries(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawparallels(np.arange(-80.,81.,10.),linewidth=0.2,labels=[True, False, False, True])
		bmap.drawmeridians(np.arange(-180.,181.,10.),linewidth=0.2,labels=[True, False, False, True])
	elif projection=="west_europe":
		bmap = Basemap(projection="stere", lon_0=10, lat_0=45, boundinglat=0,\
                rsphere=6378160.0, ellps="WGS84",k_0=0.9330127018922193,\
                width=3000000,height=2000000, resolution='i')
		bmap.drawcoastlines(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawcountries(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawparallels(np.arange(-80.,81.,5.),linewidth=0.2,labels=[True, False, False, True])
		bmap.drawmeridians(np.arange(-180.,181.,5.),linewidth=0.2,labels=[True, False, False, True])
	elif projection=="italy":
		bmap = Basemap(projection="stere", lon_0=12, lat_0=43, boundinglat=0,\
                rsphere=6378160.0, ellps="WGS84",k_0=0.9330127018922193,\
                width=1500000,height=1500000, resolution='h')
		bmap.drawcoastlines(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawcountries(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawparallels(np.arange(-80.,81.,2.5),linewidth=0.2,labels=[True, False, False, True])
		bmap.drawmeridians(np.arange(-180.,181.,2.5),linewidth=0.2,labels=[True, False, False, True])
		bmap.readshapefile('/home/mpim/m300382/shapefiles/ITA_adm_shp/ITA_adm1','ITA_adm1',linewidth=0.3,color='black')
	elif projection=="alps":
		bmap = Basemap(projection="stere", lon_0=10.5, lat_0=45.8, boundinglat=0,\
                rsphere=6378160.0, ellps="WGS84",k_0=0.9330127018922193,\
                width=900000,height=500000, resolution='h')
		bmap.drawcoastlines(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawcountries(linewidth=0.5, linestyle='solid', color='black')
		bmap.drawparallels(np.arange(-80.,81.,2.5),linewidth=0.2,labels=[True, False, False, True])
		bmap.drawmeridians(np.arange(-180.,181.,2.5),linewidth=0.2,labels=[True, False, False, True])
		bmap.readshapefile('/home/mpim/m300382/shapefiles/ITA_adm_shp/ITA_adm1','ITA_adm1',linewidth=0.3,color='black')
	else:
		raise ValueError('Projection should be nh, eurasia, west_europe, italy or alps')
	return(bmap)
