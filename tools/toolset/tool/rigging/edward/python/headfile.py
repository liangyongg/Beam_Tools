import sys
import os
#pspath='Z:/software/tank/studio/install/engines/app_store/tk-maya/v0.3.7/resources/pyside111_py26_qt471_win64/python'
#if not pspath in sys.path:
#    sys.path.append(pspath)
#os.environ["PATH"]  = os.environ["PATH"] + ";Z:/software/tank/studio/install/engines/app_store/tk-maya/v0.3.7/resources/pyside111_py26_qt471_win64/lib"
#from headfile import *
#import PySide
#from PySide import QtGui, QtCore

try:
    import PyQt4.QtCore as QtCore
    import PyQt4.QtGui as QtGui
    import sip as pyqtsip
except:
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import shiboken as pyqtsip
    
print 'load head file start ...'
print 'load head file end ...'
