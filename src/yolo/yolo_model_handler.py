import os
import sys
from pathlib import Path

import torch

FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # YOLOv5 root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH
ROOT = Path(os.path.relpath(ROOT, Path.cwd()))  # relative

from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import (check_img_size, cv2, non_max_suppression, print_args, scale_coords, xyxy2xywh)

from yolov5.utils.torch_utils import select_device

from yolov5.utils.augmentations import letterbox
import numpy as np

def cv2_to_tensor_image(img0, model, device, img_size=[640,640], stride=32, auto=True):
    img = letterbox(img0, img_size, stride=stride, auto=auto)[0]

    # Convert
    img = img.transpose((2, 0, 1))[::-1]  # HWC to CHW, BGR to RGB
    img = np.ascontiguousarray(img)

    img = torch.from_numpy(img).to(device)
    img = img.half() if model.fp16 else img.float()  # uint8 to fp16/32
    img /= 255  # 0 - 255 to 0.0 - 1.0
    if len(img.shape) == 3:
        img = img[None]  # expand for batch dim

    return img


class Model_Handler:
    def __init__(self,
                 weights,
                 imgsz,
                 device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
                 half=False,  # use FP16 half-precision inference
                 dnn=False,  # use OpenCV DNN for ONNX inference
                 ):

        # Load model
        self.device = select_device(device)
        self.model = DetectMultiBackend(weights, device=self.device, dnn=dnn, fp16=half)
        self.stride, self.names, self.pt = self.model.stride, self.model.names, self.model.pt
        self.imgsz = check_img_size(imgsz, s=self.stride)  # check image size
        bs = 1  # batch_size
        self.model.warmup(imgsz=(1 if self.pt else bs, 3, *self.imgsz))  # warmup

    def predict(self,
                loaded_image,
                augment=False,  # augmented inference
                visualize=False,
                conf_thres=0.25,  # confidence threshold
                iou_thres=0.45,  # NMS IOU threshold
                max_det=1000,  # maximum detections per image
                classes=None,
                agnostic_nms=False
                ):

        tensor_image = cv2_to_tensor_image(loaded_image, self.model, self.device, img_size=self.imgsz, stride=self.stride, auto=self.pt)

        height, width, _ = loaded_image.shape
        pred = self.model(tensor_image, augment=augment, visualize=visualize)

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Second-stage classifier (optional)
        # pred = utils.general.apply_classifier(pred, classifier_model, im, im0s)

        # Process predictions
        s = ""
        predictions_relative = []
        predictions_absolute = []


        for i, det in enumerate(pred):  # per image

            s += '%gx%g ' % tensor_image.shape[2:]  # print string
            gn = torch.tensor(loaded_image.shape)[[1, 0, 1, 0]]  # normalization gain whwh

            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(tensor_image.shape[2:], det[:, :4], loaded_image.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    s += f"{n} {self.names[int(c)]}{'s' * (n > 1)}, "  # add to string

                # Write results
                for *xyxy, conf, cls in reversed(det):
                    xywh = (xyxy2xywh(torch.tensor(xyxy).view(1, 4)) / gn).view(-1).tolist()  # normalized xywh

                    predictions_relative.append([int(cls)] +  xywh)
                    predictions_absolute.append([int(cls)] + [int(a) for a in xyxy])
            print(s)
        return predictions_relative, predictions_absolute

if __name__ == "__main__":
    from src.yolo.yolo_box_visualiser import show_image_with_labels
    loaded_image = cv2.imread("../../../../../../var/folders/j6/2rvpb16156j8_s_r83ddmd0w0000gn/T/TemporaryItems/NSIRD_screencaptureui_xzqmYn/Screenshot 2022-04-18 at 15.43.51.png")
    model_handler = Model_Handler("/Users/mathew/github/adaptive-web-scraping/models/CoVa-dataset-train-V1.pt", [640, 640])
    predictions_relative, predictions_absolute = model_handler.predict(loaded_image)

    show_image_with_labels(loaded_image,predictions_relative, names=["interest_area", "not_interesting"])
    print(predictions_relative, predictions_absolute)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



