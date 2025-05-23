#!/usr/bin/env python3
"""Utility to fine-tune a YOLOv8 model for brick detection."""
from __future__ import annotations

import argparse
from pathlib import Path
from types import SimpleNamespace


def _load_yolo() -> SimpleNamespace:
    """Return the YOLO class from ultralytics or raise RuntimeError."""
    try:
        from ultralytics import YOLO  # type: ignore
        return SimpleNamespace(YOLO=YOLO)
    except Exception as exc:  # pragma: no cover - optional dependency missing
        raise RuntimeError("ultralytics package is required for training") from exc


def train(data_yaml: str, model: str, epochs: int, out_path: Path) -> None:
    """Train and save a YOLOv8 model."""
    yolo_mod = _load_yolo()
    yolo = yolo_mod.YOLO(model)
    results = yolo.train(data=data_yaml, epochs=epochs)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    best_pt = Path(results.save_dir) / "weights" / "best.pt"
    try:
        best_pt.rename(out_path)
    except FileNotFoundError:  # pragma: no cover - training did not produce file
        pass
    print(f"Model saved to {out_path}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Train YOLOv8 brick detector")
    parser.add_argument("data", help="Path to dataset YAML")
    parser.add_argument("--model", default="yolov8n.pt", help="Base model weights")
    parser.add_argument("--epochs", type=int, default=50, help="Number of epochs")
    parser.add_argument(
        "--out",
        default="detector/model.pt",
        help="Destination path for trained weights",
    )
    args = parser.parse_args(argv)
    train(args.data, args.model, args.epochs, Path(args.out))


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()
