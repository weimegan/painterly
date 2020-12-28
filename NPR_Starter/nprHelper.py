import imageIO
from imageIO import *
#import a2
#from a2 import *
import numpy as np

import scipy
from scipy import signal
from scipy import ndimage
#import a7help
#reload(a7help)
#from a7help import *
import random as rnd
import math

#Helpful functions for you to use at your own risk! They are probably correct for the most part though...

Sobel=np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])

def imageFrom1Channel(a):
    out=np.empty([a.shape[0], a.shape[1], 3])
    for i in range(3):
        out[:, :,i]=a
    return out

def sharpnessMap(im, sigma=1):
    L=np.dot(im, np.array([0.3, 0.6, 0.1]))
    blur=ndimage.filters.gaussian_filter(L, sigma)
    high=L-blur
    energy=high*high
    sharpness=ndimage.filters.gaussian_filter(energy, 4*sigma)
    sharpness/=max(sharpness.flatten())
    return imageFrom1Channel(sharpness)

def computeTensor(im, sigmaG=1, factor=4, debug=False):
    L=np.dot(im, np.array([0.3, 0.6, 0.1]))
    L=L**0.5
    L=ndimage.filters.gaussian_filter(L, sigmaG)
    gx=signal.convolve(L, Sobel, mode='same')
    gy=signal.convolve(L, Sobel.T, mode='same')

    h, w=im.shape[0], im.shape[1]
    
    gx[:, 0:2]=0
    gy[0:2, :]=0
    gx[:, w-2:w]=0
    gy[h-2:h, :]=0

    out = np.empty([L.shape[0], L.shape[1], 2, 2])
    
    out[:, :, 0, 0]=gy*gy
    out[:, :, 0, 1]=gy*gx
    out[:, :, 1, 0]=gy*gx
    out[:, :, 1, 1]=gx*gx

    out=ndimage.filters.gaussian_filter(out, [sigmaG*factor, sigmaG*factor, 0, 0])
    return out

def eigenVec(triplet):
    y,x =1.0, 0.0
    def ap(y, x):
        return triplet[0]*y+triplet[1]*x, triplet[1]*y+triplet[2]*x
    for i in range(20):
        y, x=ap(y, x)
        r=math.sqrt(y*y+x*x)
        y/=r
        x/=r
    return y, x
    

def scaleImage(im, k):
    h, w=int(im.shape[0]*k), int(im.shape[1]*k)
    out = constantIm(h, w, 0.0)
    coord=np.mgrid[0:h, 0:w]*1.0/k
    for i in range(3):
        out[:,:,i]=ndimage.map_coordinates(im[:, :, i], coord, mode='nearest', order=3)
    return out

def rotateImage(im, theta):
    h, w=int(im.shape[0]), int(im.shape[1])
    out = np.empty_like(im)
    coord=np.mgrid[0:h, 0:w]*1.0
    ct, st=np.cos(theta), np.sin(theta)
    coord2=np.empty_like(coord)

    coord[0]-=h/2
    coord[1]-=w/2
    coord2[0]=st*coord[1]+ct*coord[0]+h/2
    coord2[1]=ct*coord[1]-st*coord[0]+w/2
    for i in range(3):
        out[:,:,i]=ndimage.map_coordinates(im[:, :, i], coord2, mode='nearest', order=3)
    return out

def rotateBrushes(texture, n):
    L=[]
    for i in range(n):
        theta=2*math.pi/n*i
        tmp=rotateImage(texture, -theta)
        L.append(tmp)
    return L

def BW(im, weights=[0.3,0.6,0.1]):
    img = im.copy()
    img = np.dot(img,weights)
    return img

def gfilter3(im, sigma):
  im_out=im.copy()
  im_out[:,:,0]=ndimage.filters.gaussian_filter(im_out[:,:,0], sigma)
  im_out[:,:,1]=ndimage.filters.gaussian_filter(im_out[:,:,1], sigma)
  im_out[:,:,2]=ndimage.filters.gaussian_filter(im_out[:,:,2], sigma)
  return im_out

def computeTensor(im, sigmaG=1, factorSigma=4):
  # rgb to lumin
  l=ndimage.filters.gaussian_filter(BW(im), sigmaG) 


  # Compute Ix^2, Iy^2, IxIy
  Sobel=np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
  im_x=ndimage.filters.convolve(l, Sobel, mode='reflect')
  im_y=ndimage.filters.convolve(l, Sobel.transpose(), mode='reflect')

  # Pack components
  im_out=np.dstack([im_x**2, im_x*im_y, im_y**2])
  im_out=gfilter3(im_out, sigmaG*factorSigma)
  return im_out


