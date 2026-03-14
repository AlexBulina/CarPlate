from __future__ import annotations

import argparse
from pathlib import Path

from ultralytics import YOLO


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run prediction with a trained Ultralytics YOLO model.")
    parser.add_argument(
        "--weights",
        default="model/train/weights/best.pt",
        help="Path to trained weights or a pretrained YOLO checkpoint.",
    )
    parser.add_argument(
        "--source",
        default="dataset/Dataset/test/frame-2955.jpg",
        help="Image, folder, video, URL, or webcam index like 0.",
    )
    parser.add_argument("--conf", type=float, default=0.25, help="Confidence threshold.")
    parser.add_argument("--imgsz", type=int, default=640, help="Inference image size.")
    parser.add_argument("--device", default=None, help="Device, e.g. cpu or 0.")
    parser.add_argument("--project", default=None, help="Custom output project directory.")
    parser.add_argument("--name", default="license-plate-predict", help="Run name.")
    parser.add_argument("--save-txt", action="store_true", help="Save YOLO txt predictions.")
    parser.add_argument("--show", action="store_true", help="Show predictions in a window.")
    return parser.parse_args()


def normalize_source(raw_source: str) -> str | int:
    if raw_source.isdigit():
        return int(raw_source)

    source_path = Path(raw_source)
    if source_path.exists():
        return str(source_path)

    return raw_source


def main() -> None:
    args = parse_args()
    weights_path = Path(args.weights)
    if not weights_path.exists() and not args.weights.endswith(".pt"):
        raise FileNotFoundError(f"Weights not found: {weights_path}")

    model = YOLO(args.weights)
    predict_kwargs = {
        "source": normalize_source(args.source),
        "conf": args.conf,
        "imgsz": args.imgsz,
        "device": args.device,
        "name": args.name,
        "save": True,
        "save_txt": args.save_txt,
        "show": args.show,
    }
    if args.project:
        predict_kwargs["project"] = args.project

    model.predict(**predict_kwargs)


if __name__ == "__main__":
    main()
