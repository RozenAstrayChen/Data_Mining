import cv2
import numpy as np
from PIL import Image, ImageStat

def Read_JPG(filename):
    '''

    :param filename:  file path
    :return: matrix of RGB which type is numpy
    '''
    # be ware cv2 is read bgr
    img = Image.open(filename)

    return img

file_path = '/Users/Rozen_mac/code/mining/K_means/sample.jpg'
img = Read_JPG(file_path)
