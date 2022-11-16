import os, sys
import cv2
import glob
import time
from illumination_boost_lut import *
from threading import Semaphore, Thread

# Chosen font
font = cv2.FONT_HERSHEY_SIMPLEX

# Lambda parameter
_lambda = 2

MAX_BUFFERED_FRAMES = 4
MAX_PROCESSING_THREADS = 10

# Exit flag
Exit = False

# Use original
use_original = False

# Use lut
use_lut = True

# Threads
camera_thread = None
processing_threads = None
show_result_thread = None

new_frames = list()
processed_frames = list()

def process_frame(img):
    global _lambda
    prev_proc_frame_time = time.time()
    out = illumination_boost(img, _lambda, use_lut=use_lut)
    new_proc_frame_time = time.time()
    processing_time = str(int(1000*(new_proc_frame_time - prev_proc_frame_time))) + ' ms'
    return (out, processing_time)

 
def show_result(img, out, fps, fps_2, processing_time):
    # result = cv2.hconcat([img, out])
    if use_original:
        result = img
    else:
        result = out

    # putting the FPS count on the original image
    # cv2.putText(result, fps, (7, 20), font, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

    # putting the FPS count on the full image
    # cv2.putText(result, fps_2, (7, 50), font, 0.5, (100, 255, 0), 1, cv2.LINE_AA)

    # putting the processing time on the out image
    cv2.putText(result, processing_time, (7, 20), font, 0.5, (255, 100, 0), 1, cv2.LINE_AA)

    cv2.imshow('Original image and Boosted', result)

def processing_func():
    global Exit, new_frames, processed_frames
    while not Exit:

        try:
            img, fps = new_frames.pop(0)
            if img is not None:
                out, processing_time = process_frame(img)
                processed_frames.append((img, out, fps, processing_time))
        except IndexError:
            time.sleep(0.001)

def show_result_func():
    global Exit, processed_frames, use_original, use_lut
    prev_frame_time = 0
    while not Exit:
        try:
            img, out, fps, processing_time = processed_frames.pop(0)
            new_frame_time = time.time()
            
            fps_2 = 1/max(new_frame_time-prev_frame_time,0.00001)
            prev_frame_time = new_frame_time
            fps_2 = str(int(fps_2)) + ' fps'
            if (img is not None) and (out is not None) and (fps is not None) and (processing_time is not None):
                show_result(img, out, fps, fps_2, processing_time)
        except IndexError:
            time.sleep(0.001)
        finally:
            ret = cv2.waitKey(1)
            if  ret == ord('q'):
                Exit = True
                break
            elif ret == ord('d'):
                use_original = not use_original
            elif ret == ord('a'):
                use_lut = not use_lut

def camera_func(vc):
    prev_frame_time = 0
    global Exit, new_frames, MAX_BUFFERED_FRAMES
    while not Exit:
        ret, img = vc.read()
        new_frame_time = time.time()

        fps = 1/max(new_frame_time-prev_frame_time,0.00001)
        prev_frame_time = new_frame_time
        fps = str(int(fps)) + ' fps'

        while len(new_frames) == MAX_BUFFERED_FRAMES and not Exit:
            time.sleep(0.1)
        new_frames.append((img, fps))

def start_camera_thread(vc):
    global camera_thread
    camera_thread = Thread(None, camera_func, 'camera_func', [vc])
    camera_thread.start()

def start_processing_thread():
    global processing_thread
    processing_thread = Thread(None, processing_func, 'processing_func')
    processing_thread.start()

def start_processing_threads():
    global processing_threads
    processing_threads = list()
    for i in range(0,MAX_PROCESSING_THREADS):
        thread = Thread(None, processing_func, 'processing_func')
        thread.start()
        processing_threads.append(thread)

def start_show_result_thread():
    global show_result_thread
    show_result_thread = Thread(None, show_result_func, 'show_result_func')
    show_result_thread.start()

def start_threads(vc):
    start_camera_thread(vc)
    start_processing_threads()
    start_show_result_thread()

def join_threads():
    global camera_thread, processing_thread, show_result_thread, processing_threads
    camera_thread.join()
    [t.join() for t in processing_threads]
    show_result_thread.join()


def main():
    # Capturing video from file
    vc = cv2.VideoCapture('video.mp4')
    # vc = cv2.VideoCapture(0)
    start_threads(vc)
    join_threads()
    vc.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()