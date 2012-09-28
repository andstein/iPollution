

class locateCH(object):

    def __init__(self,fname):
        self.fname= fname

        self.data= []

        with file(fname,'r') as f:

            for line in f.readlines()[1:]:

                ort,plz,x,gemeinde,canton,e,n = line.rstrip().split(';')
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

        for x in self.data:

            if x['ort_f'][:len(prefix_f)] == prefix_f and x['ort'] not in orte:
                ret.append(x)
                orte.append(x['ort'])

            if len(ret) >= limit:
                break

        return ret

