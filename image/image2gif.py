# https://gist.github.com/jonschoning/7216290

#   This file is part of VISVIS. This file may be distributed 
#   seperately, but under the same license as VISVIS (LGPL).
#    
#   images2gif is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Lesser General Public License as 
#   published by the Free Software Foundation, either version 3 of 
#   the License, or (at your option) any later version.
# 
#   images2gif is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Lesser General Public License for more details.
# 
#   You should have received a copy of the GNU Lesser General Public 
#   License along with this program.  If not, see 
#   <http://www.gnu.org/licenses/>.
#
#   Copyright (C) 2009 Almar Klein

""" Module images2gif

Provides functionality for reading and writing animated GIF images.
Use writeGif to write a series of numpy arrays or PIL images as an 
animated GIF. Use readGif to read an animated gif as a series of numpy
arrays.

Many thanks to Ant1 for:
* noting the use of "palette=PIL.Image.ADAPTIVE", which significantly
  improves the results. 
* the modifications to save each image with its own palette, or optionally
  the global palette (if its the same).

- based on gifmaker (in the scripts folder of the source distribution of PIL)
- based on gif file structure as provided by wikipedia

"""
from __future__ import print_function

try:
    import PIL
    from PIL import Image, ImageChops
    from PIL.GifImagePlugin import getheader, getdata
except ImportError:
    PIL = None

try:
    import numpy as np
except ImportError:
    np = None    

# getheader gives a 87a header and a color palette (two elements in a list).
# getdata()[0] gives the Image Descriptor up to (including) "LZW min code size".
# getdatas()[1:] is the image data itself in chuncks of 256 bytes (well
# technically the first byte says how many bytes follow, after which that
# amount (max 255) follows).


def intToBin(i):
    """ Integer to two bytes """
    # devide in two parts (bytes)
    i1 = i % 256
    i2 = int( i/256)
    # make string (little endian)
    return chr(i1) + chr(i2)


def getheaderAnim(im):
    """ Animation header. To replace the getheader()[0] """
    bb = "GIF89a"
    bb += intToBin(im.size[0])
    bb += intToBin(im.size[1])
    bb += "\x87\x00\x00"
    return bb


def getImageDescriptor(im):
    """ Used for the local color table properties per image.
    Otherwise global color table applies to all frames irrespective of
    wether additional colours comes in play that require a redefined palette
    Still a maximum of 256 color per frame, obviously.
    
    Written by Ant1 on 2010-08-22
    """
    bb = '\x2C' # Image separator,
    bb += intToBin( 0 ) # Left position
    bb += intToBin( 0 ) # Top position
    bb += intToBin( im.size[0] ) # image width
    bb += intToBin( im.size[1] ) # image height
    bb += '\x87' # packed field : local color table flag1, interlace0, sorted table0, reserved00, lct size111=7=2^(7+1)=256.
    # LZW minimum size code now comes later, begining of [image data] blocks
    return bb


def getAppExt(loops=float('inf')):
    """ Application extention. Part that specifies amount of loops. 
    If loops is inf, it goes on infinitely.
    """
    if loops == 0:
        bb = "" # application extension should not be used
                # (the extension interprets zero loops
                # to mean an infinite number of loops)
    else:
        bb = "\x21\xFF\x0B"  # application extension
        bb += "NETSCAPE2.0"
        bb += "\x03\x01"
        if loops == float('inf'):
            loops = 2**16-1
        bb += intToBin(loops)
        bb += '\x00'  # end
    return bb


def getGraphicsControlExt(duration=0.1):
    """ Graphics Control Extension. A sort of header at the start of
    each image. Specifies transparancy and duration. """
    bb = '\x21\xF9\x04'
    bb += '\x08'  # no transparancy
    bb += intToBin( int(duration*100) ) # in 100th of seconds
    bb += '\x00'  # no transparant color
    bb += '\x00'  # end
    return bb


def _writeGifToFile(fp, images, durations, loops):
    """ Given a set of images writes the bytes to the specified stream.
    """
    
    # Obtain palette for all images and count each occurance
    palettes, occur = [], []
    for im in images: 
        palettes.append( getheader(im)[1] )
    for palette in palettes: 
        occur.append( palettes.count( palette ) )
    
    # Select most-used palette as the global one (or first in case no max)
    globalPalette = palettes[ occur.index(max(occur)) ]
    
    # Init
    frames = 0
    firstFrame = True
    
    
    for im, palette in zip(images, palettes):
        
        if firstFrame:
            # Write header
            
            # Gather info
            header = getheaderAnim(im)
            appext = getAppExt(loops)
            
            # Write
            fp.write(header)
            fp.write(globalPalette)
            fp.write(appext)
            
            # Next frame is not the first
            firstFrame = False
        
        if True:
            # Write palette and image data
            
            # Gather info
            data = getdata(im) 
            imdes, data = data[0], data[1:]       
            graphext = getGraphicsControlExt(durations[frames])
            # Make image descriptor suitable for using 256 local color palette
            lid = getImageDescriptor(im) 
            
            # Write local header
            if palette != globalPalette:
                # Use local color palette
                fp.write(graphext)
                fp.write(lid) # write suitable image descriptor
                fp.write(palette) # write local color table
                fp.write('\x08') # LZW minimum size code
            else:
                # Use global color palette
                fp.write(graphext)
                fp.write(imdes) # write suitable image descriptor
            
            # Write image data
            for d in data:
                fp.write(d)
        
        # Prepare for next round
        frames = frames + 1
    
    fp.write(";")  # end gif
    return frames


## Exposed functions 

def writeGif(filename, images, duration=0.1, loops=0, dither=1):
    """ writeGif(filename, images, duration=0.1, loops=0, dither=1)
    Write an animated gif from the specified images. 
    images should be a list of numpy arrays of PIL images.
    Numpy images of type float should have pixels between 0 and 1.
    Numpy images of other types are expected to have values between 0 and 255.
    """
    
    if PIL is None:
        raise RuntimeError("Need PIL to write animated gif files.")
    
    AD = Image.ADAPTIVE
    images2 = []
    
    # convert to PIL
    for im in images:
        
        if isinstance(im,Image.Image):
            images2.append( im.convert('P', palette=AD, dither=dither) )
            
        elif np and isinstance(im, np.ndarray):
            if im.dtype == np.uint8:
                pass
            elif im.dtype in [np.float32, np.float64]:
                im = (im*255).astype(np.uint8)
            else:
                im = im.astype(np.uint8)
            # convert
            if len(im.shape)==3 and im.shape[2]==3:
                im = Image.fromarray(im,'RGB').convert('P', palette=AD, dither=dither)
            elif len(im.shape)==2:
                im = Image.fromarray(im,'L').convert('P', palette=AD, dither=dither)
            else:
                raise ValueError("Array has invalid shape to be an image.")
            images2.append(im)
            
        else:
            raise ValueError("Unknown image type.")
    
    # check duration
    if hasattr(duration, '__len__'):
        if len(duration) == len(images2):
            durations = [d for d in duration]
        else:
            raise ValueError("len(duration) doesn't match amount of images.")
    else:
        durations = [duration for im in images2]
        
    
    # open file
    fp = open(filename, 'wb')
    
    # write
    try:
        n = _writeGifToFile(fp, images2, durations, loops)
        print(n, 'frames written')
    finally:
        fp.close()
    

def readGif(filename):
    """ 
    """
    
    # Check PIL
    if PIL is None:
        raise RuntimeError("Need PIL to read animated gif files.")
    
    # Check whether it exists
    if not os.path.isfile(filename):
        raise IOError('File not found: '+str(filename))
    
    # Load file using PIL
    pilIm = PIL.Image.open(filename)    
    pilIm.seek(0)
    
    # Read all images inside
    ims = []
    try:
        while True:
            # Get image as numpy array
            tmp = pilIm.convert() # Make without palette
            a = np.asarray(tmp)
            if len(a.shape)==0:
                raise MemoryError("Too little memory to convert PIL image to array")
            # Store, and next
            ims.append(a)
            pilIm.seek(pilIm.tell()+1)
    except EOFError:
        pass
    
    # Done
    return ims


if __name__ == '__main__':
    im = np.zeros((200,200), dtype=np.uint8)
    im[10:30,:] = 100
    im[:,80:120] = 255
    im[-50:-40,:] = 50
    
    images = [im*1.0, im*0.8, im*0.6, im*0.4, im*0]
    writeGif('lala3.gif',images, duration=0.5, dither=0)