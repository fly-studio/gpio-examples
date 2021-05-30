import cv2


def detectFaces(image_name):
    img = cv2.imread(image_name)
    face_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img #if语句：如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图

    faces = face_cascade.detectMultiScale(gray, 1.1, 3)#1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

    cv2.imwrite('/codes/python/examples/face/drawfaces.jpg', img)

detectFaces("/root/Ultra-Light-Fast-Generic-Face-Detector-1MB/MNN/build/55.jpg")
