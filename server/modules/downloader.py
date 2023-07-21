from modules.cmr_api import GranuleDownload


REFL_DOI="10.5067/EMIT/EMITL2ARFL.001"
MIN_DOI="10.5067/EMIT/EMITL2BMIN.001"

def findReflectanceFiles(lat, lon, start_date, end_date = ""):
    granuleDownloader = GranuleDownload(doi=MIN_DOI)
    return granuleDownloader.searchByPoint(lon, lat, start_date, end_date)

def getAll():
    granuleDownloader = GranuleDownload(doi=MIN_DOI)
    return granuleDownloader.getAll()