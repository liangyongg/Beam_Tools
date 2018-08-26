#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from KLCommentedImpl import KLCommented
from KLCommentImpl import KLComment

class KLTypeOp(KLCommented):

  __op = None
  __lhs = None
  __rhs = None
  __isUnary = False

  def __init__(self, data):

    # call superclass
    super(KLTypeOp, self).__init__(data)

    if data['type'] == "ComparisonOpImpl":
      if data['binOpType'] == 'eq':
        self.__op = 'equal'
      elif data['binOpType'] == 'ne':
        self.__op = 'notequal'
      elif data['binOpType'] == 'lt':
        self.__op = 'lessthan'
      elif data['binOpType'] == 'gt':
        self.__op = 'greaterthan'
      self.__lhs = data['lhs']['type']
      self.__rhs = data['rhs']['type']
    elif data['type'] == "AssignOpImpl":
      self.__op = 'assign'
      self.__lhs = data['thisType']
      self.__rhs = data['rhs']['type']
    elif data['type'] == "BinOpImpl":
      self.__op = data['binOpType'].lower()
      self.__lhs = data['lhs']['type']
      self.__rhs = data['rhs']['type']
    elif data['type'] == "ASTUniOpDecl":
      self.__op = data['uniOpType'].lower()
      self.__rhs = data['thisType']
      self.__lhs = self.__rhs
      self.__isUnary = True

  def getOp(self):
    return self.__op

  def isUnary(self):
    return self.__isUnary

  def getLhs(self):
    return self.__lhs

  def getRhs(self):
    return self.__rhs

  def getName(self):
    if self.__op == 'equal':
      return '=='

    elif self.__op == 'notequal':
      return '!='

    elif self.__op == 'lessthan':
      return '<'

    elif self.__op == 'greaterthan':
      return '>'

    elif self.__op == 'assign':
      return '='

    elif self.__op == 'add':
      return '+'

    elif self.__op == 'sub':
      return '-'

    elif self.__op == 'mul':
      return '*'

    elif self.__op == 'div':
      return '/'

    elif self.__op == 'neg':
      return '-'

    elif self.__op == 'pos':
      return '+'

    else:
      raise Exception('KLTypeOp %s not implemented in KLTypeOpImpl.py!' % self.__op)

    return None


  def getKLCode(self, includeReturnType = True, includeKeyWord = True, includePrefix = True, includeName = True):

    code = ''
    if includeKeyWord:
      code += 'function '

    if self.__op == 'equal':
      if includeReturnType:
        code += 'Boolean '
      if includeName:
        code += '== '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'notequal':
      if includeReturnType:
        code += 'Boolean '
      if includeName:
        code += '!= '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'lessthan':
      if includeReturnType:
        code += 'Boolean '
      if includeName:
        code += '< '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'greaterthan':
      if includeReturnType:
        code += 'Boolean '
      if includeName:
        code += '> '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'assign':
      if includeReturnType:
        code += '%s ' % self.getLhs()
      if includeName:
        code += '= '
      code += '( %s other )' % (self.getRhs())

    elif self.__op == 'add':
      if includeReturnType:
        code += '%s ' % self.getLhs()
      if includeName:
        code += '+ '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'sub':
      if includeReturnType:
        code += '%s ' % self.getLhs()
      if includeName:
        code += '- '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'mul':
      if includeReturnType:
        code += '%s ' % self.getLhs()
      if includeName:
        code += '* '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'div':
      if includeReturnType:
        code += '%s ' % self.getLhs()
      if includeName:
        code += '/ '
      code += '( %s a, %s b )' % (self.getLhs(), self.getRhs())

    elif self.__op == 'neg':
      if includeName:
        code += '- '
      code += '%s' % (self.getLhs())

    elif self.__op == 'pos':
      if includeName:
        code += '+ '
      code += '%s' % (self.getLhs())

    else:
      raise Exception('KLTypeOp %s not implemented in KLTypeOpImpl.py!' % self.__op)

    return code

  def getLabel(self):
    return self.getKLCode(includeKeyWord = False)

  def getParameters(self):
    return []

  def getThisType(self):
    return self.getLhs()

  def getReturnType(self):
    if self.__op == 'equal':
      return 'Boolean'

    elif self.__op == 'assign':
      return self.getThisType()

    elif self.__op == 'add':
      return self.getThisType()

    elif self.__op == 'sub':
      return self.getThisType()

    elif self.__op == 'mul':
      return self.getThisType()

    elif self.__op == 'div':
      return self.getThisType()

    elif self.__op == 'neg':
      return None

    elif self.__op == 'pos':
      return None

    return None

  def isInternal(self):
    return False
