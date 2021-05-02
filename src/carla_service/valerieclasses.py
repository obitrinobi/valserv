#!/usr/bin/env python3

# coding=UTF-8

import os
import re
import sys
import argparse
import glob
import pickle
import json
import collections
import copy 
import uuid
from enum import Enum, IntEnum



#//
#//                 INTEL CORPORATION PROPRIETARY INFORMATION
#//
#//    This software is supplied under the terms of a license agreement or
#//    nondisclosure agreement with Intel Corporation and may not be copied
#//    or disclosed except in accordance with the terms of that agreement.
#//    Copyright (C) 2020 Intel Corporation. All Rights Reserved.
#//
#//    ## specifics
#//
#//    Valerie - Validation Framework 
#//    Author: Oliver Grau



#################### Logging / Printing ####################

class PrintLevel(IntEnum):
    """Enumeration for print verbosity levels"""
    nothing = 0
    error = 1
    warning = 2
    info = 3
    debug = 4

class Printer(): #Thread):
    """A thread safe printer class"""
    def __init__(self):
        """Constructor"""
        #Thread.__init__(self)
        self.level = PrintLevel.info
        #self.queue = Queue()
        #self.start()

    def print(self, level, string):
        """Print a string to the printer queue
        level: verbosity level (from PrintLevels)
        string: string to print, possibly multi line
        """
        if level <= self.level:
            #self.queue.put(string)
            print(string)

    #def run(self):
    #    while True:
    #        string = self.queue.get()
    #        print(string)
    #        #time.sleep(1)

PRINTER = Printer()


class VMeta ():

  """
   

  :version:
  :author:
  """

  def __init__(self,s=None,dict=None):
    """
     

    @return  :
    @author
    """
    self.name=""
    if dict:
      self.name=dict['Name']
    if s:
      self.name=s

    #print ("VMeta init") 
    pass
  def __str__(self):
    return self.name
  def ToObjDict(self):
          type_name = self.__class__.__name__
          return { type_name : self.ToDict() }
  def ToDict(self):
          type_name = "__"+self.__class__.__name__+"__"
          data = {}
          data[type_name] = True
          data['Name'] = self.name
          return data



##
##
class Attribute (VMeta):

  """
   

  :version:
  :author:
  """

  def __init__(self,s=None,dict=None):
    """
     

    @return  :
    @author
    """
    VMeta.__init__(self,s,dict)
    self.index = None
    if dict:
      #print("AttributeF init:",dict)
      if 'index' in dict:
          self.index=dict['index']
    pass

  def ToDict(self):
    type_name = "__"+self.__class__.__name__+"__"
    data = super().ToDict()
    data[type_name] = True
    if self.index!=None:
       data['index'] = self.index
    return data

######################

class AttributeF (Attribute):
  """
   

  :version:
  :author:
  """
  def __init__(self,s=None, v=0.0, vmin=0.0, vmax=1.0, dict=None ):
    """
     

    @return  :
    @author
    """

    Attribute.__init__(self,s,dict)
    self.v=v
    self.vmin=vmin
    self.vmax=vmax

    if dict:
      #print("AttributeF init:",dict)
      self.v=dict['v']
      self.vmin=dict['vmin']
      self.vmax=dict['vmax']
      self.vmin=dict['vmin']

    pass
  def __str__(self):
    return '{{"Name" = "{0}","value" = "{1}", "min" = {2}", "max" = {3}}}'.format(self.name, self.v, self.vmin, self.vmax)
  def InfoPrint(self):
    print(self)

  def ToDict(self):
          type_name = "__"+self.__class__.__name__+"__"
          data = super().ToDict()
          data[type_name] = True
          data['Name'] = self.name
          data['v'] = self.v
          data['vmin'] = self.vmin
          data['vmax'] = self.vmax
          return data


######################

class SampleF (AttributeF):
    """
    

    :version:
    :author:
    """
    def __init__(self,s=None, v=0.0, vmin=0.0, vmax=1.0, step=0.1, dict=None ):
        """
        

        @return  :
        @author
        """
        AttributeF.__init__(self,s,v, vmin,vmax,dict=dict)
        self.step=step
        if dict:
            self.step=dict['step']
        pass
    def __str__(self):
        return '{{"Name" = "{0}","value" = "{1}", "min" = {2}", "max" = {3}", "step" = {4}}}'.format(self.name, self.v, self.vmin,   self.vmax, self.step)
    def ToDict(self):
        type_name = "__"+self.__class__.__name__+"__"
        data = super().ToDict()
        data[type_name] = True
        data['step'] = self.step
        return data
    def StartValue(self):
        self.v = self.vmin
    def Increment(self):
        if self.v+self.step < self.vmax:
            self.v += self.step
            return True
        return False

######################

class Node (VMeta):

  """
   

  :version:
  :author:
  """

  """ ATTRIBUTES

   

  """

  def __init__(self,n=None, dict=None):
    """
     

    @return  :
    @author
    """
    VMeta.__init__(self,n, dict)
    self.uuid=str(uuid.uuid1())
    self.vindex = None
    self.attributelist = []
    if dict:
        if 'attributes' in dict:
            for a in dict['attributes']:
                print ("Attribute:",a)
                self.Add(a)
    pass
  def Add(self,a):
    a.index= len(self.attributelist)
    self.attributelist.append(a)
  # generate index info for attributes. Can be used to generate filenames, etc..
  def UniqueAttrId (self):
      rlist = []
      for a in self.attributelist:
         v=self.uuid,a.index,a.name
         rlist.append(v)
      return rlist
  
  def __str__(self):
    return '{{"Name" = "{0}","uuid" = "{1}" }}'.format(self.name, self.uuid )
  def InfoPrint(self):
    print(self.name," l:",len(self.attributelist), " id:",self.uuid, " vindex:",self.vindex  )
    for i in self.attributelist:
      i.InfoPrint()

  def ToDict(self):
          type_name = "__"+self.__class__.__name__+"__"
          data = super().ToDict()
          data[type_name] = True
          if self.attributelist:
            data['attributes'] = []
            for a in self.attributelist:
               data['attributes'].append(a.ToObjDict())
          data['uuid']=self.uuid
          data['vindex']=self.vindex
          return data

######################


class Sampler (VMeta):

    """
    

    :version:
    :author:
    """

    """ ATTRIBUTES

    

    """

    def __init__(self, node,n=None, dict=None):
        """
     

        @return  :
        @author
        """
        VMeta.__init__(self,n,dict)
        self.node=copy.deepcopy(node)  # could be shallow?
    def InfoPrint(self):
        print(self.name," l:",len(self.node.attributelist)," -> ",self.node.attributelist )
        #for i in self.nodelist:
            #i.InfoPrint()
    def ToDict(self):
        type_name = "__"+self.__class__.__name__+"__"
        data = super().ToDict()
        data[type_name] = True
        return data
    def __iter__(self):
        self.itnode= copy.deepcopy(self.node)
        self.index =0
        self.itnode.vindex=self.index
        for a in self.itnode.attributelist:
           a.StartValue()
        if len(self.itnode.attributelist):
           self.itnode.attributelist[0].v -= self.itnode.attributelist[0].step
        #print("Sampler __iter__")
        return self
    def __next__(self):
        for i in range(len(self.itnode.attributelist)):
            if self.itnode.attributelist[i].Increment():
                #print("__next__")
                self.itnode.vindex=self.index
                self.index =self.index+1
                return self.itnode
            #print("itnode:",self.itnode.attributelist[i])
            #print("node:",self.node.attributelist[i])
            self.itnode.attributelist[i].StartValue()
            #print("itnode-new:",self.itnode.attributelist[i])
        raise StopIteration


######################

class Controller (VMeta):

  """
   

  :version:
  :author:
  """

  """ ATTRIBUTES

   

  """

  def __init__(self,n=None):
    """
     

    @return  :
    @author
    """
    VMeta.__init__(self,n)
    self.curent = None
    self.nodelist = []
    self.renderer = None
    self.evaluator = None
    self.debug=0
    pass
  def Add(self,a):
    self.nodelist.append(a)
  def SetCurent(self, n):
    self.curent = n
  def SetRenderer(self, r):
    self.renderer = r
    r.SetNode(self.curent)
  def SetEvaluator(self, r):
    self.evaluator = r
    r.SetNode(self.curent)
  def Config( self, inputdir, softwaredir, outputdir, debug=0, servernodes=3): 
    self.inputdir=inputdir
    self.softwaredir=softwaredir
    self.outputdir=outputdir
    self.debug=debug
    self.servernodes=servernodes

  def Run(self):
      if self.curent == None:
          print ("Controller::Run need a start node - pass")
          return
      if self.renderer == None:
          print ("Controller::Run need a renderer - pass")
          return
      if self.evaluator == None:
          print ("Controller::Run need an evaluator - pass")
          return

      PRINTER.print(PrintLevel.info, self )

      startnode=self.curent
      sampler=Sampler(startnode)
      var_path = os.path.join(self.inputdir, "variants")
      servernodes = 1
      if self.debug is 0 :
        folder_indx = 1
        for variant in sampler:
          folder_indx = folder_indx%(servernodes + 1)
          if(folder_indx==0):
            folder_indx = 1
          var_path = "variants/" + str(folder_indx)
          var_path = os.path.join(self.inputdir, var_path)
          if not os.path.exists(var_path):
            os.makedirs(var_path) # create directory for variants
            print("created dir" + (var_path))
          servernodes = servernodes + 1
          if servernodes > self.servernodes:
            servernodes = self.servernodes
          fn="{}/variant-{}.json".format(var_path,variant.vindex)
          PRINTER.print(PrintLevel.info, "Store variant '{}'".format(fn))
          #WriteJson(fn, variant)
          with open(fn, 'w', encoding='utf-8') as f:
            json.dump(variant, f, cls=ValEncoder, ensure_ascii=False, indent=4)
          folder_indx = folder_indx + 1

        self.renderer.Run()
        self.evaluator.Run( self.renderer.jobid )
      else:
        for variant in sampler:
          fn="{}/variant-{}.json".format(os.path.join(self.inputdir,"variants"),variant.vindex)
          PRINTER.print(PrintLevel.info, "Store variant into'{}'".format(fn) )
          #WriteJson(fn, variant)
          with open(fn, 'w', encoding='utf-8') as f:
            json.dump(variant, f, cls=ValEncoder, ensure_ascii=False, indent=4)


  def __str__(self):
    return '{{"Controller cur: "{}","debug" = "{}"}}'.format(self.curent, self.debug)

  def InfoPrint(self):
    print(self.name," l:",len(self.nodelist)," -> ",self.nodelist )
    for i in self.nodelist:
      i.InfoPrint()


#####
class ValEncoder(json.JSONEncoder):
    def default(self, obj):
      if isinstance(obj, AttributeF):
          return obj.ToObjDict()
      if isinstance(obj, SampleF):
          return obj.ToObjDict()
      if isinstance(obj, Node):
          return obj.ToObjDict()

      # Let the base class default method raise the TypeError
      return json.JSONEncoder.default(self, obj)

def ValDecoderOld(dct):
    print("ValDecoder:",dct)
    if '__AttributeF__' in dct:
        return AttributeF( dict=dct )
    if '__SampleF__' in dct:
        return SampleF( dict=dct )
    if '__Node__' in dct:
        return Node( dict=dct )
    return dct

def ValDecoder(dct):
    PRINTER.print(PrintLevel.debug, "ValDecoder dict: '{}'".format(dct))
    if '__AttributeF__' in dct:
        return AttributeF( dict=dct )
    if 'AttributeF' in dct:
        return dct['AttributeF']
    if '__SampleF__' in dct:
        return SampleF( dict=dct )
    if 'SampleF' in dct:
        #print("dct['SampleF']:",dct['SampleF'])
        return dct['SampleF'] 
    if '__Node__' in dct:
        return Node( dict=dct )
    if 'Node' in dct:
        #print("dct['Node']:",dct['Node'])
        return dct['Node']
    #print("!!!!!!!!")
    return dct


def WriteJson( fn, o):
    #  write json file
    with open(fn, 'w', encoding='utf-8') as f:
        json.dump(o, f, cls=ValEncoder, ensure_ascii=False, indent=4)

def ReadJson( fn, o):
    # read json file
    with open(fn, 'r', encoding='utf-8') as f:
        obj=json.load( f, object_hook=ValDecoder )
        return obj
    return None




if __name__ == '__main__':
    main(sys.argv[1:])

