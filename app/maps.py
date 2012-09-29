import os.path
import re
import colorsys
import Image, ImageDraw

import config,maps_helpers

fname_re = re.compile('(?P<year>\\d+)_(?P<substance>.*?)_(?P<source>.*?)\.png')


class MapException(Exception):
    pass

class mapImage(object):

    def __init__(self,fname):

        self.fname = fname
        basename = os.path.basename(fname)

        m = fname_re.match(basename)
        if not m:
            raise Exception('not valid file name for mapImage : ' + basename)

        self.year = m.group('year')
        self.substance = m.group('substance')
        self.source = m.group('source')

        self.coord = maps_helpers.coord_for_src( self.source )
        self.mapper = maps_helpers.get_mapper( self.source,self.substance )

        self.img = Image.open(fname)
        self.pixels = self.img.load()


    def pixel(self,e,n):
        ''' returns pixel value (0..1,0..1,0..1) at specified coordinates '''
        x,y = self.coord(e,n)
        if x>=self.img.size[0] or x<0 or y>=self.img.size[1] or y<0:
            raise MapException('indexes {e}/{n} (mapping to {x},{y}) out of bounds'.format(
                e=e,n=n,x=x,y=y))
        r,g,b= self.pixels[int(x),int(y)]
        return (r/256.,g/256.,b/256.)

    def valid(self,e,n):
        ''' returns whether given coordinates point to valid point on map '''
        v= self.pixel(e,n)
        return self.mapper.valid(v)

    def value(self,e,n):
        if not self.valid(e,n):
            raise MapException('cannot calculate value for invalid pixel')
        return self.mapper.value(self.pixel(e,n))


    def dump(self,e,n,fileobj):
        ''' mark coordinates; fileobj can be filename.png or StringIO '''
        img = Image.open(self.fname)
        draw = ImageDraw.Draw(img)
        x,y= self.coord(e,n)
        draw.line( [x,0,x,self.img.size[1]] ,fill='#000000' )
        draw.line( [0,y,self.img.size[0],y] ,fill='#000000' )
#        draw.rectangle( [x-5,y-5,x+5,y+5] ,outline='#FF0000' )
        del draw
        img.save(fileobj,format='PNG')


