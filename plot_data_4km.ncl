;*************************************************
; NCL Graphics: nic_1.ncl
;
; Concepts illustrated:
;    - Plotting ice data
;    - Reading data from binary files
;    - Reading data from an ASCII file with headers
;    - Changing the labelbar labels
;    - Plotting categorical data
;
; This example shows how to plot data from the NIC (National Ice Center);
; specifically the 24 km IMS (Interactive Multisensor Snow and Ice Mapping System)
; Daily Northern Hemisphere Snow and Ice Analysis. The data in ascii format 
; is available from ftp://sidads.colorado.edu/pub/DATASETS/NOAA/G02156/24km. The
; lat/lon grids are in binary and may be found at 
; ftp://sidads.colorado.edu/pub/DATASETS/NOAA/G02156/metadata.
; The data are mapped into a polar stereographic projection centered at 90 degrees North,
; with a center longitude of 80 West. 
;
; According to the description of the data grid at 
; http://nsidc.org/data/docs/noaa/g02156_ims_snow_ice_analysis
; use of this data should be acknowledged and cited as follows:
;
; National Ice Center. 2008, updated daily. 
; IMS daily Northern Hemisphere snow and ice analysis at 4 km and 24 km resolution. 
; Boulder, CO: National Snow and Ice Data Center. Digital media.
;
; See comments interspersed with  the code for additional detail concerning 
; the techniques used to plot these data.
;
;*************************************************
;
; These files are loaded by default in NCL V6.2.0 and newer
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_code.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/gsn_csm.ncl"
; load "$NCARG_ROOT/lib/ncarg/nclscripts/csm/contributed.ncl"

begin
  nrows = 6144
  ncols = 6144
;
; The lat/lon values are in binary format with the areas outside the projected space set to 
; the IEEE NaN (Not a Number) value. Since the graphics routines do not work well with NaN
; values, change them to the default fillvalue for the type of the data, which is float.
;

  setfileoption("bin","ReadByteOrder","LittleEndian")

  lat  = cbinread("imslat_4km.bin", (/nrows,ncols/), "float")
  lon  = cbinread("imslon_4km.bin", (/nrows,ncols/), "float")

  msg = default_fillvalue("float")
  lat = where(isnan_ieee(lat),msg,lat)
  lon = where(isnan_ieee(lon),msg,lon)

  lat@_FillValue = msg
  lon@_FillValue = msg

; The data file contains categorical data with values 0 - 5 where  each line represents a row of the the grid
; There is no delimiter between the data values which are all single digits. The value 0 represents areas
; outside the circular limits of the projection. To get this into a usable form in NCL read the data as
; strings and then use the function str_split_by_length to break the line length strings into strings of 1
; character each. Then convert to float.
;
fils = systemfunc ("ls *.asc") ; file paths

  nhead   = 30

  fili    = fils(0)

; wrkc_2d will be nrows (1024 x 1)
; It is necessary to subscript the array to get rid of the right hand single element dimension
;
  wrkc_2d = readAsciiTable(fili, 1, "string", nhead )
  data = tofloat(str_split_by_length(wrkc_2d(:,0),1))
;
; Designate the value 0 as the fill value, but then change all the fill values to the default float
; fill value in order to satisfy the contouring code which does not accept 0 as a fill value.
;
  data@_FillValue = 0
  data@_FillValue = msg
  data@lat2d=lat 
  data@lon2d=lon(:,::-1) - 180
;
; Print some statistics about the data
;
  ; print("Total number of points    = " + product(dimsizes(data)))
  ; print("num(ismissing(data))      = " + num(ismissing(data)))
  ; print("num(.not.ismissing(data)) = " + num(.not.ismissing(data)))  
  ; print("num(ismissing(lat))       = " + num(ismissing(lat)))
  ; print("num(.not.ismissing(lat))  = " + num(.not.ismissing(lat)))
  ; print("num(ismissing(lon))       = " + num(ismissing(lon)))
  ; print("num(.not.ismissing(lon))  = " + num(.not.ismissing(lon)))
  ; print("min/max data = " + min(data) + " / " + max(data))
  ; print("min/max lat  = " + min(lat) + " / " + max(lat))
  ; print("min/max lon  = " + min(lon) + " / " + max(lon))

;
; Plotting code

;
; Use triangular mesh gridding. It is much faster, but even more important it
; produces a plot that is correct. The standard "curvilinear" and "spherical" 
; methods have trouble with grids defined like this one.
;
  res = True
  res@cnFillOn = True
;  res@cnFillPalette = "default"           ; set color map
  res@cnLinesOn = False
  res@cnLineLabelsOn = False
  res@cnFillMode = "rasterfill"
  res@cnMissingValFillColor = "gray"
;
; Since the data is categorical, values between the categories need to be
; excluded. Use Explicit level selection to accomplish this. 
;
  res@cnLevelSelectionMode = "explicitlevels"
  res@cnLevels = (/ 0.99,1.99, 2.99, 3.99, 4.99 /)
  res@cnFillBackgroundColor = "gray"
  res@cnFillColors = (/"transparent", "blue", "darkgreen", "cyan", "white"/)
  res@lbLabelAlignment = "boxcenters"
  res@lbLabelStrings = (/ "water", "land", "ice", "snow" /)
  res@cnExplicitLabelBarLabelsOn = True
  res@cnLabelBarEndStyle = "excludeouterboxes"
  res@lbAutoManage = False
  res@lbLabelFontHeightF = 0.01
  res@pmLabelBarHeightF = 0.02
;
; extract the components of the date which is embedded in the file name in yyyyddd format
;

  string_name=str_split_by_length(fils, (/3,7,13/))
  date = tostring(yyyyddd_to_yyyymmdd(tointeger(string_name(1))))
  res@gsnCenterString = date
  res@gsnCenterStringFontHeightF = 0.02
  res@gsnMaximize = True
;
; delete(data@_FillValue)
;
  res@trGridType = "triangularmesh"
  res@tfDoNDCOverlay = False

  ; res@mpProjection = "orthographic"
  ; res@mpGridAndLimbOn = True
  ; res@mpGridLineDashPattern = 2
  ; res@mpCenterLatF = 90
  ; res@mpCenterLonF = -40

  res@mpProjection = "LambertConformal"
  res@mpLambertParallel1F = 33.0         ; two parallels
  res@mpLambertParallel2F = 45.0
  res@mpLambertMeridianF  = 10        ; central meridian
  res@mpLimitMode         = "LatLon"
  res@mpMaxLonF    = 50                      ; specify the plot domain
  res@mpMinLonF    = -23.5                      ;
  res@mpMinLatF    = 29.5                     ;
  res@mpMaxLatF    = 70.5                    ;
  res@mpOutlineBoundarySets = "AllBoundaries"
  res@mpDataSetName       = "Earth..3"
  res@mpOutlineOn = True 

    wks = gsn_open_wks("png","nic_ims_eur_"+date)     ; send graphics to PNG file


  plot = gsn_csm_contour_map(wks,data,res)
end
