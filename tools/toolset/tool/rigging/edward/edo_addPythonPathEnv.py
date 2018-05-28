import sys
import edward as edo

def edo_addPythonPathEnv(path):
    if not path in sys.path:
        sys.path.append(path)
        print 'add edward python path env...'
    else:
        print 'edward python path env has already been in thi sys path...'

edopythonpath=edo.__file__.replace('\\','/').split('__')[0]+'/python/'
edo_addPythonPathEnv(edopythonpath)