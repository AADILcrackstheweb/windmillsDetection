# Windmill Detection using Satellite Imagery

Welcome to the Windmill Detection Project! This repository focuses on creating a custom dataset for windmill detection using satellite imagery from the Boonidhi portal and developing a custom model for accurate windmill detection.

## Table of Contents
- [Introduction](#introduction)
- [Dataset Preparation](#dataset-preparation)
  - [Dataset Download](#dataset-download)
  - [Data Processing](#data-processing)
- [Data Annotation](#data-annotation)
- [Model Training](#model-training)
- [Contributing](#contributing)
- [License](#license)

## Introduction
This project aims to create a robust dataset and model for detecting windmills using satellite imagery. The dataset is sourced from the Boonidhi portal and processed through a series of steps to prepare it for training a custom YOLOv8 model.

## Dataset Preparation

### Dataset Download

1. **Write an Overpass Turbo API Query**:
   - Obtain the windmill coordinates for your area of interest using [Overpass Turbo](https://overpass-turbo.eu/).

2. **Export Data**:
   - Export the retrieved data as a GeoJSON file.

3. **Convert GeoJSON to Shapefile**:
   - Use the script `shapefileConvertor.py` to convert the GeoJSON file to a shapefile, which is compatible with the Boonidhi portal.
   - Access the [Bhoonidhi Portal](https://bhoonidhi.nrsc.gov.in/bhoonidhi/login.html) for further steps.

### Data Processing

1. **Merge Bands and Create True Colour Image**:
   - Use QGIS software to merge different bands of the downloaded imagery and create a true colour band. Adjust brightness, contrast, and gamma as needed.

2. **Overlay GeoJSON Layer**:
   - Overlay the GeoJSON layer onto the raster layer in QGIS to pinpoint the windmills.

3. **Convert Points to Bounding Boxes**:
   - Use the "Rectangles, Ovals and Diamond" tool in QGIS to create bounding boxes of 444x444 pixels around the windmills.

4. **Extract 444x444 Images**:
   - Utilize the script `444x444_extractor.py` as a Python plugin in QGIS to download the 444x444 images.

5. **Create 224x224 Patches**:
   - Generate 224x224 random patches from the 444x444 images using the script `224x224_Clipper.py`.

## Data Annotation

1. **Create a CVAT Project**:
   - Set up a new project in [CVAT](https://www.cvat.ai/).

2. **Create a Task**:
   - Within the project, create a task and use "windmill" as the label name.

3. **Annotate Images**:
   - Annotate the 6x6 square patches, ensuring windmills are at the centre of each patch.

## Model Training

1. **Train with YOLOv8**:
   - Use the YOLOv8 framework to train the custom windmill detection model with the prepared and annotated dataset.

## Contributing

We welcome contributions to this project! If you have suggestions for improvements or find any issues, please open an issue or submit a pull request. Please follow the [contributing guidelines](CONTRIBUTING.md).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Feel free to contribute to this project by following the above steps. For any issues or queries, please refer to the provided scripts or reach out to the project maintainers.
