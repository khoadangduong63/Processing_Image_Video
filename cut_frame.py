import os
import cv2
import argparse


def processWidthHeight(width, height, src_width = 0, src_height = 0, fx = 0, fy = 0):
    if width == 0 and fx == 0:
        width = src_width
    elif width == 0 and fx != 0:
        width = int(round(src_width * fx))

    if height == 0 and fy == 0:
        height = src_height
    elif height == 0 and fy != 0:
        height = int(round(src_height * fy))
    
    return width, height


def cutFrame(input_path, output_path, width, height, fx = 0, fy = 0):
    cap = cv2.VideoCapture(input_path)
    src_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    src_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width, height = processWidthHeight(width, height, src_width, src_height, fx, fy)

    output_path = os.path.join(output_path, "frame", os.path.splitext(os.path.split(input_path)[1])[0])
    if os.path.exists(output_path) == False:
        os.makedirs(output_path)

    count = 0
    while True:
        ret,image = cap.read()
        if ret == True:
            resize = cv2.resize(image, (width, height)) 
            cv2.imwrite(os.path.join(output_path, "%09d.jpg" % count), resize)
            count += 1
        else:
            break

parser = argparse.ArgumentParser(description="Program to cut frame video")
parser.add_argument("--input", type=str, required=True, help="Enter path of file video or path of folder contains images")
parser.add_argument("--output", type=str, default=os.getcwd(), help="Enter name file or address folder to save images and videos")
parser.add_argument("--width", type=int, default = 0, help="Enter resize width")
parser.add_argument("--height", type=int, default = 0, help="Enter resize height")
parser.add_argument("--fx", type=float, default = 0, help="Enter scale factor along the horizontal axis, default = 0")
parser.add_argument("--fy", type=float, default = 0, help="Enter scale factor along the vertical axis, default = 0")
args = parser.parse_args()


input_path = os.path.abspath(args.input)
output_path = os.path.abspath(args.output)

width = args.width
height = args.height
fx = args.fx
fy = args.fy

cutFrame(input_path, output_path, width, height, fx, fy)