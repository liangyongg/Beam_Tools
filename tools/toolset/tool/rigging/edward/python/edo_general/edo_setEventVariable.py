import sys
#edo_setEventVariable(0)
def edo_setEventVariable(d=0):
    opath='//file-cluster/GDC/Resource/Support/Maya/extra/Rigging_Simulation/edward/python'
    lpath='E:/program/edward/python'
    if d==0:
        while opath in sys.path:
            sys.path.remove(opath)
        if not lpath in sys.path:
            sys.path.append(lpath)
    if d==1:
        while lpath in sys.path:
            sys.path.remove(lpath)
        if not opath in sys.path:
            sys.path.append(opath)
    print sys.path