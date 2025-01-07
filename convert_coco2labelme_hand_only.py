import io 
import json
import os
import codecs
from PIL import Image
def encodeImageForJson(image):
    img_pil = Image.open(image)
    f = io.BytesIO()
    img_pil.save(f, format='PNG')
    data = f.getvalue()
    encData = codecs.encode(data, 'base64').decode()
    encData = encData.replace('\n', '')
    return encData

def convert(coco_direction, coco_file, out):
    
    image_path  = coco_file[:-4] + 'jpg' #os.path.join(image_direction, coco_file[:-4] + 'jpg')
    
    labelme_annotation = {
        "version": "5.5.0",
        "flags": dict(),
        "shapes": [],
        "imagePath": image_path,
        "imageData": None, #encodeImageForJson(os.path.join(coco_direction, image_path)), 
        "imageHeight": 3840,
        "imageWidth": 1920
    }
    
    labels = ["lwrist","lthumb", "lindex", "lmiddle", "lring", "lpinky", "rwrist","rthumb", "rindex", "rmiddle", "rring", "rpinky"]
    label_counts = [1,4,4,4,4,4,1,4,4,4,4,4]
    with open(os.path.join(coco_direction, coco_file), "r") as json_file:
        data = json.load(json_file)
        people = data 
        person_id = 0
        for person in people:
            points = person['keypoints']
            label = 0
            count = 0
            shape = None
            for i in range(len(points)):
                if i < 91:
                    continue
                #print(label, i, labels[label])
                if count == 0: 
                    shape = {
                        "label": labels[label], 
                        "points": [
                            points[i]
                        ],
                        "group_id": person_id,
                        "description": str(i),
                        "shape_type": "linestrip",
                        "flags": dict(),
                        "mask": None
                    }
                    if label == 0 or label == 6:
                        shape["shape_type"] = "point"
                    #count += 1 
                else:
                    shape["points"].append(points[i])

                count += 1 
                if count == label_counts[label]:
                    labelme_annotation["shapes"].append(shape)
                    print(count, len(shape["points"]))
                    label+=1
                    count = 0
            person_id += 1
    with open(os.path.join(out, coco_file), "w") as json_save_file:
        json.dump(labelme_annotation, json_save_file)

json_path = "path-to-jsons-and-images"
list_json = os.listdir(json_path)

for json_file in list_json:
    if 'json' in json_file:
        convert(json_path, json_file, "output")
