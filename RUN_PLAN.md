# Run And Train Plan

## 1. Prepare Environment

Open PowerShell in the project folder:

```powershell
cd C:\Plate\License-Plate-Detection-using-YOLOv10
```

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Check that Ultralytics is available:

```powershell
python -c "import ultralytics; print(ultralytics.__version__)"
```

## 2. Prepare Dataset

If the dataset is not downloaded yet:

```powershell
$env:KAGGLE_CONFIG_DIR = (Resolve-Path .kaggle).Path
kaggle datasets download -d alihassanml/yolo-number-plates
Expand-Archive -Path .\yolo-number-plates.zip -DestinationPath .\dataset -Force
```

Expected dataset structure:

```text
dataset/
  Dataset/
    train/
    test/
```

The project uses:

- [data.yaml](c:/Plate/License-Plate-Detection-using-YOLOv10/data.yaml)
- class `0: license_plate`

## 3. Start Training

Standard training command:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16
```

Training on CPU:

```powershell
python train.py --data data.yaml --model yolov10n.pt --device cpu --epochs 10 --batch 8
```

Training with another model size:

```powershell
python train.py --data data.yaml --model yolov10s.pt --epochs 100 --imgsz 640 --batch 16
```

Output location after training:

```text
runs/detect/license-plate-train/
```

Main output files:

- `weights/best.pt`
- `weights/last.pt`
- `results.png`
- `results.csv`

## 4. Run Prediction

Prediction on one image:

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg
```

Prediction on the whole test folder:

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test
```

Prediction from webcam:

```powershell
python predict.py --weights model/train/weights/best.pt --source 0 --conf 0.5
```

Output location after prediction:

```text
runs/detect/license-plate-predict/
```

## 5. Recommended Working Order

1. Install dependencies.
2. Verify dataset exists in `dataset/Dataset`.
3. Run a quick prediction with existing weights `model/train/weights/best.pt`.
4. Start a short training run for validation.
5. Start full training.
6. Run prediction on test images, video, or webcam.

## 6. Important Notes

- Do not use the old command with `--cfg` and `--weights`.
- Use `--model` instead of `--weights` in [train.py](c:/Plate/License-Plate-Detection-using-YOLOv10/train.py).
- Use [predict.py](c:/Plate/License-Plate-Detection-using-YOLOv10/predict.py) for inference.
- The old README command `python train.py --data dataset/data.yaml --cfg cfg/yolov10.yaml --weights yolov10.pt` is not valid for this repository.
- If `yolov10n.pt` is missing, Ultralytics may download it from the internet during the first training run.
