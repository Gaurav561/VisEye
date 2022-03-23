from flask import Flask, render_template, Response

import mmap
import time

import cv2
import numpy as np


# def gen_frames():  
#     shape = (720, 1280, 3)
#     n = np.prod(shape)
#     mm = mmap.mmap(-1, n, "IMG")
#     while True:
#         # read image
#         start = time.perf_counter()
#         mm.seek(0)
#         buf = mm.read(n)
#         img = np.frombuffer(buf, dtype=np.uint8).reshape(shape)
#         stop = time.perf_counter()
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield (b'--frame\r\n'
#                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 

#         print("Reading Duration:", (stop - start) * 1000, "ms")
#         cv2.imshow("img", img)
#         key = cv2.waitKey(1) & 0xFF
#         key = chr(key)
#         if key.lower() == "q":
#             break
#     cv2.destroyAllWindows()
#     mm.close()
      

def gen_frames():
    cap = cv2.VideoCapture(0)
########################################################
    shape = (768,1024, 3)
    n = np.prod(shape)
    mm = mmap.mmap(-1, n, "IMG_NP",access=mmap.ACCESS_READ)
    while True:
        # read image
        start = time.perf_counter()
        mm.seek(0)
        buf = mm.read(n)
        frame = np.frombuffer(buf, dtype=np.uint8).reshape(shape)
        stop = time.perf_counter()

        print("Reading Duration:", (stop - start) * 1000, "ms")

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
########################################################
    # while True:
    #     _,frame = cap.read()

    #     ret, buffer = cv2.imencode('.jpg', frame)
    #     frame = buffer.tobytes()
    #     yield (b'--frame\r\n'
    #             b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('test.html')


@app.route("/video")
def home():
    # shape = (720, 1280, 3)
    # n = np.prod(shape)
    # mm = mmap.mmap(-1, n, "IMG")
    # while True:
    #     # read image
    #     start = time.perf_counter()
    #     mm.seek(0)
    #     buf = mm.read(n)
    #     img = np.frombuffer(buf, dtype=np.uint8).reshape(shape)
    #     stop = time.perf_counter()

    #     print("Reading Duration:", (stop - start) * 1000, "ms")
    #     cv2.imshow("img", img)
    #     key = cv2.waitKey(1) & 0xFF
    #     key = chr(key)
    #     if key.lower() == "q":
    #         break
    # cv2.destroyAllWindows()
    # mm.close()
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    


if __name__ == "__main__":
    app.run(debug=True)