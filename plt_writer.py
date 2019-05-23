
class InspectPLT:
   def __init__(self):
      self.names     = []
      self.variables = []
      self.values    = []
      self.length = None

   def setData(self,name,variable,value):
      self.names    .append(name)
      self.variables.append(variable)
      self.values   .append(value)
      if self.length is None:
         self.length = len(value)
      else:
         assert len(value) == self.length

   def reset(self):
      del self.names
      del self.variables
      del self.values
      self.names     = []
      self.variables = []
      self.values    = []
      self.length = None

   def write_plt(self,filename):
      print ("Creating file {0}...".format(filename))
      wtfile = open(filename,"w")

      wtfile.write("DF-ISE text\n\n")
      wtfile.write("Info {\n")
      wtfile.write("  version   = 1.0\n")
      wtfile.write("  type      = xyplot\n")
      wtfile.write("  datasets  = [\n")
      wtfile.write("    ")
      for name in self.names:
         wtfile.write("\"{0}\" ".format(name))
      wtfile.write("]\n")
      wtfile.write("  functions = [\n")
      wtfile.write("    ")
      for var in self.variables:
         wtfile.write("{0} ".format(var))
      wtfile.write("]\n")
      wtfile.write("}\n\n")

      wtfile.write("Data {\n")
      for i in range(self.length):
         wtfile.write("    ")
         for dataset in self.values:
            wtfile.write("  {0}".format(dataset[i]))
         wtfile.write("\n")
      wtfile.write("}\n")
      wtfile.close()
      print ("...done!")
