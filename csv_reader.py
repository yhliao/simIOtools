import numpy as np
class readCSV: 
   def __init__(self,filename):
      self.field = None
      self.data = []

      with open(filename) as ref:
         for i, row in enumerate(ref):
            row = row.rstrip("\n")
            if i ==0:
               self.field = row.split(",")
               for i in range(len(self.field)):
                  self.data.append([])
            else:
               tokens = row.split(",")
               assert(len(tokens)==len(self.data))
               for j, t in enumerate(tokens):
                  arr = self.data[j]

                  arr.append(float(t))
         ref.close()
   def retrieve(self,varname):
      idx = self.field.index(varname)
      return np.array(self.data[idx])
