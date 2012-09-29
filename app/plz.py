# -*- coding: utf-8 -*-

class locateCH(object):

    def __init__(self,fname):
        self.fname= fname

        self.data= []
        self.replacements=[
                (u'ä',u'u'),
                (u'ö',u'u'),
                (u'ü',u'u'),
                (u'é',u'u'),
                (u'è',u'u'),
                (u'ê',u'e'),
                (u'ë',u'u'),
                (u'ï',u'i'),
                (u'î',u'i'),
                (u'ç',u'c'),
                ]

        with file(fname,'r') as f:

            for line in f.readlines()[1:]:

                ort,plz,x,gemeinde,canton,e,n = line.decode('utf-8').rstrip().split(';')
                self.data.append({
                        'ort' : ort,
                        'ort_f' : self.fuzzify(ort),
                        'plz' : plz,
                        'coord' : (int(e),int(n)),
                    })


    def fuzzify(self,x):
        x= x.lower()
        for ft in self.replacements:
            x=x.replace(ft[0],ft[1])
        return x

    def find(self,prefix,limit=100):
        #TODO speed up
        prefix_f = self.fuzzify(prefix)

        ret= []
        orte = []

        for x in self.data:

            if x['ort_f'][:len(prefix_f)] == prefix_f and x['ort'] not in orte:
                ret.append(x)
                orte.append(x['ort'])

            if len(ret) >= limit:
                break

        return ret


    def by_plz(self,plz):
        for x in self.data:
            if x['plz'] == plz:
                return x
        return None
