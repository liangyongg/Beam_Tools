import glob
import logging
import os
import sys

__all__ = [os.path.splitext(os.path.basename(plugin))[0]
           for path in __path__
           for plugin in glob.glob(os.path.join(path, '*_plugin'))]

def getBuilder():
    dccBuilder = None
    print "getBuilder: plugins.__init__.__all__: ", __all__
    for eachPlugin in __all__:
        mod = __import__("rigging.beam.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)
        print "getBuilder.mod: ", mod

        if mod.dccTest() is True:
            loaded_mod = __import__("rigging.beam.plugins." + eachPlugin + ".builder", fromlist=['builder'])
            reload(loaded_mod)
            print "getBuilder.loaded_mod: ", loaded_mod
            loaded_class = getattr(loaded_mod, 'Builder')

            dccBuilder = loaded_class()

    if dccBuilder is None:
        print "Failed to find DCC builder. Falling back to Python builder."

        from rigging.beam.core import builder
        dccBuilder = builder.Builder(debugMode=True)

    print "dccBuilder :", dccBuilder
    return dccBuilder

def getSynchronizer():
    dccSynchronizer = None
    print "getSynchronizer: plugins.__init__.__all__: ", __all__
    for eachPlugin in __all__:
        mod = __import__("rigging.beam.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)
        print "getSynchronizer.mod: ",mod

        if mod.dccTest () is True:
            loaded_mod = __import__ ("rigging.beam.plugins." + eachPlugin + ".synchronizer", fromlist = ['synchronizer'])
            reload (loaded_mod)
            print "getSynchronizer.loaded_mod: ", loaded_mod
            loaded_class = getattr (loaded_mod, 'Synchronizer')

            dccSynchronizer = loaded_class ()

    if dccSynchronizer is None:
        print "Failed to find DCC Synchronizer. Falling back to Python Synchronizer."
        from rigging.beam.core import synchronizer
        dccSynchronizer = synchronizer.Synchronizer ()

    print "getSynchronizer.dccSynchronizer: ",dccSynchronizer
    return dccSynchronizer

def getFabricClient():
    """Returns the appropriate Fabric client for the DCC.

    Args:
        Arguments (Type): information.

    Returns:
        Type: True if successful.

    """

    client = None

    for eachPlugin in __all__:
        mod = __import__("rigging.beam.plugins." + eachPlugin, fromlist=['dccTest'])
        reload(mod)

        if mod.dccTest() is True:
            loaded_mod = __import__("rigging.beam.plugins." + eachPlugin + ".fabric_client", fromlist=['getClient'])
            reload(loaded_mod)

            client = loaded_mod.getClient()

    if client is None:
        print "Failed to find DCC client. Falling back to Python client."

    return client