import json
import os
from PIL import Image
from datetime import datetime

classes = {"id": 0, "name": "starfish", "supercategory": "none"}
# 画像サイズを指定
image_width = 1280  # 画像の実際の幅
image_height = 720  # 画像の実際の高さ

def yolo_to_coco(yolo_annotation_dir, yolo_image_dir, coco_output_file):
    # COCOデータセットの構造を初期化
    annotations_json = {
        "info": {},
        "licenses": [],
        "categories": [],
        "images": [],
        "annotations": []
    }
    
    # 現在の日付と時刻を取得し、ISO 8601形式で設定
    current_datetime = datetime.now().isoformat()
    # 現在の年を取得
    current_year = str(datetime.now().year)

    # "info" フィールドを設定
    annotations_json["info"] = {
        "year": current_year,
        "version": "1.0",
        "description": "YOLO to COCO converted dataset",
        "contributor": "",
        "url": "",
        "date_created": current_datetime
    }

    # "licenses" フィールドを設定
    license_info = {
        "id": 1,
        "url": "",
        "name": "Unknown"
    }
    annotations_json["licenses"].append(license_info)

    annotation_id = 1

    # 指定ディレクトリ内のすべてのYOLOアノテーションファイルを処理
    yolo_annotation_files = [f for f in os.listdir(yolo_annotation_dir) if f.endswith(".txt")]
    for yolo_annotation_file in yolo_annotation_files:
        with open(os.path.join(yolo_annotation_dir, yolo_annotation_file), "r") as f:
            lines = f.read().strip().split("\n")

        for line in lines:
            line_parts = line.split(" ")
            yolo_box = line_parts[1:]
            x, y, w, h = map(float, yolo_box)
            
            # バウンディングボックスを実際の画像サイズにスケーリング
            x *= image_width
            y *= image_height
            w *= image_width
            h *= image_height

            image_filename = yolo_annotation_file.replace(".txt", ".jpg")
            image_info = {
                "id": annotation_id,
                "license": 1,
                "file_name": image_filename,
                "height": image_height,  # 画像の実際の高さと幅を設定する必要があります
                "width": image_width,
                "date_captured": current_datetime
            }

            annotations_json["images"].append(image_info)

            coco_category_id = line_parts[0]  # クラスIDをそのままCOCOカテゴリIDとして使用

            coco_annotation = {
                "id": annotation_id,
                "image_id": annotation_id,
                "category_id": coco_category_id,
                "bbox": [x, y, w, h],
                "area": w * h,
                "segmentation": [],
                "iscrowd": 0
            }

            annotations_json["annotations"].append(coco_annotation)
            annotation_id += 1

    # 画像の実際の高さと幅を設定
    for image_info in annotations_json["images"]:
        image_path = os.path.join(yolo_image_dir, image_info["file_name"])
        image = Image.open(image_path)
        width, height = image.size
        image_info["width"] = width
        image_info["height"] = height

    # COCOデータセットをJSONファイルとして保存
    with open(coco_output_file, "w") as f:
        json.dump(annotations_json, f)

    print("YOLO dataset converted to COCO format and saved to", coco_output_file)

# Usage
yolo_annotation_dir = r"C:\Users\user\Desktop\Data\labels\valid"
yolo_image_dir = r"C:\Users\user\Desktop\Data\images\valid"
coco_output_file = "output_coco_dataset.json"

yolo_to_coco(yolo_annotation_dir, yolo_image_dir, coco_output_file)
