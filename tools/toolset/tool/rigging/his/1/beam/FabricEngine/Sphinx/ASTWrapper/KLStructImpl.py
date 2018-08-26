#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLCommentedImpl import KLCommented
from KLMemberImpl import KLMember

class KLStruct(KLCommented):

  __name = None
  __members = None
  __operators = None
  __operatorLookup = None
  __methods = None
  __methodLookup = None
  __types = {}
  __parentStructName = None
  __methodsCache = None

  def __init__(self, data):

    # call superclass
    super(KLStruct, self).__init__(data)

    self.__name = data['name']
    KLStruct.__types[self.__name] = self

    if data.has_key('parentStructName'):
      self.__parentStructName = data['parentStructName']

    self.__members = []
    for member in data['members']:
      self.__members += [KLMember(member)]

    self.__operators = {}
    self.__operatorLookup = {}
    self.__methods = {}
    self.__methodLookup = {}
    self.__methodsCache = {}

  @staticmethod
  def getAll():
    return KLStruct.__types

  @staticmethod
  def getRef(name, useRefs = True):
    if not name:
      return ''
    if KLStruct.__types.has_key(name) and useRefs:
      return ':ref:`'+name.lower()+'`'
    return name

  def getName(self):
    return self.__name

  def getKLType(self):
    return 'struct'

  def getMembers(self, includeInherited = False):
    if not includeInherited:
      return self.__members
    parents = self.getParents()
    members = []
    for p in parents:
      members += p.getMembers(includeInherited = True)
    members += self.__members
    return members

  def getMethods(self, includeInherited = False, includeInternal = True, category = None):
    if category == 'operators':
      return self.getOperators()

    cacheKey = str(int(includeInherited))+str(int(includeInternal))+str(category)
    if self.__methodsCache.has_key(cacheKey):
      return self.__methodsCache[cacheKey]

    # print self.getName()+ ' getMethods '+cacheKey+' '+str(self.__methodsCache.keys())

    methods = self.__methods.values()

    filteredMethods = []
    for m in methods:
      if m.isInternal() and not includeInternal:
        continue
      if m.getComments().getSingleQualifier('category', category) != category and category:
        continue
      filteredMethods.append(m)

    methods = filteredMethods

    lookup = {}
    for m in methods:
      key = m.getLabel()
      lookup[key] = m

    if includeInherited:
      parents = self.getParents()
      for parent in parents:
        parentMethods = parent.getMethods(includeInherited = includeInherited, includeInternal = includeInternal, category = category)
        for m in parentMethods:
          if not m.isVirtual():
            continue
          key = m.getLabel()
          if lookup.has_key(key):
            continue
          lookup[key] = m

    # if no category is set...
    if not category:

      hasDefaultConstructor = False
      hasCopyConstructor = False
      hasClone = False

      for key in lookup:
        m = lookup[key]
        params = m.getParameters()
        if m.isConstructor():
          if len(params) == 0:
            hasDefaultConstructor = True
            continue
          elif(len(params)) == 1:
            if params[0].getType() == self.getName():
              hasCopyConstructor = True
              continue
        elif m.getName() == 'clone' and len(params) == 0:
          hasClone = True

    if not hasDefaultConstructor or not hasCopyConstructor or not hasClone:
      from KLMethodImpl import KLMethod
      t = self.getName()
      if not hasDefaultConstructor:
        m = KLMethod({'thisUsage': 'in', 'preComments': ['/// default constructor\n'], 'name': t, 'returnType': '', 'params': [], 'type': 'MethodOpImpl'}, self.getName())
        self._addMethod(m)
        lookup[m.getLabel()] = m
      if not hasCopyConstructor:
        m = KLMethod({'thisUsage': 'in', 'preComments': ['/// copy constructor\n'], 'name': t, 'returnType': '', 'params': [{'usage': 'in', 'typeUserName': t, 'name': 'other'}], 'type': 'MethodOpImpl'}, self.getName())
        self._addMethod(m)
        lookup[m.getLabel()] = m
      if not hasClone:
        m = KLMethod({'thisUsage': 'in', 'preComments': ['/// clone method\n'], 'name': 'clone', 'thisType': t, 'returnType': t, 'params': [], 'type': 'MethodOpImpl'}, self.getName())
        self._addMethod(m)
        lookup[m.getLabel()] = m

    result = []
    for key in sorted(lookup.keys()):
      result.append(lookup[key])    

    self.__methodsCache[cacheKey] = result

    return result

  def getMethod(self, key, includeInternal = False):
    if self.__methods.has_key(key):
      return self.__methods[key]
    if self.__methodLookup.has_key(key):
      return self.__methods[self.__methodLookup[key]]
    for id in self.__methods:
      m = self.__methods[id]
      if m.getName() == key and (includeInternal or not m.isInternal()):
        return m
    return None

  def getOperators(self, includeInherited = False):
    lookup = {}
    for id in self.__operators:
      lookup[self.__operators[id].getLabel()] = self.__operators[id]

    result = []
    for key in sorted(lookup.keys()):
      result.append(lookup[key])    

    return result

  def getOperator(self, key):
    if self.__operators.has_key(key):
      return self.__operators[key]
    if self.__operatorLookup.has_key(key):
      return self.__operators[self.__operatorLookup[key]]
    for id in self.__operators:
      o = self.__operators[id]
      if o.getName() == key:
        return o
    return None

  def getParents(self):
    if not self.__parentStructName:
      return []
    p = self.__parentStructName
    ts = KLStruct.__types
    content = []
    if ts.has_key(p):
      if isinstance(ts[p], KLStruct):
        content += [ts[p]]
    return content

  def _addOperator(self, decl):
    label = decl.getLabel()

    if self.__operatorLookup.has_key(label):
      # todo: error out here
      return

    self.__operatorLookup[label] = decl.getID()
    self.__operators[decl.getID()] = decl

  def _addMethod(self, decl):
    label = decl.getLabel()
    if self.__methodLookup.has_key(label):
      # todo: error out here
      return

    self.__methodLookup[label] = decl.getID()
    self.__methods[decl.getID()] = decl
