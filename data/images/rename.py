
import os,os.path,re

fname_re = re.compile('(?P<timestamp>\\d+)_(?P<substance>.*?)\.png')

for fname in os.listdir('.'):

    m = fname_re.match(fname)
    if m:

        newname = m.group('timestamp')[:4] + '_' + m.group('substance') + '_BAFU.png'
        os.rename(fname, newname)

        print '{fname} -> {newname}'.format(fname=fname,newname=newname)

