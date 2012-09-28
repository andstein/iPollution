import os.path
import re
import colorsys
import Image, ImageDraw

import config


# maps from hue to value for different substance
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
            if self.tuples[i][0] < wrapat:
                self.tuples[i][0] += wrapat

    def get(self,hue):
        if hue<self.wrapat:
            hue += self.wrapat
        diff = 256
        best = None
        for i,hv in enumerate(self.tuples):
            if abs(hv[0]-hue) < diff:
                diff= abs(hv[0]-hue)
                best= i


        if self.interpolate:
            raise Exception('not implemented yet') #TODO
            if hue < self.tuples[i][0]:
                if i>0:
                    return self.between(hue,self.tuples[i-1],self.tuples[i])
            else:
                if i+1<len(self.tuples):
                    return self.between(hue,self.tuples[i],self.tuples[i+1])

        return self.tuples[i][1]

    def between(self,h,hv1,hv2):
        return hv1[1] + (hv2[1]-hv1[1]) * (h-hv1[0])/(hv2[0]-hv1[0])



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
        ''' returns pixel value at specified coordinates '''
        x,y = coord2xy(e,n)
        return self.pixels[int(x),int(y)] #TODO bound checks, interpolate

    def hue(self,e,n):
        ''' returns hue value at specified coordinates '''
        v= self.pixel(e,n)
        return colorsys.rgb_to_hsv(*v)[2]

    def valid(self,e,n):
        ''' returns whether given coordinates point to valid point on map '''
        v= self.pixel(e,n)
        return colorsys.rgb_to_hsv(*v)[1] > 0

    def value(self,e,n):
        if not self.valid(e,n):
            raise Exception('cannot calculate value for invalid pixel')
        return self.gradient.get(self.hue(e,n))
        # there's no blue in the maps, so we map around


    def dump(self,e,n,fname):
        ''' for debugging purposes; draws rectangle at coordinates '''
        img = Image.open(self.fname)
        draw = ImageDraw.Draw(img)
        x,y= coord2xy(e,n)
        print 'coords : x=%d y=%d'%(x,y)
        draw.rectangle( [x-5,y-5,x+5,y+5] ,outline='#FF0000' )
        del draw
        img.save(fname)


images= []
for fname in os.listdir(config.images_dir):
    if fname_re.match(fname):
        images.append( mapImage(os.path.join(config.images_dir,fname)) )

