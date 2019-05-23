from __future__ import division
import numpy as np
import pandas as pd
## This module is used to generate organized .mdm file for ICCAP
### Only support LIN, LIST, CON sweep type here
class writeMDM:
   def __init__(self):
      self.dbnum = 0
      self.lin_exists = False
      self.USER_INPUTS = {}
      self.ICCAP_INPUTS  = {}
      self.ICCAP_OUTPUTS = {}

   def get_INPUTVAR(self,name):
      try:
         varinfo = self.ICCAP_INPUTS[name]
      except:
         varinfo = self.USER_INPUTS[name]
      finally:
         return varinfo

   def set_LINSWEEP(self,name,start,stop,stepsize):
      linvar = self.get_INPUTVAR(name)
      assert linvar["sweep_type"]=="LIN",(
            "Sweeptype of {} is not LIN!".format(name))
      stepnum = (stop-start)/stepsize + 1
      assert stepnum.is_integer()
      linvar["sweep_options"] = "1 {} {} {} {}".format(
                                 start,stop,int(stepnum),stepsize)
      linvar["data"] = np.linspace(start,stop,stepnum)
      self.dblen = int(stepnum)

   def set_CONSWEEP(self, name,value):
      convar = self.get_INPUTVAR(name)
      assert convar["sweep_type"]=="CON",(
            "Sweeptype of {} is not CON!".format(name))
      convar["sweep_options"] = str(value)
      convar["data"] = value
            

   def set_SYNCSWEEP(self, name, ratio, offset, master):
      convar = self.get_INPUTVAR(name)
      assert convar["sweep_type"]=="SYNC",(
            "Sweeptype of {} is not SYNC!".format(name))
      convar["sweep_options"] = "{} {} {}".format(
                              ratio,offset,master)
      convar["ratio"] = ratio
      convar["offset"]= offset
      convar["master"]= master

   def set_LISTSWEEP(self,name,order):
      listvar = self.get_INPUTVAR(name)
      assert listvar["sweep_type"]=="LIST",(
            "Sweeptype of {} is not LIST!".format(name))
      listvar["sweep_options"] = str(order)

   def new_ICCAP_INPUT(self,name,mode_and_options,sweep_type):
      if self.lin_exists and sweep_type=="LIN":
         raise AssertionError,(
               "Currently only one LIN SWEEP is supported")
      self.ICCAP_INPUTS[name] = {
         "mode_and_options": mode_and_options,
         "sweep_type": sweep_type,
         "sweep_options": "",
         "values" : []
      }
      if sweep_type == "LIN":
         self.lin_exists=True

   def new_USER_INPUT(self,name,sweep_type):
      if self.lin_exists and sweep_type=="LIN":
         raise AssertionError,(
               "Currently only one LIN SWEEP is supported")
      self.USER_INPUTS[name] = {
         "sweep_type": sweep_type,
         "sweep_options": "",
         "values" : []
      }
      if sweep_type == "LIN":
         self.lin_exists=True

   def new_ICCAP_OUTPUT(self,name,mode_and_options):
      self.ICCAP_OUTPUTS[name] = {
         "mode_and_options": mode_and_options,
         "values" : []
      }

   def __update(self,name,var,new_vars):
      swtype = var["sweep_type"]
      if (swtype == "CON" or swtype=="LIN" ):
         try:
            new_value = new_vars[name]
            print("trying to set a CON/LIN/SYNC variable,"
                 + "simply check if the value matches...")
            assert new_value == var["data"]
         except:
            pass
         finally:
            var["values"].append(var["data"])
      elif swtype == "SYNC":
            var["values"].append(new_vars[name])
      elif swtype == "LIST":
         try:
            var["values"].append(new_vars[name])
         except:
            raise AssertionError,(
            "The LIST variable {}". format(name) 
            + " is not specified... update failed")
      elif swtype == "SYNC":
         pass
      else:
         print "The writer can handle LIST, LIN, and CON only!!"
         raise AssertionError
   
   def add_DB(self,USER_VAR,ICCAP_VAR,tabular_output):
      ## all 3 inputs are dictionary, key: variable name
      for name, var in self.USER_INPUTS.iteritems():
         self.__update(name,var,USER_VAR)
      for name, var in self.ICCAP_INPUTS.iteritems():
         self.__update(name,var,ICCAP_VAR)
      for name, var in self.ICCAP_OUTPUTS.iteritems():
         new_data = tabular_output[name]
         if hasattr(self,"dblen"):
            assert len(new_data) == self.dblen
         else:
            self.dblen = len(new_data)
         var["values"].append(new_data)
      self.dbnum +=1

   def _preprocess(self):
      for var in self.USER_INPUTS.values():
         assert(self.dbnum == len(var["values"]))
         if var["sweep_type"] == "LIST":
            valueset = pd.unique(var["values"])
            options = var["sweep_options"]+" "+str(len(valueset))
            for val in valueset:
               options += " {}".format(val)
            var["sweep_options"]=options
      for var in self.ICCAP_INPUTS.values():
         assert(self.dbnum == len(var["values"])),(
            "{} {}".format(self.dbnum,len(var["values"])))
         if var["sweep_type"] == "LIST":
            valueset = pd.unique(var["values"])
            options = var["sweep_options"]+" "+str(len(valueset))
            for val in valueset:
               options += " {}".format(val)
            var["sweep_options"]=options
      for var in self.ICCAP_OUTPUTS.values():
         assert(self.dbnum == len(var["values"]))
      
      self.DBcol  = []
      self.DBhead = "#"
      for name, var in self.USER_INPUTS.iteritems():
         if var["sweep_type"] == "LIN":
            self.DBcol.append(var["values"])
            self.DBhead += name + " "*8 
      for name, var in self.ICCAP_INPUTS.iteritems():
         if var["sweep_type"] == "LIN":
            self.DBcol.append(var["values"])
            self.DBhead += name + " "*8
      for name, var in self.ICCAP_OUTPUTS.iteritems():
         self.DBcol.append(var["values"])
         self.DBhead += name + " "*8
      self.DBhead = self.DBhead[:-8]

   def write_file(self,filename):
      self._preprocess()
      wf = open(filename,"w")
      wf.write("!  VERSION = 6.00 \r\n")
      wf.write("BEGIN_HEADER \r\n")
      if len(self.USER_INPUTS)!=0:
         wf.write("  USER_INPUTS \r\n")
         for name, var in self.USER_INPUTS.iteritems():
            wf.write("    {}  {}  {}\r\n".format(name,
                        var["sweep_type"],var["sweep_options"]))
      wf.write("  ICCAP_INPUTS \r\n")
      for name, var in self.ICCAP_INPUTS.iteritems():
         wf.write("    {}  {} {}  {}\r\n".format(
                     name,var["mode_and_options"],
                     var["sweep_type"],var["sweep_options"]))

      wf.write("  ICCAP_OUTPUTS \r\n")
      for name, var in self.ICCAP_OUTPUTS.iteritems():
         wf.write("    {}  {} \r\n".format(
                     name,var["mode_and_options"]))
      wf.write("\r\nEND_HEADER \r\n")
      for i in range(self.dbnum):
         wf.write("\r\nBEGIN_DB\r\n")
         for name, var in self.USER_INPUTS.iteritems():
            wf.write("  USER_VAR  {}  {}\r\n".format(
                              name,var["values"][i]))
         for name, var in self.ICCAP_INPUTS.iteritems():
            if var["sweep_type"] != "LIN":
               wf.write("  ICCAP_VAR  {}  {}\r\n".format(
                                 name,var["values"][i]))
         wf.write(" \r\n"+self.DBhead+"\r\n")
         for j in range(self.dblen):
            for col in self.DBcol:
               wf.write(str(col[i][j])+"\t")
            wf.write("\n")
         wf.write("END_DB\r\n")
      wf.close()

