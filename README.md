# snow_ims
Shows how to download and process IMS Snow Cover data with Python. 

![](http://guidocioni.altervista.org/snow/archive/ims_nh_example.png)

The main script is `download_plot_data.run`, which calls the Python script `plot_data.py` where the data is read and some plots produced on different projections. These are defined for convenience in `map_projection_ims.py`

The main utilities to read the data are contained in `ims_reader.py`. Please note the following. 
- Coordinates for 4 km resolution data (`imslon_4km.bin` and `imslat_4km.bin`) are already downloaded and placed in the same folder to avoid having to read from the (slow) server every time 
- The 4 km daily data is read directly from the server using pandas as it is not too big: we can avoid having to download and process it beforehand. 
- Coordinates for the 1 km resolution data are already downloaded and saved as `pickle` for the same reason. Furthermore they are already subsetted on the Eurasian continent (see image below) as the original files are too big to be saved (8 GB in total!) ![Subset area](http://guidocioni.altervista.org/snow/archive/ims_subset.png)
- The 1 km daily data is downloaded and processed BEFORE launching the Python script in `download_plot_data.run` so as to avoid having to load it into Python, thus saving memory and CPU. We do in a quite clever way using only `sed` and `cut`: `sed -ne '9031,17030p' ims_file.asc | cut -c11001-19000 > ims_file_subsetted_1km.asc`. If you find an easier way...do let me know! 

