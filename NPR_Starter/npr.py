#npr.py
import imageIO as io
#import a2
import numpy as np
import scipy as sp
from scipy import signal
from scipy import ndimage
import random as rnd
import nprHelper as helper
import math

#write-up:
#https://www.overleaf.com/read/kjcvnhzhjkjn

def inBounds(out, y, x, texture):
    ht = texture.shape[0]
    wt = texture.shape[1]
    h = out.shape[0]
    w = out.shape[1]
    return (y > ht/2 and y < h - ht/2) and (x > wt/2 and x < w - wt/2) 

def brush(out, y, x, color, texture):
    '''out: the image to draw to. y,x: where to draw in out. 
    color: the color of the stroke. texture: the texture of the stroke.'''
    ht = texture.shape[0]
    wt = texture.shape[1]
    if inBounds(out,y,x,texture):
        t = texture*color + (1-texture)*out[y-ht//2:y+(ht-ht//2), x-wt//2:x+(wt-wt//2)]
        out[y-ht//2:y+(ht-ht//2), x-wt//2:x+(wt-wt//2)] = t

def singleScalePaint(im, out, importance, texture, size=10, N=1000, noise=0.3):
    '''Paints with all brushed at the same scale using importance sampling.'''
    h = out.shape[0]
    w = out.shape[1]

    a = np.max(texture.shape)

    #scale texture image to size
    textscale = helper.scaleImage(texture, size/a)
    ht = textscale.shape[0]
    wt = textscale.shape[1]
    
    #splat brush for N random y, x 
    b = 0 #number of brush strokes
    while b < N:
        y=int(rnd.random()*(h-ht)*0.9999+ht/2)
        x=int(rnd.random()*(w-wt)*0.9999+wt/2)

        reject = rnd.random()
        if inBounds(out, int(y), int(x), textscale):
            if reject <= importance[y,x,0]:
                col = (1-noise/2+noise*np.random.rand(3))*im[y,x]
                brush(out, int(y), int(x), col, textscale)
                b += 1


def painterly(im, texture, N=10000, size=50, noise=0.3):
    '''First paints at a coarse scale using all 1's for importance sampling, 
    then paints again at size/4 scale using the sharpness map for importance sampling.'''
    #first pass: brush size: size, importance = 1
    out = np.zeros_like(im)
    importance = np.ones_like(im)
    singleScalePaint(im, out, importance, texture, size, N, noise)

    #second pass: brush size: size/4, importance = sharpness
    sharpness = helper.sharpnessMap(im)
    singleScalePaint(im, out, sharpness, texture, size//4, N, noise)
    return out


def computeAngles(im):
    '''Return an image that holds the angle of the smallest eigenvector of the structure tensor at each pixel. 
    If you have a 3 channel image as input, just set all three channels to be the same value theta.'''
    tensor = helper.computeTensor(im)
    out = np.zeros_like(tensor)
    for y in range(tensor.shape[0]):
        for x in range(tensor.shape[1]):
            if tensor.shape[2] == 3:
                a = np.array([[tensor[y,x,0], tensor[y,x,1]], [tensor[y,x,1], tensor[y,x,2]]])
                eig = np.linalg.eigh(a)
                eigval = eig[0]
                ind = np.argmin(eigval)
                eigvec = eig[1]
                theta = np.arctan2(eigvec[:,ind][1], eigvec[:,ind][0]) 
                if theta < 0:
                    theta += 2*np.pi
                for z in range(tensor.shape[2]):
                    out[y,x,z] = theta    
    return out

def singleScaleOrientedPaint(im, out, thetas, importance, texture, size, N, noise, nAngles=36):
    '''same as single scale paint but now the brush strokes will be oriented according to the angles in thetas.'''
    h = out.shape[0]
    w = out.shape[1]

    a = np.max(texture.shape)

    #scale texture image to size
    textscale = helper.scaleImage(texture, size/a)
    ht = textscale.shape[0]
    wt = textscale.shape[1]

    #splat brush for N random y, x 
    b = 0 #number of brush strokes
    while b < N:
        y=int(rnd.random()*(h-ht)*0.9999+ht/2)
        x=int(rnd.random()*(w-wt)*0.9999+wt/2)

        reject = rnd.random()
        if inBounds(out, int(y), int(x), textscale):
            if reject <= importance[y,x,0]:
                col = (1-noise/2+noise*np.random.rand(3))*im[y,x]

                #compute rotated brushes
                rotated = helper.rotateBrushes(textscale, nAngles)
                theta = thetas[int(y), int(x), 0]
                ind = int((theta*nAngles)/(2*math.pi))
                brush(out, int(y), int(x), col, rotated[ind])
                b += 1

def orientedPaint(im, texture, N=7000, size=50, noise=0.3):
    '''same as painterly but computes and uses the local orientation information to orient strokes.'''
    #compute angles
    thetas = computeAngles(im)

    #first pass: brush size: size, importance = 1
    out = np.zeros_like(im)
    importance = np.ones_like(im)
    singleScaleOrientedPaint(im, out, thetas, importance, texture, size, N, noise)

    #second pass: brush size: size/4, importance = sharpness
    sharpness = helper.sharpnessMap(im)
    singleScaleOrientedPaint(im, out, thetas, sharpness, texture, size//4, N, noise)
    return out