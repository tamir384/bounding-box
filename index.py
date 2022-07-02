import math
import cv2
import os

images_path = input('Please enter the path to the images folder\n')
detection_file_path = input('Please enter the path to the detection file\n')
visualizations_path = input("Please enter the path to the visualizations folder (destination)\n")
cars_color = input("Please enter a color for the bounding-boxes of cars in B,G,R format, for example: 255,0,0\n")
cars_color = cars_color.split(',')
pedestrians_color = input("Please enter a color for the bounding-boxes of pedestrians in B,G,R format, for example: "
                          "255,0,0\n")
pedestrians_color = pedestrians_color.split(',')
motors_color = input("Please enter a color for the bounding-boxes of motors in B,G,R format, for example: 255,0,0\n")
motors_color = motors_color.split(',')
colors = {0: (int(pedestrians_color[0]), int(pedestrians_color[1]), int(pedestrians_color[2])),
          1: (int(motors_color[0]), int(motors_color[1]), int(motors_color[2])),
          2: (int(cars_color[0]), int(cars_color[1]), int(cars_color[2]))}


def insert_rectangle(img, bounding_box):
    x = int(bounding_box[0])
    y = int(bounding_box[1])
    width = int(bounding_box[2])
    height = int(bounding_box[3])
    label = int(bounding_box[4])
    score = (math.floor(int(bounding_box[5]) / 20)) + 1
    cv2.rectangle(img, (int(x - width / 2), int(y + height / 2)), (int(x + width / 2), int(y - height / 2)),
                  colors[label], score)


detections_dictionary = {}
with open(detection_file_path) as f:
    for line in f:
        splitted_line = line.split("\t")
        file_name = splitted_line[0]
        splitted_line[6] = splitted_line[6].strip()
        objects_array = []
        if not file_name in detections_dictionary:
            detections_dictionary[file_name] = objects_array
        else:
            objects_array = detections_dictionary[file_name]
        objects_array.append(splitted_line[1:])

for (root, dirs, files) in os.walk(images_path):
    for file_name in files:
        if not file_name.startswith('.'):  # ignoring .DS_Store hidden file to avoid exceptions
            image = cv2.imread(f"{images_path}/{file_name}")
            if file_name in detections_dictionary:
                for bb in detections_dictionary[file_name]:
                    insert_rectangle(image, bb)
            cv2.imwrite(f"{visualizations_path}/{file_name}", image)
