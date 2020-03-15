import os
import cv2
import argparse

def getPathOutput(output_path):
  if os.path.isdir(output_path) == False:
    os.makedirs(output_path)
  return output_path


def run(input_path, output_path, width, height, fps, angle = 0, fx = 0, fy = 0):
  if os.path.isfile(input_path):
    output_path = getPathOutput(output_path)
    # Process video
    if os.path.splitext(input_path)[1].lower() in ['.mp4', '.avi', '.mkv', '.flv', '.mov', '.wmv', '.webm']:
      print("Processing video..... Please waiting")
      resizeAndRotateVideo(input_path, output_path, width, height, fps, angle, fx, fy)
      print("Done")

    # Process image
    elif os.path.splitext(input_path)[1].lower() in ['.jpg', '.png', '.jpeg', '.bmp']:
      print("Processing images..... Please waiting")
      resizeAndRotateImage(input_path, output_path, width, height, angle, fx, fy)
      print("Done")

    # Wrong format
    else:
      print("The program does not have the right format for your image or video")
  
  elif os.path.isdir(input_path):
    print("Processing list files..... Please waiting")
    processingMultiFiles(input_path, output_path, width, height, fps, angle, fx, fy)
    print("Done")
  else:
    print("Cannot open your input. Please check it again!")


def processWidthHeight(width, height, src_width = 0, src_height = 0, angle = 0, fx = 0, fy = 0):
  if width == 0 and fx == 0:
    width = src_width
  elif width == 0 and fx != 0:
    width = int(round(src_width * fx))

  if height == 0 and fy == 0:
    height = src_height
  elif height == 0 and fy != 0:
    height = int(round(src_height * fy))

  if (angle > 0 and angle <= 90) or angle > 180:
    width, height = height, width
  
  return width, height


def resizeAndRotateFrame(frame, width, height, angle = 0):
  if angle > 0 and angle <= 90:
    frame = cv2.rotate(frame,cv2.ROTATE_90_CLOCKWISE)
  elif angle > 90 and angle <= 180: 
    frame = cv2.rotate(frame,cv2.ROTATE_180)
  elif angle > 180:
    frame = cv2.rotate(frame,cv2.ROTATE_90_COUNTERCLOCKWISE)
  frame = cv2.resize(frame, (width,height), interpolation = cv2.INTER_LINEAR)
  return frame


def resizeAndRotateImage(input_path, output_path, width, height, angle = 0, fx = 0, fy = 0):
  
  image = cv2.imread(input_path)
  src_height, src_width, src_channels = image.shape
  width, height = processWidthHeight(width, height, src_width, src_height, angle, fx, fy)
  image = resizeAndRotateFrame(image, width, height, angle)

  output_folder = getPathOutput(output_path)
  changedImagePath = os.path.join(output_folder,"_".join(("process", os.path.split(input_path)[1])))
  cv2.imwrite(changedImagePath, image)


def resizeAndRotateVideo(input_path, output_path, width, height, fps, angle = 0, fx = 0, fy = 0):
  cap = cv2.VideoCapture(input_path)

  src_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
  src_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
  
  width, height = processWidthHeight(width, height, src_width, src_height, angle, fx, fy)
    
  if fps == 0:
    fps = cap.get(cv2.CAP_PROP_FPS)

  
  output_folder = getPathOutput(output_path)
  changedVideoPath = os.path.join(output_folder,"_".join(("process", os.path.split(input_path)[1])))

  fourcc = cv2.VideoWriter_fourcc(*'XVID')
  out = cv2.VideoWriter(changedVideoPath, fourcc, fps, (width,height))
  
  
  while True:
      ret, frame = cap.read()
      if ret == True:
        frame = resizeAndRotateFrame(frame, width, height, angle)
        out.write(frame)
      else:
          break
      
  cap.release()
  out.release()
  cv2.destroyAllWindows()
  
  return changedVideoPath


def processingMultiFiles(input_dir, output_dir, width, height, fps, angle = 0, fx = 0, fy = 0):
  output_dir = getPathOutput(output_dir)
  for input_path in os.listdir(input_dir):
    input_path = os.path.join(input_dir, input_path)
    # Process video
    if os.path.splitext(input_path)[1].lower() in ['.mp4', '.avi', '.mkv', '.flv', '.mov', '.wmv', '.webm']:
      output_path = os.path.join(output_dir, "processed_videos")
      if os.path.exists(output_path) == False:
        os.makedirs(output_path)

      resizeAndRotateVideo(input_path, output_path, width, height, fps, angle, fx, fy)

    # Process image
    elif os.path.splitext(input_path)[1].lower() in ['.jpg', '.png', '.jpeg', '.bmp']:
      output_path = os.path.join(output_dir, "processed_images")
      if os.path.exists(output_path) == False:
        os.makedirs(output_path)
      
      resizeAndRotateImage(input_path, output_path, width, height, angle, fx, fy)


parser = argparse.ArgumentParser(description="Program to resize and rotate video")
parser.add_argument("--input", type=str, required=True, help="Enter path of file image or video or path of folder contains images")
parser.add_argument("--output", type=str, default=os.getcwd(), help="Enter address folder to save images and videos")
parser.add_argument("--width", type=int, default = 0, help="Enter resize width")
parser.add_argument("--height", type=int, default = 0, help="Enter resize height")
parser.add_argument("--fx", type=float, default = 0, help="Enter scale factor along the horizontal axis, default = 0")
parser.add_argument("--fy", type=float, default = 0, help="Enter scale factor along the vertical axis, default = 0")
parser.add_argument("--fps",type=int, default = 0, help="Enter frame per second (FPS) for new video")
parser.add_argument("--angle", type=int, default = 0, help="Enter angle for rotate, angle = 90,180,270")
args = parser.parse_args()


input_path = os.path.abspath(args.input)
output_path = os.path.abspath(args.output)

width = args.width
height = args.height
fx = args.fx
fy = args.fy
fps = args.fps
angle = args.angle
run(input_path, output_path, width, height, fps, angle, fx, fy)