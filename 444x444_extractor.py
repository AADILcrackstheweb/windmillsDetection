import sys
from qgis.core import QgsApplication, QgsProject, QgsVectorLayer, QgsFeature, QgsGeometry, QgsField, QgsFields, QgsWkbTypes
from qgis.PyQt.QtCore import QVariant
from qgis.analysis import QgsNativeAlgorithms

# Initialize QGIS Application
qgs = QgsApplication([], False)
qgs.initQgis()

# Append the path where processing module can be found
sys.path.append('/Applications/QGIS.app/Contents/Resources/python/plugins')

import processing
from processing.core.Processing import Processing
Processing.initialize()
qgs.processingRegistry().addProvider(QgsNativeAlgorithms())

# Specify the path to the raster and vector layers
raster_path = '/Users/kavindev/Desktop/SentinelFiles/LastTime/MergedLayer.tif'
vector_path = '/Users/kavindev/Desktop/SentinelFiles/LastTime/vectorMask.gpkg'

# Load the vector layer
vector_layer = QgsProject.instance().addMapLayer(QgsVectorLayer(vector_path, "vector", "ogr"))

if not vector_layer or not vector_layer.isValid():
    print("Vector layer failed to load! Check the name or path.")
else:
    print("Vector layer loaded successfully.")

# Iterate through features and clip raster
for feature in vector_layer.getFeatures():
    # Create a temporary layer to store the individual feature
    temp_layer = QgsVectorLayer("Polygon?crs=epsg:4326", "temp", "memory")
    temp_layer_data = temp_layer.dataProvider()
    temp_layer.startEditing()
    temp_layer_data.addFeatures([feature])
    temp_layer.commitChanges()

    output_path = f'/Users/kavindev/Desktop/SentinelFiles/godPlease/clip_{feature.id()}.tif'  # Output path
    # Run the clipping using the temporary layer as mask
    processing.run("gdal:cliprasterbymasklayer", {
        'INPUT': raster_path,
        'MASK': temp_layer,
        'TARGET_CRS': vector_layer.crs().toWkt(),
        'CROP_TO_CUTLINE': True,
        'KEEP_RESOLUTION': True,
        'OUTPUT': output_path
    })
    print(f'Output generated for feature ID {feature.id()} at {output_path}')

# Exit the QGIS Application
qgs.exitQgis()
