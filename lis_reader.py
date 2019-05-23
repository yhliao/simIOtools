
class readLIS:
   class block(object):
      def __init__(self):
         self.sweep_var = ""
         self.sweep_value = []
         self.node_var   = []
         self.node_value = []

   def __init__(self):
      self.blocks = []
      self.numblocks = 0

   def retrieve(self,block,varname):
      returnblock = self.blocks[block]
      if varname == returnblock.sweep_var:
         return returnblock.sweep_value
      for i,name in enumerate(returnblock.node_var):
         if varname == name:
            return returnblock.node_value[i]

   def readlis(self,filename):
      with open(filename,"r") as rf:
         not_end = True
         while not_end:
            not_end = self.__readblock(rf)

   def __readblock(self,rf):
      start_parse = False
      stop_parse = False
      while not start_parse:
         line = rf.readline()
         if line.find('x')==0:
            start_parse = True
            print ("start to read a new block")
         elif line == "":
            return False

      newblock = self.block()
      rf.readline()
      ## Construciting variable names to outline the data
      var_names  = str.split(rf.readline())
      node_names = str.split(rf.readline())
      newblock.sweep_var = var_names[0]
      for node, var in zip(node_names,var_names[1:]):
         newblock.node_var.append(node+" "+var)
         newblock.node_value.append([])
      while not stop_parse:
         line = rf.readline()
         if line.find('y') == 0:
            stop_parse=True
         else:
            values = str.split(line)
            newblock.sweep_value.append(float(values[0]))
            for i,val in enumerate(values[1:]):
               newblock.node_value[i].append(float(val))
      self.blocks.append(newblock)
      self.numblocks += 1
      return True


