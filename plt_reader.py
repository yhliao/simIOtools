import re
import numpy as np
### This module is supposed to work well with the standard .plt
### files generated by Sentaurus, but doesn't have good flexibility
class readPLT:
   def __init__(self):
      self.datasets  = []
      self.functions = []
      self.datachunk = []
      self.names     = []

   def set_name(self,names):
      self.names = names
      
   def retrieveAll(self):
      returndata = []
      for name in self.names:
         returndata.append(self.retrieve(name))
      return np.vstack(returndata).T

   def retrieve(self,name):
      nr = nc = -1 
      for i,sets in enumerate(self.datasets):
         if name in sets:
            j = sets.index(name)
            nr = i
            nc = j
      if nr == -1 or nc ==-1:
         print ("Retrieval failed!!"+
               "\"{}\" not found in the datasets".format(name))
         return None
      data = np.empty(len(self.datachunk))
      for i,chunk in enumerate(self.datachunk):
         data[i] = chunk[nr][nc]
      return data

   def read_plt(self,filename):
      print ("Reading file {}...".format(filename))
      pltfile = open(filename,"r")
      ### Skip first 6 lines
      for i in range(5):
         pltfile.readline()
      ## Dealing with datasets
      line = pltfile.readline()
      assert line.find("datasets")!=-1
      assert line.find("[")!=-1
      rightbracketfound = -1
      while rightbracketfound == -1:
         line = pltfile.readline()
         rightbracketfound = line.find("]")
         #datasubset = re.findall(r"\w+[(| *]\w*,{0,1}\w*[)]{0,1}",line)
         tokens = line.split("\"")
         self.datasets.append([tokens[i] for i in range(1,len(tokens),2)])
      #print ("Definition of dataset loaded")
      ## Dealing with functions 
      line = pltfile.readline()
      assert line.find("functions")!=-1
      assert line.find("[")!=-1
      rightbracketfound = -1
      while rightbracketfound == -1:
         line = pltfile.readline()
         rightbracketfound = line.find("]")
         funcsubset = re.findall(r"\w+",line)
         self.functions.append(funcsubset)
      #print ("Definition of function set loaded")

      nrows = len(self.datasets)
      assert len(self.functions)==nrows
      ## Dealing with Data
      Datastart = -1
      while Datastart == -1:
         line = pltfile.readline()
         Datastart = line.find("Data")
      assert line.find("{") != -1

      rightbracketfound = -1
      while True:
         datachunk = []
         line = pltfile.readline()
         rightbracketfound = line.find("}")
         if rightbracketfound != -1 or line=="":
            break
         datasubset = re.findall(r"[^ |^\n|^\]]+",line)
         datachunk.append(datasubset)
         for i in range(nrows-1):
            line = pltfile.readline()
            assert line.find("}") == -1
            datasubset = re.findall(r"[^ |^\n|^\]]+",line)
            datachunk.append(datasubset)

         self.datachunk.append(datachunk)
      #print ("Data chunks loaded")
      pltfile.close()