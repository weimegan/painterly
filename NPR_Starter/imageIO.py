import png
import numpy

baseInputPath='Input/'
baseOutputPath='Output/'

def imread(path='in.png', gamma=2.2):
    '''reads a PNG RGB image at baseInputPath+path and return a numpy array organized along Y, X, channel.
    The values are encoded as float and are linearized (i.e. gamma is decoded)'''
    global baseInputPath
    reader=png.Reader(baseInputPath+path)
    im=reader.asFloat()
    a=numpy.vstack(im[2])
    if im[3]['greyscale']:
        raise NameError( 'Expected an RGB image, given a greyscale one')        
    x, y=im[0], im[1]
    a.resize(y, x, 3)
    a**=gamma
    return a

def imreadGrey(path='raw.png'):
    '''reads a PNG greyscale image at baseInputPath+path and return a numpy array organized along Y, X.
    The values are encoded as float and are assumed to be linear in the input file (gamma is NOT decoded)'''
    global baseInputPath    
    reader=png.Reader(baseInputPath+path)
    im=reader.asFloat()
    a=numpy.vstack(im[2])
    if not im[3]['greyscale']:
        raise NameError( 'Expected a greyscale image, given an RGB one')
    x, y=im[0], im[1]
    a.resize(y, x)
    return a

##added by Abe, this function reads the image whether it is grey or rgb
def getImage(path='raw.png', gamma=2.2):
    '''reads a PNG image at baseInputPath+path and return a numpy array organized along Y, X.
        The values are encoded as float and are linearized (i.e. gamma is decoded)'''
    global baseInputPath
    reader=png.Reader(baseInputPath+path)
    im=reader.asFloat()
    a=numpy.vstack(im[2])
    if im[3]['greyscale']:
        x, y=im[0], im[1]
        a.resize(y, x)
    else:
        x, y=im[0], im[1]
        a.resize(y, x, 3)
    a**=gamma
    return a
##

def imwrite(im, path='out.png' ,gamma=2.2):
    '''takes a 3D numpy array organized along Y, X, channel and writes it to a PNG file.
    The values are assumed to be linear between 0 and 1 and are gamma encoded before writing.'''
    global baseOutputPath
    y,x=im.shape[0], im.shape[1]
    im=numpy.clip(im, 0, 1)
    im=im.reshape(y, x*3)
    writer = png.Writer(x,y)
    f=open(baseOutputPath+path, 'wb')
    writer.write(f, 255*(im**(1/gamma)))
    f.close()
    im.resize(y, x, 3)

seqCount=0
def imwriteSeq(im, path='out'):
    global seqCount
    path=path+str(seqCount)+'.png'
    imwrite(im, path)
    seqCount+=1


def imwriteGrey(im, path='raw.png'):
    '''takes a 2D numpy array organized along Y, X and writes it to a PNG file.
    The values are assumed to be linear between 0 and 1 and are NOT gamma encoded before writing.'''
    global baseOutputPath
    print(im)
    print(im.shape)
    y,x=im.shape[0], im.shape[1]
    im2=numpy.clip(im, 0, 1)
    writer = png.Writer(x,y,greyscale=True)
    f=open(baseOutputPath+path, 'wb')
    writer.write(f, im2*255)
    f.close()

def constantIm(y, x, color=0):
    out = numpy.empty([y, x, 3])
    out[:, :]=color
    return out
    
def emptyIm(im):
    return numpy.empty([numpy.shape(im)[0], numpy.shape(im)[1], 3])

