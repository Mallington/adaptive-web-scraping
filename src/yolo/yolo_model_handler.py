import torch

# Model
model = torch.hub.load('/Users/mathew/github/adaptive-web-scraping/models/ ', 'CoVa-dataset-train-V1.pt')  # or yolov5m, yolov5l, yolov5x, custom

# Images
img = 'https://ultralytics.com/images/zidane.jpg'  # or file, Path, PIL, OpenCV, numpy, list

# Inference
results = model(img)

# Results
results.print()  # or .show(), .save(), .crop(), .pandas(), etc.
torch.jit.load('DeepLab.pth').eval().to(device)