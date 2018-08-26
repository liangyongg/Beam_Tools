#
# Copyright (c) 2010-2017 Fabric Software Inc. All rights reserved.
#

import os
import re, collections

class SpellChecker(object):

  __alphabet = 'abcdefghijklmnopqrstuvwxyz'
  __NWORDS = None

  def __init__(self, logFilePath = None, filterGlobal = False, extraWords = None):

    self.__cache = {}

    wordsEnFilePath = os.path.join(os.path.split(__file__)[0], 'wordsEn.txt')
    wordsFabricFilePath = os.path.join(os.path.split(__file__)[0], 'wordsFabric.txt')
    if SpellChecker.__NWORDS is None:
      words = self.splitWords(file(wordsEnFilePath).read()) + self.splitWords(file(wordsFabricFilePath).read())
      if extraWords:
        words += extraWords
      SpellChecker.__NWORDS = self._train(words)

    self.__logFilePath = logFilePath
    if not self.__logFilePath:
      self.__logFilePath = os.environ.get('TEMP', os.environ.get('TMP', self.__logFilePath))
      if self.__logFilePath:
        self.__logFilePath = os.path.normpath(os.path.join(self.__logFilePath, 'spelling.log'))
    self.__logFile = None
    if self.__logFilePath:
      self.__logFile = open(self.__logFilePath, 'w')

    self.__results = {}
    self.__filterGlobal = filterGlobal

  def getLogFile(self):
    return self.__logFilePath

  def splitWords(self, text):
    return re.findall('\\b[a-z]+\\b', text.lower()) 

  def _train(self, features):
    model = collections.defaultdict(lambda: 1)
    for f in features:
      model[f] += 1
    return model

  def _edits1(self, word):
    splits     = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes    = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in splits for c in SpellChecker.__alphabet if b]
    inserts    = [a + c + b     for a, b in splits for c in SpellChecker.__alphabet]
    return set(deletes + transposes + replaces + inserts)

  def _known_edits2(self, word):
    return set(e2 for e1 in self._edits1(word) for e2 in self._edits1(e1) if e2 in SpellChecker.__NWORDS)

  def _known(self, words): return set(w for w in words if w in SpellChecker.__NWORDS)

  def correctWord(self, word):
    result = self.__cache.get(word, None)
    if result:
      return result
    candidates = self._known([word]) or self._known(self._edits1(word)) or self._known_edits2(word) or [word]
    result = max(candidates, key=SpellChecker.__NWORDS.get)
    self.__cache[word] = result
    return result

  def correctText(self, text, reference = None):
    words = self.splitWords(text)
    results = {}
    for word in words:
      if len(word) < 2:
        continue
      corrected = self.correctWord(word.lower())
      if not corrected == word.lower():
        if self.__filterGlobal:
          if not self.__results.has_key(word.lower()):
            self.__results[word.lower()] = corrected
            results[word.lower()] = corrected
        else:
          results[word.lower()] = corrected

    if len(results) and self.__logFile:
      if reference:
        self.__logFile.write('\n%s\n' % reference)
      for key in results:
        self.__logFile.write('"%s" is unknown, did you mean "%s"?\n' % (key, results[key]))
    return results

