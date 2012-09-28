# -*- coding: utf-8 -*-

class locateCH(object):

    def __init__(self,fname):
        self.fname= fname

        self.data= []

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
        return x.lower() #TODO implement

    def find(self,prefix,limit=100):
        #TODO speed up
        prefix_f = self.fuzzify(prefix)

        ret= []
        orte = []

        print prefix + ' -- ' + ''.join(["%02x-"%ord(x) for x in prefix])
        print '==='+str(type(prefix))
        print '---'+str(prefix==u'zürich')

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
