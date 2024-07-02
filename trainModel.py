from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')  # load a pretrained model (recommended for training)

model.train(data='D:\image-segmentation-yolov8-main\image-segmentation-yolov8-main\config.yaml', epochs=50, imgsz=224)
