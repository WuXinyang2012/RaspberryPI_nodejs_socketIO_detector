#!/usr/bin/env python3
from socketIO_client_nexus import SocketIO, LoggingNamespace
import warnings
import os, time
from mvnc import mvncapi as mvnc
import numpy
import cv2
import os, sys
import json
import picamera
import picamera.array

warnings.simplefilter("ignore", DeprecationWarning)

#define some global variables and load necessary data
# Load graph
path_to_networks = './Inception-v3/'
#path_to_images = dir
graph_filename = 'graph'
with open(path_to_networks + graph_filename, mode='rb') as f:
    graphfile = f.read()

# Load categories
categories = []
with open(path_to_networks + 'categories.txt', 'r') as f:
    for line in f:
        cat = line.split('\n')[0]
        if cat != 'classes':
            categories.append(cat)
    f.close()
    #print('Number of categories:', len(categories))

# Load dict
dict = []
with open(path_to_networks + 'dict.txt', 'r') as f:
    for line in f:
        cat = line.split('\n')[0]
        dict.append(cat)
    f.close()
    #print('Number of categories:', len(dict))

#Load inputsize
with open(path_to_networks + 'inputsize.txt', 'r') as f:
    reqsize = int(f.readline().split('\n')[0])

# Load preprocessing data
mean = 128
std = 1 / 128

devices = mvnc.EnumerateDevices()
global camera

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError

def on_connect():
    print('connect')

def on_disconnect():
    print('disconnect')

def on_reconnect():
    print('reconnect')


def load_devices():
    global devices
    global device
    global graphfile
    global graph
    global camera
    if len(devices) == 0:
        print('No devices found')
        quit()
    device = mvnc.Device(devices[0])
    device.OpenDevice()
    graph = device.AllocateGraph(graphfile)
    print('NCS device was opened.')
    #socketIO.emit('event_B')
    socketIO.emit('new message', 'NCS device was opened.')
    camera = picamera.PiCamera()
    camera.rotation = 180

def Capture():
    stream = picamera.array.PiRGBArray(camera)
    camera.capture(stream, format = 'bgr')
    frame = stream.array
    return frame

def ImageRead():
    return cv2.imread("./test3.jpg")

def infer():
    global graph
    image = Capture()
    img = numpy.array(image).astype(numpy.float32)
    dx, dy, dz = img.shape
    delta = float(abs(dy - dx))
    if dx > dy:  # crop the x dimension
        img = img[int(0.5 * delta):dx - int(0.5 * delta), 0:dy]
    else:
        img = img[0:dx, int(0.5 * delta):dy - int(0.5 * delta)]
    img = cv2.resize(img, (reqsize, reqsize))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    for i in range(3):
        img[:, :, i] = (img[:, :, i] - mean) * std
    graph.LoadTensor(img.astype(numpy.float16), 'user object')
    output, userobj = graph.GetResult()
    top_inds = output.argsort()[::-1][:5]
    #print(''.join(['*' for i in range(79)]))
    result = []
    for i in range(5):
        if output[top_inds[i]] <= 0.001 or categories[top_inds[i]] not in dict:
            break
        # print(top_inds[i], categories[top_inds[i]], output[top_inds[i]])
        print(categories[top_inds[i]])
        result.append(categories[top_inds[i]])
    socketIO.emit('new message', result)
    #print(''.join(['*' for i in range(79)]))

def exit():
    global device
    global camera
    camera.close()
    device.CloseDevice()
    print("NCS device is closed.")
    socketIO.emit('new message', "NCS device is closed.")




socketIO = SocketIO('localhost', 3000, LoggingNamespace)
socketIO.on('connect', on_connect)
socketIO.on('disconnect', on_disconnect)
socketIO.on('reconnect', on_reconnect)


while(1):

    socketIO.on('start', load_devices)
    # Listen
    socketIO.on('infer', infer)
    socketIO.wait(seconds=1)

    # Stop listening
    #socketIO.off('infer')
    #socketIO.emit('event_B')
    #socketIO.wait(seconds=1)

    # Listen only once
    socketIO.on('exit', exit)
    socketIO.wait(seconds=1)
