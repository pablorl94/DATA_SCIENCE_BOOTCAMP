# Importations

import json
import openrouteservice
import pandas as pd
import pyproj
from shapely import geometry
from shapely.geometry import Point, LineString, Polygon, MultiPolygon


# Functions

def extract_coordinates_radius(dataframe, rad_col, lng_col, lat_col):
    radiuses, points_list = [], []

    for i, row in dataframe.iterrows():
        radiuses.append(row[rad_col])
        points_list.append((row[lng_col], row[lat_col]))
        
    return radiuses, points_list


def transform_coordinates(coord1, coord2, reverse=False):
    system1, system2 = "epsg:4326", "epsg:32632"
    if reverse:
        system1, system2 = system2, system1 
    transformer = pyproj.Transformer.from_crs(system1, system2)
    
    return transformer.transform(coord1, coord2)


def reverse_coordinates(coordinates_list):

    return [(coor[1], coor[0]) for coor in coordinates_list]


def create_buffer_polygon(point, radius, resolution=1):
    point_utm = transform_coordinates(*point)
    point_buffer = Point(point_utm).buffer(distance = radius, 
                                           resolution = resolution)
    polygon_points = []
    for point in point_buffer.exterior.coords:
        polygon_points.append(transform_coordinates(*point, reverse = True))

    return polygon_points


def style_function(color):

    return lambda feature: dict(color = color, weight = 3, opacity = 0.5)


def get_normal_route(client, coordinates):
    normal_route = client.directions(coordinates,
                                     profile = "foot-walking",
                                     preference = "recommended",
                                     format_out = "geojson",
                                     geometry_simplify = True,
                                     dry_run = False)

    return normal_route


def get_buffer_route(normal_route):
    route = LineString(normal_route["features"][0]["geometry"]["coordinates"])
    buffer_route = route.buffer(0.005)
    
    return buffer_route


def obtain_polygons(route_buffer, points_list, radiuses):
    sites_polygon = []
    
    for site_coordinates, radius in zip(points_list, radiuses):
        if route_buffer.intersects(Point(site_coordinates)):
            site_polygon_coordinates = create_buffer_polygon(site_coordinates, 
                                                             radius = radius)
            sites_polygon.append(Polygon(site_polygon_coordinates))
        
    return sites_polygon


def get_detour_route(client, coordinates, buffer_route, sites_polygon):
    request_params = {"coordinates": coordinates,
                      "profile": "foot-walking",
                      "preference": "recommended",
                      "format_out": "geojson",
                      "options": {
                          "avoid_polygons": geometry.mapping(MultiPolygon(sites_polygon))
                      },
                      "geometry_simplify": True,
                      "dry_run": False}
    
    route_detour = client.directions(**request_params)
    
    return route_detour


def get_detour_route_coordinates(detour_route):
    coor = detour_route["features"][0]["geometry"]["coordinates"]

    return coor


def create_route_json(coordinates, dtype = "dict"):
    if dtype == "dict":
        coordinates = [[element["lng"], element["lat"]] for element in coordinates]
    elif dtype == "list":
        coordinates = [[element[0], element[1]] for element in coordinates]
        
    route = {"type": "Feature",
             "geometry": {"type": "LineString", 
                          "coordinates": coordinates}}
                          
    return route


def main(coordinates):
    API_KEY = "5b3ce3597851110001cf62486d267b042a754245aeb826068a8ea035"
    client = openrouteservice.Client(key=API_KEY)
    coords = (coordinates[0], coordinates[1])
    df = pd.read_csv("points.csv")
    radiuses, points_list = extract_coordinates_radius(dataframe = df, 
                                                       rad_col = "radio(m)", 
                                                       lng_col = "Longitude",
                                                       lat_col = "Latitude")
    normal_route = get_normal_route(client, coords)
    buffer_route = get_buffer_route(normal_route)
    sites_polygon = obtain_polygons(buffer_route, points_list, radiuses)
    route_detour = get_detour_route(client, coords, buffer_route, sites_polygon)
    route_coordinates = get_detour_route_coordinates(route_detour)
    route_coordinates.insert(0, list(coords[0]))
    route_coordinates.append(list(coords[1]))
    
    return create_route_json(route_coordinates, dtype="list")


# Executable

if __name__ == "__main__":
    coords = input("Introduce the coordinates in the correct format: ")
    main(coords)


