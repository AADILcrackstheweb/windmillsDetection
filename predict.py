from ultralytics import YOLO

import cv2
model_path = r"C:\Users\sraad\runs\segment\train5\weights\best.pt"
image_path = r"D:\projct\temp\images\clip15.tif"
img = cv2.imread(image_path)
H, W, _ = img.shape
model = YOLO(model_path)
results = model(img)
for result in results:
    for j, mask in enumerate(result.masks.data):
        mask = mask.numpy() * 255
        mask = cv2.resize(mask, (W, H))
        cv2.imwrite('C:/Users/sraad/Pictures/output.png', mask)

