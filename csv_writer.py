class WRITEcsv:
   def __init__(self):
      self.coldata = []
      self.colname = []
   def add_cols(self,name,data):
      self.coldata += data
      self.colname += name
   def clear(self):
      self.coldata.clear()
      self.colname.clear()
   def write(self,wfname):
      write_column(wfname,self.colname,self.coldata)

def write_column(wfname,fieldname,coldata):
   assert(len(fieldname)==len(coldata))
   numcol = len(coldata)
   collen = [len(data) for data in coldata]
   with open(wfname,"w") as wf: 
      for i in range(numcol):
         wf.write(fieldname[i])
         if i < numcol-1:
            wf.write(',')
         else:
            wf.write('\n')
      for j in range(max(collen)):
         for i in range(numcol):
            if j < collen[i]:
               wf.write(str(coldata[i][j]))
            if i < numcol-1:
               wf.write(',')
            else:
               wf.write('\n')
      wf.close()
