import os.path
import re
import colorsys
import Image, ImageDraw

import config


# datapoints ( value , hue ) for different maps
mappings= {
        'no2': [ [2.5, 208], [7.5, 180], [12.5, 100], [17.5, 80], [22.5, 60], [27.5, 51], [32.5, 40], [37.5, 0], [42.5, 286] ],
        'o3': [ [50, 180], [150, 80], [250, 60], [350, 40], [450, 0], [550, 286] ],
        'pm10': [ [2.5, 208], [7.5, 180], [12.5, 80], [17.5, 60], [22.5, 40], [27.5, 0], [32.5, 268] ],
        }

fname_re = re.compile('(?P<timestamp>\\d+)_(?P<substance>.*?)\.png')

def coord2xy(e,n):
    x = 1.4 * e/1000. - 658.2
    y =-1.42* n/1000. + 423.32
    return x,y

class gradient(object):


    def __init__(self,tuples,wrapat=247,interpolate=False):
        ''' ``wrapat`` defines at which hue value the circle is "unfolded"
            -- i.e. specify something that is NOT used in the color scale '''
        self.wrapat = 247
        self.interpolate = interpolate
        self.tuples = tuples
        for i in range(len(self.tuples)):
            if self.tuples[i][1] < wrapat:
                self.tuples[i][1] += wrapat

    def get(self,hue):
        if hue<self.wrapat:
            hue += self.wrapat
        diff = 360
        best = None
        for i,vh in enumerate(self.tuples):
            if abs(vh[1]-hue) < diff:
                diff= abs(vh[1]-hue)
                best= i

        if self.interpolate:
            raise Exception('not implemented yet') #TODO ?
            if hue < self.tuples[i][1]:
                if i>0:
                    return self.between(hue,self.tuples[i-1],self.tuples[i])
            else:
                if i+1<len(self.tuples):
                    return self.between(hue,self.tuples[i],self.tuples[i+1])

        return self.tuples[best][0]

    def between(self,h,vh1,vh2):
        return vh1[0] + (vh2[0]-vh1[0]) * (h-vh1[1])/(vh2[1]-vh1[1])


class MapException(Exception):
    pass

class mapImage(object):

    def __init__(self,fname):

        self.fname = fname
        basename = os.path.basename(fname)
        m = fname_re.match(basename)
        if not m:
            raise Exception('not valid file name for mapImage : ' + basename)
        self.timestamp = m.group('timestamp')
        self.year = int(self.timestamp[:4])
        self.substance = m.group('substance')
        self.gradient = gradient(mappings[self.substance])
        self.img = Image.open(fname)
        self.pixels = self.img.load()


    def pixel(self,e,n):
        ''' returns pixel value (0..1,0..1,0..1) at specified coordinates '''
        x,y = coord2xy(e,n)
        if x>=self.img.size[0] or x<0 or y>=self.img.size[1] or y<0:
            raise MapException('indexes {e}/{n} (mapping to {x},{y}) out of bounds'.format(
                e=e,n=n,x=x,y=y))
        r,g,b= self.pixels[int(x),int(y)] #TODO bound checks, interpolate
        return (r/256.,g/256.,b/256.)

    def hue(self,e,n):
        ''' returns hue (0..360) value at specified coordinates '''
        v= self.pixel(e,n)
        return colorsys.rgb_to_hsv(*v)[0] * 360

    def valid(self,e,n):
        ''' returns whether given coordinates point to valid point on map '''
        v= self.pixel(e,n)
        return colorsys.rgb_to_hsv(*v)[1] > 0

    def value(self,e,n):
        if not self.valid(e,n):
            raise MapException('cannot calculate value for invalid pixel')
        return self.gradient.get(self.hue(e,n))
        # there's no blue in the maps, so we map around


    def dump(self,e,n,fname):
        ''' for debugging purposes; draws rectangle at coordinates '''
        img = Image.open(self.fname)
        draw = ImageDraw.Draw(img)
        x,y= coord2xy(e,n)
        draw.rectangle( [x-5,y-5,x+5,y+5] ,outline='#FF0000' )
        del draw
        img.save(fname)


