from osgeo import gdal
from gdalconst import GA_ReadOnly
from django.conf import settings
from django.contrib.gis.measure import Distance
from django.contrib.gis.gdal import SpatialReference
import math

class Dem(object):
    """Representation of a DEM of the area"""
    def __init__(self, path_to_dem=settings.DEM_FILE_LOCATION):
        """Open the DEM using GDAL"""
        self.raster = gdal.Open(path_to_dem, GA_ReadOnly)
        self.band = self.raster.GetRasterBand(1)
        transform = self.raster.GetGeoTransform()
        self.xOrigin = transform[0]
        self.yOrigin = transform[3]
        self.pixelWidth = transform[1]
        self.pixelHeight = transform[5]
        self.projection = SpatialReference(self.raster.GetProjection())
        self.pixel_distance = Distance(**{ self.projection.linear_name: self.pixelWidth })

    def read_value(self, point):
        """Read the value of the raster at a particular point"""
        xOffset = int((point.x - self.xOrigin) / self.pixelWidth)
        yOffset = int((point.y - self.yOrigin) / self.pixelHeight)
        data = self.band.ReadAsArray(xOffset, yOffset, 1, 1)
        return data[0,0]