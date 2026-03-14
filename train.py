from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Train a license plate detector with Ultralytics YOLO.")
    parser.add_argument("--data", default="data.yaml", help="Path to dataset YAML.")
    parser.add_argument("--model", default="yolov10n.pt", help="Base model checkpoint or YAML.")
    parser.add_argument("--epochs", type=int, default=100, help="Number of training epochs.")
    parser.add_argument("--imgsz", type=int, default=640, help="Training image size.")
    parser.add_argument("--batch", type=int, default=16, help="Batch size.")
    parser.add_argument("--device", default=None, help="Device, e.g. cpu, 0, 0,1.")
    parser.add_argument("--project", default=None, help="Custom output project directory.")
    parser.add_argument("--name", default="license-plate-train", help="Run name.")
    parser.add_argument("--workers", type=int, default=8, help="Data loader workers.")
    parser.add_argument("--cache", action="store_true", help="Cache images for faster training.")
    parser.add_argument("--patience", type=int, default=30, help="Early stopping patience.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    data_path = Path(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"Dataset config not found: {data_path}")

    model = YOLO(args.model)
    train_kwargs = {
        "data": str(data_path),
        "epochs": args.epochs,
        "imgsz": args.imgsz,
        "batch": args.batch,
        "device": args.device,
        "name": args.name,
        "workers": args.workers,
        "cache": args.cache,
        "patience": args.patience,
        "plots": True,
    }
    if args.project:
        train_kwargs["project"] = args.project

    model.train(**train_kwargs)


if __name__ == "__main__":
    main()
