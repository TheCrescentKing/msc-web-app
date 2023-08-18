import pathlib
import hvplot.xarray
import holoviews as hv
from bokeh.resources import CDN
from bokeh.embed import file_html
from modules.ortho_correct import mineralOrthoCorrect


def mineralMap(fileName, mineralGroup = 1):
	data_dir = pathlib.Path().resolve() / "data" / fileName
	orthoArray = mineralOrthoCorrect(data_dir, mineralGroup)
	# plot = orthoArray.hvplot.contour(cmap='jet', aspect = 'equal', frame_width=500, rasterize=False)
	plot = orthoArray.hvplot.contour(cmap='jet', aspect = 'equal', frame_width=500, geo=True, tiles='EsriImagery', rasterize=False)
	return file_html(hv.render(plot), CDN, 'mineral-map')