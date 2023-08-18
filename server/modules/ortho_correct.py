import xarray as xr
import numpy as np

GLT_NODATA_VALUE=0

def mineralOrthoCorrect(filePath, mineralGroup = 1):
	minGroupColumnName = "group_" + str(mineralGroup) + "_mineral_id"
	minerals = xr.open_dataset(filePath)
	# mineral_metadata = xr.open_dataset(filePath,group='mineral_metadata')
	location = xr.open_dataset(filePath, group='location')
	glt_array = np.nan_to_num(np.stack([location['glt_x'].data,location['glt_y'].data],axis=-1),nan=GLT_NODATA_VALUE).astype(int)
	ds_array = minerals[minGroupColumnName].data

	# Build Output Dataset
	fill_value = 0
	out_ds = np.zeros((glt_array.shape[0], glt_array.shape[1]), dtype=np.float32) + fill_value
	valid_glt = np.all(glt_array != GLT_NODATA_VALUE, axis=-1)
	# Adjust for One based Index
	glt_array[valid_glt] -= 1 
	# Use indexing/broadcasting to populate array cells with 0 values
	out_ds[valid_glt] = ds_array[glt_array[valid_glt, 1], glt_array[valid_glt, 0]]
	
	GT = minerals.geotransform
	# Create Array for Lat and Lon and fill
	dim_x = location.glt_x.shape[1]
	dim_y = location.glt_x.shape[0]
	lon = np.zeros(dim_x)
	lat = np.zeros(dim_y)
	
	for x in np.arange(dim_x):
		x_geo = GT[0] + x * GT[1]
		lon[x] = x_geo
	for y in np.arange(dim_y):
		y_geo = GT[3] + y * GT[5]
		lat[y] = y_geo
	
	coords = {'lat':(['lat'],lat), 'lon':(['lon'],lon)}
	data_vars = {minGroupColumnName:(['lat','lon'], out_ds)}

	out_xr = xr.Dataset(data_vars=data_vars, coords=coords, attrs= minerals.attrs)
	out_xr[minGroupColumnName].attrs = minerals[minGroupColumnName].attrs
	out_xr.coords['lat'].attrs = location['lat'].attrs
	out_xr.coords['lon'].attrs = location['lon'].attrs
	out_xr.rio.write_crs(minerals.spatial_ref,inplace=True) # Add CRS in easily recognizable format	

	return out_xr