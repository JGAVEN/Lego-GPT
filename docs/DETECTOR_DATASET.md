# Brick Detector Dataset Format

> **Note**: The project launches with an English-only interface and does not support additional languages.

This document describes the expected layout for training the YOLOv8 brick detector with the `lego-detect-train` command.

The dataset should follow the standard [Ultralytics](https://docs.ultralytics.com/datasets/detect/) directory structure:

```
<dataset>/
├── images
│   ├── train
│   └── val
└── labels
    ├── train
    └── val
```

Each image has a corresponding label file under `labels/` with the same file name and the YOLO text annotation format:

```
<class> <x_center> <y_center> <width> <height>
```

Coordinates are normalised between 0 and 1. The `data.yaml` file references the image folders and lists the class names:

```yaml
train: images/train
val: images/val
nc: <number-of-classes>
names:
  0: 3001
  1: 3003
```

Running `lego-detect-train data.yaml --epochs 100 --out detector/model.pt` outputs a weights file suitable for the detector worker.

Mount the dataset directory into the training container:

```bash
docker run -v /path/to/dataset:/data lego-detect-train lego-detect-train /data/data.yaml --out /app/detector/model.pt
```
