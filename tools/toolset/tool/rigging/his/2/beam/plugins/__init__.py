import glob
import logging
import os
import sys

__all__ = [os.path.splitext(os.path.basename(plugin))[0]
           for path in __path__
           for plugin in glob.glob(os.path.join(path, '*_plugin'))]

def getBuilder():
    dccBuilder = None
    for eachPlugin in __all__:
        loaded_mod = __import__("rigging.beam.plugins." + eachPlugin + ".builder", fromlist=['builder'])
        reload(loaded_mod)
        loaded_class = getattr(loaded_mod, 'Builder')

        dccBuilder = loaded_class()

    if dccBuilder is None:
        print "Failed to find DCC builder. Falling back to Python builder."

        from rigging.beam.core import builder
        dccBuilder = builder.Builder(debugMode=True)

    return dccBuilder