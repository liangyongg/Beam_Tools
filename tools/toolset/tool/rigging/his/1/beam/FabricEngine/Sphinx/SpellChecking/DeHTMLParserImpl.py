#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

class DeHTMLParser(HTMLParser):

  def __init__(self, debugLog = False):
    HTMLParser.__init__(self)
    self.__text = []
    self.__stack = []
    self.__ignoredTags = 0
    self.__tagsToIgnore = ['title', 'script', 'a', 'svg']
    self.__classesToIgnore = ['xref', 'highlight', 'highlighttable', 'klcode', 'methodtable', 'paramtable', 'footer', 'search', 'search-tip', 'pre']
    self.__debugLog = debugLog

  def startIgnoring(self):
    self.__ignoredTags = self.__ignoredTags + 1

  def endIgnoring(self):
    self.__ignoredTags = self.__ignoredTags - 1

  def isIgnoring(self):
    return self.__ignoredTags > 0

  def handle_data(self, data):
    text = data.strip()
    if len(text) > 0 and not self.isIgnoring():
      text = sub('[ \t\r\n]+', ' ', text)
      self.__text.append(text + ' ')
      if self.__debugLog:
        print text

  def handle_starttag(self, tag, attrs):
    if tag == 'p':
      self.__text.append('\n\n')
    elif tag == 'br':
      self.__text.append('\n')
    if tag in self.__tagsToIgnore:
      self.startIgnoring()
    else:
      for (attrName, attrValue) in attrs:
        if attrName == 'class':
          for className in attrValue.split(' '):
            if className in self.__classesToIgnore:
              self.startIgnoring()
              break

    if self.__debugLog:
      print '%d <-- %s %s' % (self.__ignoredTags, tag, attrs)

    self.__stack.append((tag, attrs))

  def handle_startendtag(self, tag, attrs):
    if tag == 'br':
      self.__text.append('\n\n')

  def handle_endtag(self, tag):
    if tag in self.__tagsToIgnore:
      self.endIgnoring()
    else:
      for (attrName, attrValue) in self.__stack[-1][1]:
        if attrName == 'class':
          for className in attrValue.split(' '):
            if className in self.__classesToIgnore:
              self.endIgnoring()
              break

    if len(self.__stack) > 0:
      if self.__stack[-1][0] == tag:
        self.__stack.pop()

    if self.__debugLog:
      print '%d --> %s' % (self.__ignoredTags, tag)

  def text(self):
    return ''.join(self.__text).strip()

def dehtml(text, debugLog = False):
  try:
    parser = DeHTMLParser(debugLog = debugLog)
    parser.feed(text)
    parser.close()
    if debugLog:
      print parser.text()
    return parser.text()
  except:
    print_exc(file=stderr)
    return text
