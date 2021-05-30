import datetime

from vidgear.gears import CamGear, WriteGear
import cv2
t = datetime.datetime.now()

# add various Picamera tweak parameters to dictionary
options = {
    "CAP_PROP_FRAME_WIDTH": 320,
    "CAP_PROP_FRAME_HEIGHT": 240,
    "CAP_PROP_FPS": 24,
    #"CAP_PROP_FOURCC": .fourcc('M', 'J', 'P', 'G'),
}

"""
硬解 1s内延时
ffmpeg \
-f video4linux2  \
-framerate 24 \
-s 800x600 \
-i /dev/video0 \
-pix_fmt yuv420p \
-codec:v:0 h264_v4l2m2m \
-b:v 9990684 -maxrate 9990684 -bufsize 19981368 \
-preset ultrafast \
-tune zerolatency \
-g 6 -keyint_min 6 \
-force_key_frames:0 "expr:gte(t,0+n_forced*2)" \
-vf "scale=trunc(min(max(iw\,ih*dar)\,1920)/64)*64:trunc(ow/dar/2)*2" \
-threads 4 \
-vsync -1 \
-r 25 \
-rtsp_transport tcp -f rtsp rtsp://server/
"""
# 软解 延时200ms
"""
ffmpeg  \
-f video4linux2 \
-framerate 24 \
-s 800x600 \
-i /dev/video0 \
-vcodec h264 \
-preset ultrafast \
-tune zerolatency  \
-g 6 \
-threads 4 \
-rtsp_transport tcp -f rtsp rtsp://server
"""
output_params = {
    "-framerate": 24, # fps
    "-s": "800x600",
    "-pix_fmt": "yuv420p",
    "-crf": 25, # 视频质量, 数字越大质量越差, 0为最好
    "-preset": "ultafast", # x264处理速度: fast/faster/verfast/superfast/ultrafast
    "-tune": "zerolatency", # x264固定码率 0延迟
    "-force_key_frames:0": "expr:gte(t,0+n_forced*2)",
    "-codec:v:0": "h264_v4l2m2m",
    "-vf": "scale=trunc(min(max(iw\,ih*dar)\,1920)/64)*64:trunc(ow/dar/2)*2",
    "-b:v": "9990684",
    "-maxrate": "9990684",
    "-bufsize": "19981368",
    "-vsync": -1,
    "-r": 24,
    "-g": 6, # 关键帧数
    "-threads": 4, # 线程
    "-f": "rtsp", # 目标视频格式
    "-rtsp_transport": "tcp",
}

face_cascade = cv2.CascadeClassifier("/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml")
def detect_face(frame):
    if frame.ndim == 3: # 如果img维度为3，说明不是灰度图，先转化为灰度图gray，如果不为3，也就是2，原图就是灰度图
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame

    return face_cascade.detectMultiScale(gray, 1.3, 5) # 1.3和5是特征的最小、最大检测窗口，它改变检测结果也会改变

stream = CamGear(source='/dev/video0', backend=cv2.CAP_V4L, logging=True, **options).start()
writer = WriteGear(output_filename = 'rtsp://192.168.0.100:5541/test', compression_mode = True, logging = True, **output_params)

i = 0
faces = []
while True:
    try:
        i += 1
        frame = stream.read()
        if frame is not None:
            # 半秒读取下人脸
            if i % 12 == 0:
                faces = detect_face(frame)
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 1)
            writer.write(frame)
        else:
            print("no frame")
    except KeyboardInterrupt:
        break

# safely close video stream
stream.stop()
writer.close()
print("time:", datetime.datetime.now().timestamp() - t.timestamp())

