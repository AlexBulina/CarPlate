# License Plate Detection using Ultralytics YOLOv10

This repository now includes a working local training and prediction flow based on `ultralytics`.

![License Plate Detection](./model/predict/frame-2955.jpg)

## Dataset

The Kaggle dataset extracts to `dataset/Dataset` and is already in YOLO detection format:

- `dataset/Dataset/train`
- `dataset/Dataset/test`

There is one class in the annotations:

- `0: license_plate`

The dataset config is stored in [data.yaml](./data.yaml).

## Setup

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

If you still need to download the dataset:

```powershell
$env:KAGGLE_CONFIG_DIR = (Resolve-Path .kaggle).Path
kaggle datasets download -d alihassanml/yolo-number-plates
Expand-Archive -Path .\yolo-number-plates.zip -DestinationPath .\dataset -Force
```

## Train

Start training from the YOLOv10 nano checkpoint:

```powershell
python train.py --model yolov10n.pt --data data.yaml --epochs 100 --imgsz 640 --batch 16
```

Useful variants:

```powershell
python train.py --device cpu --epochs 10 --batch 8
python train.py --model yolov10s.pt --cache
```

Training outputs are written to `runs/detect/license-plate-train` by default.

## Predict

Run prediction on a single image:

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg
```

Run prediction on a folder:

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test
```

Run prediction from webcam:

```powershell
python predict.py --weights model/train/weights/best.pt --source 0 --conf 0.5
```

Prediction outputs are written to `runs/detect/license-plate-predict` by default.

## Notes

- The original README referenced `train.py` and `detect.py`, but those files were not present in the repository.
- A previous trained checkpoint already exists at `model/train/weights/best.pt`.
- If `ultralytics` needs to download pretrained weights such as `yolov10n.pt`, the machine must have network access at run time.

## License

This project is licensed under the MIT License. See [LICENSE](./LICENSE).
