import geopandas as gpd
from shapely.geometry import MultiPoint
from shapely.geometry import Polygon
from sklearn.cluster import DBSCAN
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(message)s')

# Load the GeoJSON file
gdf = gpd.read_file('/Users/kavindev/Downloads/tn_windmills.geojson')

# Extract coordinates from GeoDataFrame
coords = gdf.geometry.apply(lambda geom: (geom.x, geom.y)).tolist()

# Cluster points using DBSCAN
db = DBSCAN(eps=0.01, min_samples=3).fit(coords)  # Adjust eps and min_samples as needed
labels = db.labels_

# Create a GeoDataFrame to store clusters
gdf['cluster'] = labels
clusters = {}

for label in set(labels):
    if label != -1:  # Ignore noise points
        cluster_points = gdf[gdf['cluster'] == label]
        if len(cluster_points) > 2:  # Minimum three points to form a polygon
            clusters[label] = cluster_points

# Sort clusters by size in descending order and select the top 80
sorted_clusters = sorted(clusters.items(), key=lambda item: len(item[1]), reverse=True)[:80]

# Simplification function to reduce vertices
def simplify_polygon(polygon, max_vertices=500, tolerance=0.01):
    vertices_count = len(polygon.exterior.coords)
    logging.info(f'Initial vertices count: {vertices_count}')
    while len(polygon.exterior.coords) > max_vertices:
        tolerance += 0.01  # Increase tolerance to simplify further
        polygon = polygon.simplify(tolerance, preserve_topology=True)
        vertices_count = len(polygon.exterior.coords)
        logging.info(f'Simplified to {vertices_count} vertices with tolerance {tolerance}')
    return polygon

polygons = []
for label, points in sorted_clusters:
    multipoint = MultiPoint(points.geometry.tolist())
    polygon = multipoint.convex_hull  # Create a convex hull polygon
    simplified_polygon = simplify_polygon(polygon)  # Simplify the polygon until vertex limit is met
    polygons.append(simplified_polygon)

# Create a new GeoDataFrame for polygons
polygons_gdf = gpd.GeoDataFrame(geometry=polygons)

# Ensure CRS is set, copying from original if it exists, or setting it to a common CRS like EPSG:4326
if gdf.crs:
    polygons_gdf.set_crs(gdf.crs, inplace=True)
else:
    polygons_gdf.set_crs("EPSG:4326", inplace=True)  # Set to WGS 84 if unknown

# Save the polygons to a Shapefile
polygons_gdf.to_file('/Users/kavindev/Downloads/tn_windmills.shp')
