import requests
import pandas as pd
from datetime import datetime as dt
from shapely.geometry import MultiPolygon, Polygon, box
# from netrc import netrc
# import os

CMR_URI='https://cmr.earthdata.nasa.gov/search/'
DOI_SEARCH=CMR_URI + 'collections.json?doi='

class GranuleDownload:
	def __init__(self, doi, pageSize = 10):
		self.doi = doi
		self.pageSize = pageSize
		self.doiUrl = DOI_SEARCH + doi

	def _getCmrFormattedDateRange(self, start_date, end_date = ""):
		# CMR formatted start and end times
		start_date = self._stringToDate(start_date)
		if (end_date == ""):
			end_date=dt.today()
		else:
			end_date = self._stringToDate(end_date)

		dt_format = '%Y-%m-%dT%H:%M:%SZ'
		return start_date.strftime(dt_format) + ',' + end_date.strftime(dt_format)

	def _stringToDate(self, string):
		day,month,year = map(int, string.split('/'))
		return dt(year, month, day)

	def _loadGranules(self, cmr_param):
		granule_arr = []

		# while True:
		granuleSearch = CMR_URI + 'granules.json'
		response = requests.post(granuleSearch, data=cmr_param)
		granules = response.json()['feed']['entry']

		
		if granules:
			for g in granules:
				granule_urls = ''
				polygon = ''
						
				# read cloud cover
				cloud_cover = g['cloud_cover']
		
				# reading bounding geometries
				if 'polygons' in g:
					polygons= g['polygons']
					multipolygons = []
					for poly in polygons:
						i=iter(poly[0].split (" "))
						ltln = list(map(" ".join,zip(i,i)))
						# multipolygons.append(Polygon([[float(p.split(" ")[0]), float(p.split(" ")[1])] for p in ltln]))
						multipolygons.append([[float(p.split(" ")[1]), float(p.split(" ")[0])] for p in ltln])
					polygon = multipolygons
				
				# Get https URLs to .nc files and exclude .dmrpp files
				granule_urls = [x['href'] for x in g['links'] if 'https' in x['href'] and '.nc' in x['href'] and '.dmrpp' not in x['href']]
				# Add to list
				granule_arr.append([granule_urls, cloud_cover, polygon])

			# cmr_param["page_num"] += 1
			# else: 
			# 	break
		return granule_arr

	def _granuleArrayToDataframe(self, granule_arr):
		cmr_results_df = pd.DataFrame(granule_arr, columns=["asset_url", "cloud_cover", "polygon"])
		# Drop granules with empty geometry - if any exist
		cmr_results_df = cmr_results_df[cmr_results_df['polygon'] != '']
		# Expand so each row contains a single url 
		cmr_results_df = cmr_results_df.explode('asset_url')
		# Name each asset based on filename
		cmr_results_df.insert(0,'name', cmr_results_df.asset_url.str.split('/',n=-1).str.get(-1))
		# Filter results by file name
		cmr_results_df = cmr_results_df[cmr_results_df.name.str.contains('_MIN_')]

		return cmr_results_df

	def getAll(self, page_num = 1):
		concept_id = requests.get(self.doiUrl).json()['feed']['entry'][0]['id']
      
		cmr_param = {
			"collection_concept_id": concept_id,
			"page_num": page_num,
   			"page_size": self.pageSize,
		}
  
		granule_arr = self._loadGranules(cmr_param)	
		granuleDataframe = self._granuleArrayToDataframe(granule_arr)

		return granuleDataframe

	def searchByPoint(self, lon, lat, start_date, end_date, page_num = 1):
     
		point_str = str(lon) +','+ str(lat)
		temporal_str = self._getCmrFormattedDateRange(start_date, end_date)
  
		concept_id = requests.get(self.doiUrl).json()['feed']['entry'][0]['id']
		
		# defining parameters
		cmr_param = {
			"collection_concept_id": concept_id, 
			"page_size": self.pageSize,
			"page_num": page_num,
			"temporal": temporal_str,
			"point":point_str,
			"cloud_cover": "0,10"
		}
	
		granule_arr = self._loadGranules(cmr_param)	
		granuleDataframe = self._granuleArrayToDataframe(granule_arr)

		return granuleDataframe