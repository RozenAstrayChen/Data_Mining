
from PIL import Image

def Read_JPG(filename):
    '''

    :param filename:  file path
    :return: matrix of RGB which type is numpy
    '''
    # read image to gray scale
    img = Image.open(filename)#.convert('L')
    img = img.resize((80, 80))

    return img

file_path = '/Users/Rozen_mac/code/mining/K_means/sample.jpg'
img = Read_JPG(file_path)
