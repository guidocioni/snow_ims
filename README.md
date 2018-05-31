# snow_ims
Shows how to download and process IMS Snow Cover data with Python. 

The main script is `download_plot_data.run`, which calls the Python script `plot_data.py`. 

Additional script are provided with different map projections `map_projection_ims.py` and tools to read the IMS data directly from the URL without having to download anything (`ims_reader.py`). Note that one needs to download the coordinate files beforehand since reading directly from the server would require too much time. 

Also note that 1-km data were so big that they needed to be sub-setted before plotting them. 
