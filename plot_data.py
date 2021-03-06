import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from datetime import datetime
import ims_reader
import map_projections_ims
from matplotlib.offsetbox import AnchoredText, AnnotationBbox, OffsetImage
import os
from matplotlib.image import imread as read_png


work_folder = str(os.getenv('WORK_FOLDER'))+'/'
coordinate_folder = str(os.getenv('HOME_FOLDER'))+'/'
DPI = 150
# Define Color Map with discrete colors 
cmap = matplotlib.colors.ListedColormap(["#144682", "#648214", "#82aac8", "#f0f0f0"])
bounds = [0, 1, 2, 3, 4]
norm = matplotlib.colors.BoundaryNorm(bounds, cmap.N)

if os.getenv('doy'):
    doy = str(os.getenv('doy'))
else:
    doy = datetime.now().strftime('%j')
if os.getenv('year'):
    year = str(os.getenv('year'))
else:
    year = datetime.now().strftime('%Y')

date_plot = datetime.strptime(year+doy, '%Y%j')


def add_logo_on_map(ax, logo='/home/ekman/guido/icon_forecasts/plotting/meteoindiretta_logo.png', zoom=0.15, pos=(0.94, 0.08)):
    '''Add a logo on the map given a pnd image, a zoom and a position
    relative to the axis ax.'''
    img_logo = OffsetImage(read_png(logo), zoom=zoom)
    logo_ann = AnnotationBbox(
        img_logo, pos, xycoords='axes fraction', frameon=False)
    logo_ann.set_zorder(10)
    at = ax.add_artist(logo_ann)
    return at


def annotation(ax, text, loc='upper right',fontsize=8):
    """Put a general annotation in the plot."""
    at = AnchoredText('%s'% text, prop=dict(size=fontsize), frameon=True, loc=loc)
    at.patch.set_boxstyle("round,pad=0.,rounding_size=0.1")
    at.zorder = 10
    ax.add_artist(at)
    return(at)


def save_figure(folder, area, lon_to_plot, lat_to_plot, data_to_plot):
    fig = plt.figure(figsize=(15, 15))

    bmap = map_projections_ims.get_projection(area)
    x, y = bmap(lon_to_plot, lat_to_plot)

    bmap.contourf(x, y, data_to_plot, levels = bounds, cmap = cmap)

    # we don't really need a colorbar taking parts of the screen 
    # ax2 = fig.add_axes([0.3, 0.18, 0.4, 0.03])
    # cb2 = matplotlib.colorbar.ColorbarBase(ax2, cmap=cmap,
    #                                 norm=norm,
    #                                 boundaries=bounds,
    #                                 ticks=[0.5, 1.5, 2.5, 3.5, 4.5],
    #                                 spacing='proportional',
    #                                 orientation='horizontal')
    # cb2.set_ticklabels(['Ocean', 'Land', 'Ice', 'Snow'])
    # cb2.ax.tick_params(size=0)

    annotation(plt.gca(), 'Data of '+date_plot.strftime("%Y-%m-%d"), 'upper right', '10')
    annotation(plt.gca(), 'IMS 1km data - NSIDC. Snow=white, Sea ice=light blue', 'upper left', '10')
    add_logo_on_map(plt.gca())

    #plt.savefig(folder + "ims_" + area + "_" + date_plot.strftime("%Y%m%d") + ".png", dpi=DPI, bbox_inches='tight')
    plt.savefig(folder + "ims_" + area + "_latest.png", dpi=DPI, bbox_inches='tight')
    plt.close()


lon_4km = ims_reader.read_lons_4km(path=coordinate_folder)
lat_4km = ims_reader.read_lats_4km(path=coordinate_folder)
data_4km = ims_reader.read_data_4km(year=year, doy=doy)

save_figure(work_folder, 'nh', lon_4km, lat_4km, data_4km)

lon_1km, lat_1km = ims_reader.read_coordinates_1km_compressed(path=coordinate_folder)
data_1km = ims_reader.read_data_1km_compressed(work_folder+'ims_%s_%s_1km.asc' % (year, doy))

save_figure(work_folder, 'eurasia', lon_1km, lat_1km, data_1km)
save_figure(work_folder, 'italy', lon_1km, lat_1km, data_1km)
save_figure(work_folder, 'alps', lon_1km, lat_1km, data_1km)
