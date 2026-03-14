# План роботи з проєктом українською

## 1. Перехід у папку проєкту

Відкрий PowerShell і перейди в папку проєкту:

```powershell
cd C:\Plate\License-Plate-Detection-using-YOLOv10
```

## 2. Встановлення залежностей

Встанови всі потрібні бібліотеки:

```powershell
python -m pip install -r requirements.txt
```

Перевір, що `ultralytics` встановився:

```powershell
python -c "import ultralytics; print(ultralytics.__version__)"
```

## 2.1. Рекомендовано: окреме віртуальне середовище `\.venv`

У цьому проєкті вже зручно працювати через `\.venv`.

### Створення `\.venv`

Якщо середовище ще не створене:

```powershell
py -3.11 -m venv .venv
```

Або повним шляхом до Python:

```powershell
C:\Users\Alexander\AppData\Local\Programs\Python\Python311\python.exe -m venv .venv
```

### Активація `\.venv` у PowerShell

Якщо PowerShell дозволяє запуск скриптів:

```powershell
.\.venv\Scripts\Activate.ps1
```

Якщо бачиш помилку `running scripts is disabled on this system`, виконай для поточної сесії:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Активація через `cmd`

Якщо не хочеш змінювати policy PowerShell:

```powershell
cmd /k .\.venv\Scripts\activate.bat
```

### Запуск без активації `\.venv`

Цей варіант найнадійніший, якщо не хочеш залежати від `PATH` або `ExecutionPolicy`:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Перевірка:

```powershell
.\.venv\Scripts\python.exe -c "import sys, ultralytics; print(sys.executable); print(ultralytics.__version__)"
```

### Встановлення залежностей саме в `\.venv`

Після активації:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Або без активації:

```powershell
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## 3. Підготовка датасету

У тебе має бути така структура:

```text
dataset\Dataset\train
dataset\Dataset\test
```

Якщо датасету ще немає, завантаж і розпакуй:

```powershell
$env:KAGGLE_CONFIG_DIR = (Resolve-Path .kaggle).Path
kaggle datasets download -d alihassanml/yolo-number-plates
Expand-Archive -Path .\yolo-number-plates.zip -DestinationPath .\dataset -Force
```

Файл конфігурації датасету:

- [data.yaml](c:/Plate/License-Plate-Detection-using-YOLOv10/data.yaml)

## 4. Швидка перевірка готової моделі

У репозиторії вже є готові ваги:

- [model/train/weights/best.pt](c:/Plate/License-Plate-Detection-using-YOLOv10/model/train/weights/best.pt)

Запуск перевірки на одному зображенні:

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg
```

Те саме без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

Результати будуть у папці:

```text
runs\detect\license-plate-predict
```

## 4.1. Як запускати `predict.py`

### Найпростіший варіант без активації `\.venv`

```powershell
cd C:\Plate\License-Plate-Detection-using-YOLOv10
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

### Якщо `\.venv` уже активований

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

### Predict на одному фото

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

### Predict на всій папці з тестовими фото

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test --device 0
```

### Predict на відео

```powershell
python predict.py --weights model/train/weights/best.pt --source .\video.mp4 --device 0
```

### Predict з вебкамери

```powershell
python predict.py --weights model/train/weights/best.pt --source 0 --conf 0.5 --device 0
```

### Predict натренованою моделлю після тренування

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test --device 0
```

### Predict без активації `\.venv` на папці

```powershell
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test --device 0
```

### Predict без активації `\.venv` на відео

```powershell
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source .\video.mp4 --device 0
```

### Predict без активації `\.venv` з вебкамери

```powershell
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source 0 --conf 0.5 --device 0
```

### Де шукати результат `predict`

За замовчуванням результати будуть тут:

```text
runs\detect\license-plate-predict
```

### Якщо треба зберегти TXT-координати

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test --device 0 --save-txt
```

### Якщо треба своя назва папки результатів

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test --device 0 --project runs/detect --name my-predict
```

## 5. Тренування на CPU

Якщо GPU ще не налаштована, можна почати з CPU:

```powershell
python train.py --data data.yaml --model yolov10n.pt --device cpu --epochs 10 --batch 8
```

Для повнішого запуску:

```powershell
python train.py --data data.yaml --model yolov10n.pt --device cpu --epochs 100 --imgsz 640 --batch 16
```

## 6. Як підняти обчислення на GPU

### Крок 1. Перевірити, чи є NVIDIA

Виконай:

```powershell
nvidia-smi
```

Якщо ця команда не працює, значить:

- або немає відеокарти NVIDIA
- або не встановлений драйвер NVIDIA

У такому випадку GPU через CUDA не запуститься.

### Крок 2. Перевірити, чи PyTorch бачить CUDA

Виконай:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no gpu')"
```

Правильний результат для GPU має бути приблизно такий:

```text
True
1
NVIDIA ...
```

Якщо бачиш:

```text
False
0
no gpu
```

значить поточний `torch` не бачить CUDA.

### Крок 3. Видалити CPU-версію PyTorch

```powershell
python -m pip uninstall -y torch torchvision torchaudio
```

### Крок 4. Встановити PyTorch з CUDA

Для цього проєкту в `\.venv` зараз використовується GPU-збірка PyTorch з CUDA 12.8.

Після активації `\.venv`:

```powershell
python -m pip uninstall -y torch torchvision torchaudio
python -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe -m pip uninstall -y torch torchvision torchaudio
.\.venv\Scripts\python.exe -m pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128
```

Якщо на момент встановлення версія CUDA на сайті PyTorch буде інша, дивись актуальну команду тут:

- https://pytorch.org/get-started/locally/

### Крок 5. Повторно перевірити CUDA

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no gpu')"
```

Якщо тепер бачиш `True`, GPU готова.

### Крок 6. Запуск тренування на GPU

Для однієї відеокарти:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

Те саме без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

Для кількох GPU:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0,1
```

### Крок 7. Як зрозуміти, що тренування йде на GPU

Під час тренування:

- у логах не повинно бути помилки про `Invalid CUDA 'device=0'`
- `torch.cuda.is_available()` має бути `True`
- у `nvidia-smi` має з’явитися процес `python`

Окремо можна відкрити ще одне вікно PowerShell і дивитися:

```powershell
nvidia-smi
```

## 7. Повне тренування

Коли все працює, запускай:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

Те саме без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

Якщо GPU немає:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 8 --device cpu
```

Короткий smoke test перед довгим тренуванням:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 1 --imgsz 640 --batch 8 --device 0
```

Швидкий старт на GPU для перевірки:

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

Приклад повного запуску без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

## 7.1. Як запускати `train.py`

### Найпростіший варіант без активації `\.venv`

```powershell
cd C:\Plate\License-Plate-Detection-using-YOLOv10
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

### Якщо `\.venv` уже активований

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

### Короткий тест тренування на GPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 1 --imgsz 640 --batch 8 --device 0
```

### Швидкий старт тренування на GPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

### Повне тренування на GPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

### Тренування на CPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device cpu
```

### Повне тренування на CPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 8 --device cpu
```

### Тренування без активації `\.venv` на GPU

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

### Повне тренування без активації `\.venv` на GPU

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

### Тренування без активації `\.venv` на CPU

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device cpu
```

### Якщо треба інша назва запуску

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0 --name my-train
```

### Якщо треба власна папка для результатів

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0 --project runs/detect
```

### Якщо хочеш швидше підвантаження зображень

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0 --cache
```

### Якщо хочеш змінити кількість воркерів

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0 --workers 4
```

### Де будуть результати `train`

За замовчуванням результати будуть тут:

```text
runs\detect\license-plate-train
```

Найважливіший файл після тренування:

```text
runs\detect\license-plate-train\weights\best.pt
```

## 8. Де будуть результати тренування

Після тренування дивись папку:

```text
runs\detect\license-plate-train
```

Головні файли:

- `weights\best.pt`
- `weights\last.pt`
- `results.png`
- `results.csv`
- `confusion_matrix.png`
- `PR_curve.png`

## 9. Що робити після тренування

Бери найкращі ваги:

```text
runs\detect\license-plate-train\weights\best.pt
```

Запуск на тестових зображеннях:

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test
```

Те саме без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test
```

Запуск на одному файлі:

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg
```

Запуск на відео:

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source .\video.mp4
```

Запуск на вебкамері:

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source 0 --conf 0.5
```

Запуск готової моделі з репозиторію без тренування:

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

Запуск готової моделі без активації `\.venv`:

```powershell
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

Збереження координат у TXT:

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test --save-txt
```

Запуск з власною папкою результатів:

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test --project runs/detect --name custom-predict
```

## 10.1. Готові команди, які можна просто копіювати

### Перехід у проєкт

```powershell
cd C:\Plate\License-Plate-Detection-using-YOLOv10
```

### Активація `\.venv` у PowerShell

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### Перевірка, що Python береться саме з `\.venv`

```powershell
python -c "import sys; print(sys.executable)"
```

### Перевірка GPU

```powershell
nvidia-smi
python -c "import torch; print(torch.__version__); print(torch.cuda.is_available()); print(torch.cuda.device_count()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no gpu')"
```

### Запуск короткого тренування на GPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
```

### Запуск повного тренування на GPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 16 --device 0
```

### Запуск повного тренування на CPU

```powershell
python train.py --data data.yaml --model yolov10n.pt --epochs 100 --imgsz 640 --batch 8 --device cpu
```

### Перевірка готової моделі на одному зображенні

```powershell
python predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
```

### Перевірка натренованої моделі на папці

```powershell
python predict.py --weights runs/detect/license-plate-train/weights/best.pt --source dataset/Dataset/test --device 0
```

### Усе те саме без активації `\.venv`

```powershell
.\.venv\Scripts\python.exe train.py --data data.yaml --model yolov10n.pt --epochs 10 --imgsz 640 --batch 8 --device 0
.\.venv\Scripts\python.exe predict.py --weights model/train/weights/best.pt --source dataset/Dataset/test/frame-2955.jpg --device 0
.\.venv\Scripts\python.exe -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'no gpu')"
```

## 10. Правильний порядок дій

1. Перейти в папку проєкту.
2. Встановити залежності.
3. Перевірити, що датасет розпакований.
4. Запустити `predict.py` на готових вагах.
5. Перевірити, чи доступна GPU.
6. Якщо GPU не працює, встановити CUDA-версію PyTorch.
7. Запустити коротке тренування.
8. Потім запустити повне тренування.
9. Взяти `best.pt`.
10. Перевірити модель на фото, відео або камері.

## 11. Важливі зауваження

- Не використовуй стару команду з `--cfg` і `--weights` для `train.py`.
- Для тренування використовуй `--model`.
- Для розпізнавання використовуй [predict.py](c:/Plate/License-Plate-Detection-using-YOLOv10/predict.py).
- Якщо `yolov10n.pt` відсутній, Ultralytics може завантажити його з інтернету під час першого запуску.
- Якщо `torch.cuda.is_available()` повертає `False`, тренування на GPU не запуститься.
- У твоєму середовищі `\.venv` уже налаштований GPU PyTorch: `torch 2.10.0+cu128`.
- Поточна перевірка GPU для цього ноутбука: `NVIDIA GeForce RTX 5070 Laptop GPU`.
- Якщо PowerShell блокує `Activate.ps1`, можна або тимчасово виконати `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`, або завжди запускати через `.\.venv\Scripts\python.exe`.
