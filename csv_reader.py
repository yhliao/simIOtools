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
            elif row=="":
               pass
            else:
               tokens = row.split(",")
               for j, t in enumerate(tokens):
                  arr = self.data[j]

                  arr.append(float(t))
         ref.close()

   def todict(self,periodicity=0):
      if periodicity == 0:
         return dict(zip(self.field,self.data))
      else:
         assert len(self.field) == len(self.data)
         assert len(self.field) % periodicity == 0
         numdict = int(len(self.field) / periodicity)
         dictlist = []
         for i in range(numdict):
            i_from = i * periodicity
            i_to   = i_from + periodicity
            newdict = dict(zip(self.field[i_from:i_to],
                               self.data[i_from:i_to]))
            dictlist.append(newdict)
         return dictlist

   def retrieve(self,varname):
      idx = self.field.index(varname)
      return np.array(self.data[idx])

   def tolist(self):
      return self.field, self.data
