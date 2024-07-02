from ultralytics import YOLO

import cv2
model_path = '/path/to/your/project/directory/'
image_path = '/path/to/your/project/directory/'
img = cv2.imread(image_path)
H, W, _ = img.shape
model = YOLO(model_path)
results = model(img)
for result in results:
    for j, mask in enumerate(result.masks.data):
        mask = mask.numpy() * 255
        mask = cv2.resize(mask, (W, H))
        cv2.imwrite('/path/to/your/project/directory/', mask)

