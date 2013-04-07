from django.contrib.gis.measure import Distance
from django.contrib.gis import geos
from trailguide.models.dem import Dem
import math

def distance_array(proj_point_array):
    """Find the distance between points in a projected point array"""
    def calc_dist(index, end_point):
        if index == 0:
            start_point = end_point
        else:
            start_point = proj_point_array[index - 1]
        return distance_between_points(start_point, end_point)

    return [calc_dist(index, point) for index, point in enumerate(proj_point_array)]

def distance_between_points(first_point, second_point):
    """Find the linear distance between two points"""
    dx = first_point.x - second_point.x
    dy = first_point.y - second_point.y
    return Distance(m=math.sqrt(dx**2 + dy**2))

def densified_line(proj_point_array, threshold):
    """Add points to the line such that the distance between any two points is < threshold"""
    distances = distance_array(proj_point_array)
    densified = []

    def gen_new_point(start_point, dx, dy):
        coords = (start_point.x + dx.m, start_point.y + dy.m)
        pnt = geos.Point(coords)
        densified.append(pnt)
        return pnt

    for index, end_point in enumerate(proj_point_array):
        if index == 0: densified.append(end_point)
        else:
            if distances[index] > threshold: # Is distance from previous point > threshold?
                number_of_segments = int(math.ceil( distances[index] / threshold ))
                start_point = proj_point_array[index - 1]

                dx = Distance(m=(end_point.x - start_point.x) / number_of_segments)
                dy = Distance(m=(end_point.y - start_point.y) / number_of_segments)

                new_point = gen_new_point(start_point, dx, dy)

                for i in range(number_of_segments):
                    new_point = gen_new_point(new_point, dx, dy)

            # Have appended any required new points, slap in the end point
            densified.append(end_point)

    return densified

def elevations_along_line(proj_point_array, dem=Dem()):
    """Return the elevations at each of a set of projected points"""
    return [dem.read_value(pnt) for pnt in proj_point_array]