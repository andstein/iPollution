

class locateCH(object):

    def __init__(self,fname):
        self.fname= fname

        self.data= []

        with file(fname,'r') as f:

            for line in f.readlines():

                ort,plz,x,gemeinde,canton,e,n = line.rstrip().split(';')
                self.data.append({
                        'ort' : ort,
                        'ort_f' : self.fuzzify(ort),
                        'plz' : plz,
                        'coord' : (e,n),
                    })

    def fuzzify(self,x):
        return x.lower() #TODO implement

    def find(self,prefix,limit=1000):
        #TODO speed up
        prefix_f = self.fuzzify(prefix)
        ret= []
        for x in self.data:
            if x['ort_f'][:len(prefix_f)] == prefix_f:
                ret.append(x)
            if len(ret) >= limit:
                break

        return ret

