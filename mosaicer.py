import cv2
import numpy as nu
import binary_convert
import compare
import os
import sys
import tensorflow as tf
import config

FLAGS = tf.app.flags.FLAGS

def mosaic(video_path,train_dir, label):
    data=video_path
    video_dir,filename=os.path.split(video_path)
    result_dir= os.path.join(video_dir,'result')
    if not os.path.exists(result_dir):
        os.makedirs(result_dir)

    cap = cv2.VideoCapture(data)
    fps = 20.0
    width = int(cap.get(3))
    height = int(cap.get(4))
    foc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(os.path.join(result_dir,filename), foc, fps, (width, height))

    cascade = cv2.CascadeClassifier("opencv/haarcascade_frontalface_alt.xml")
    #cap.isOpened()
    #for num in range(1,10):
    while(cap.isOpened()):
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = cascade.detectMultiScale(gray, scaleFactor = 1.1, minNeighbors = 3, minSize = (40, 40), flags = 0)

        for (x,y,w,h) in faces:
            imgFace = frame[y:y+h, x:x+w]
            img_yuv = cv2.cvtColor(imgFace, cv2.COLOR_BGR2YUV)

            # equalize the histogram of the Y channel
            img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

            # convert the YUV image back to RGB format
            img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
            img_output2 = cv2.resize(img_output,(32,32),interpolation = cv2.INTER_AREA)
            cv2.imwrite("image/test_data.jpg", img_output2)

            if test_db(train_dir=train_dir, label=label):
                avg_r = 0
                avg_g = 0
                avg_b = 0

                temp = w % 30
                if temp != 0:
                  w = w + (30-temp)
                  temp = h % 30
                  if temp != 0:
                    h = h + (30-temp)
                  tx = w / 30
                  ty = h / 30

                  for time_x in range(0,tx):
                      for time_y in range(0,ty):
                          for m in range(0,30):
                              for n in range(0,30):
                                  if time_y*30+y+m < height:
                                      if time_x*30+x+n < width:
                                          if time_y*30+y+m > 0:
                                              if time_x*30+x+n > 0:
                                                  avg_r = avg_r + frame[time_y*30+y+m,time_x*30+x+n,2]
                                                  avg_g = avg_g + frame[time_y*30+y+m,time_x*30+x+n,1]
                                                  avg_b = avg_b + frame[time_y*30+y+m,time_x*30+x+n,0]
                          avg_r = avg_r / 900
                          avg_g = avg_g / 900
                          avg_b = avg_b / 900

                          for m in range(0,30):
                              for n in range(0,30):
                                  if time_y*30+y+m < height:
                                      if time_x*30+x+n < width:
                                          if time_y*30+y+m > 0:
                                              if time_x*30+x+n > 0:
                                                  frame[time_y*30+y+m,time_x*30+x+n,2] = avg_r
                                                  frame[time_y*30+y+m,time_x*30+x+n,1] = avg_g
                                                  frame[time_y*30+y+m,time_x*30+x+n,0] = avg_b

        out.write(frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    return 'finish'

def test_db(train_dir, label):
    threshold=0.6
    output=binary_convert.convert("image/test_data.jpg")
    precision=compare.evaluate(output,train_dir)
    #print(precision[0],precision[1])
    if precision[label] > threshold :
      return True
    else :
      return False

if __name__ == "__main__":
    video_path=os.path.join(FLAGS.video_path,sys.argv[1])
    mosaic(video_path=video_path,train_dir=FLAGS.train_dir, label=FLAGS.mosaic_label)
