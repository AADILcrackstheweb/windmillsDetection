from ultralytics import YOLO

model = YOLO('yolov8n-seg.pt')  # load a pretrained model (recommended for training)

model.train(data='/path/to/your/config/file', epochs=50, imgsz=224)
