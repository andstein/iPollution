'''
searches in ``srcdir`` for new images, then
renames + copies them into this directory
'''

import os,os.path,re,filecmp,shutil

srcdir= '../original_images'
srcdir= 'NEW'

BAFU_re = re.compile('(?P<substance>[^_]+)_(?P<year>\\d\\d)_(?P<lang>[defi])_515pix.png')
imgs= os.listdir('.')

for candidate in os.listdir(srcdir):

    fname = ''

    if BAFU_re.match(candidate):

        m= BAFU_re.match(candidate)

        year = int(m.group('year'))
        if year<50: year+=2000
        else: year+=1900

        fname = str(year)+'_'+m.group('substance')+'_BAFU.png'

    else:
        print 'cannot parse {fname} -> ignoring file'.format(fname=candidate)
        continue

    if fname not in imgs:
        print 'found NEW file ' + fname
    elif not filecmp.cmp(os.path.join(srcdir,candidate), fname):
        print 'found CHANGED file ' + fname
    else:
        continue # don't clobber ouput

    shutil.copy(os.path.join(srcdir,candidate), fname)
    print ' -> copied'

