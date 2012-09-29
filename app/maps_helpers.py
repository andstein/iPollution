import colorsys

import maps

# datapoints ( value , hue ) for different maps
BAFU_hue_mappings= {
        'no2': [ [2.5, 208], [7.5, 180], [12.5, 100], [17.5, 80], [22.5, 60], [27.5, 51], [32.5, 40], [37.5, 0], [42.5, 286] ],
        'o3': [ [50, 180], [150, 80], [250, 60], [350, 40], [450, 0], [550, 286] ],
        'pm10': [ [2.5, 208], [7.5, 180], [12.5, 80], [17.5, 60], [22.5, 40], [27.5, 0], [32.5, 268] ],
        }

def coord_for_src(src):

    def coord2xy_BAFU(e,n):
        x = 1.4 * e/1000. - 658.2
        y =-1.42* n/1000. + 423.32
        return x,y

    if src == 'BAFU':
        return coord2xy_BAFU
    else:
        raise maps.MapException('no coordinate transformation defined for ' + src)


class BAFU_hue_mapper(object):

    def __init__(self,tuples,wrapat=247,interpolate=False):
        ''' ``wrapat`` defines at which hue value the circle is "unfolded"
            -- i.e. specify something that is NOT used in the color scale '''
        self.wrapat = 247
        self.interpolate = interpolate
        self.tuples = tuples
        for i in range(len(self.tuples)):
            if self.tuples[i][1] < wrapat:
                self.tuples[i][1] += wrapat

    def valid(self,rgb):
        ''' checks whether rgb (0..1,0..1,0..1) is valid data point '''
        return colorsys.rgb_to_hsv(*rgb)[1] > 0

    def value(self,rgb):
        ''' get value for pixel rgb (0..1,0..1,0..1) '''

        hue = colorsys.rgb_to_hsv(*rgb)[0] * 360
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


def get_mapper(src,substance):

    if src == 'BAFU':

        if substance not in BAFU_hue_mappings:
            raise maps.MapException('no BAFU-hue map defined for ' + substance)

        return BAFU_hue_mapper(BAFU_hue_mappings[substance])

    else:

        raise maps.MapException('no mapper defined for ' + src)

