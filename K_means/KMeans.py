from PIL import Image, ImageStat
import ReadFile as R
import math
import random
import numpy as np
import matplotlib.pyplot as plt


class Kmeans():
    def __init__(self, img, k=2):
        self.k = k
        self.img = img
        self.img_width, self.img_height = img.size

    def getMin(self, pixel, centroids):
        '''
        :param pixel: R, G, B values
        :param centroids:
        :return: classification index
        '''
        ds = []
        for i in range(0, len(centroids)):
            d = np.sqrt(int((centroids[i][0] - pixel[0])) ** 2 + int((centroids[i][1] - pixel[1])) ** 2 + int(
                (centroids[i][2] - pixel[2])) ** 2)
            ds.append(d)

        return ds.index(min(ds))

    def assignPixels(self, centroids):
        clusters = {}

        for x in range(self.img_width):
            for y in range(self.img_height):
                p = self.px[x, y] # RGB values
                minIndex = self.getMin(self.px[x, y], centroids)

                try:
                    clusters[minIndex].append(p)
                except KeyError:
                    clusters[minIndex] = [p]

        return clusters

    def adjustCentroids(selfs, clusters):
        new_centroids = []
        keys = sorted(clusters.keys())

        for k in keys:
            n = np.mean(clusters[k], axis=0)
            new = (int(n[0]), int(n[1]), int(n[2]))
            print(str(k) + ": " + str(new))
            new_centroids.append(new)

        return new_centroids


    def fit(self):
        centroids = []
        old_centroids = []
        self.px = self.img.load()
        rgb_range = ImageStat.Stat(self.img).extrema
        # (0~255)*3

        # init k of centroids for the clustering
        for k in range(self.k):
            # init random centroids
            centroid = px[np.random.randint(0, self.img_width), np.random.randint(0, self.img_height)]
            centroids.append(centroid)

        print("init centroids ", centroids)

        old_centroids = centroids
        clusters = self.assignPixels(centroids)
        centroids = self.adjustCentroids(clusters)

        print("===========================================")
        print("Convergence Reached!")
        print(centroids)
        return centroids

    def drawWindows(self, centroids):
        img = Image.new('RGB', (self.img_width, self.img_height), "white")
        p = img.load()

        for x in range(img.size[0]):
            for y in range(img.size[1]):
                RGB_value = centroids[self.getMin(px[x, y], centroids)]
                p[x, y] = RGB_value

        img.show()



file_path = '/Users/Rozen_mac/code/mining/K_means/sample.jpg'
img = R.Read_JPG(file_path)
px = img.load()
k = Kmeans(img, k=3)
reslut = k.fit()
k.drawWindows(reslut)