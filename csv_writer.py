import os
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

def write_column(wfname,fieldname,coldata,force=False):
   assert(len(fieldname)==len(coldata))
   numcol = len(coldata)
   collen  = [len(data) for data in coldata]
   headlen = [len(data) for data in fieldname]
   if os.path.isfile(wfname) and (not force):
      overwrite = input(wfname+" already exists. Overwrite? ")
      if overwrite == "y":
         pass
      else:
         return
      
   try:
      wf=open(wfname,"w")
   except FileNotFoundError:
      dirname = wfname[:wfname.rfind('/')]
      print ("csv_writer --- Creating Directory", dirname)
      os.makedirs(dirname)
      wf=open(wfname,"w")
   finally:
      for j in range(max(headlen)):
         for i in range(numcol):
            if j < headlen[i]:
               wf.write(str(fieldname[i][j]))
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
