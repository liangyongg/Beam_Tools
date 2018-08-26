import rigging.beam.FabricEngine.Core

from rigging.beam.log.utils import fabricCallback
from rigging.beam.plugins.maya_plugin.utils import *


def getClient():
    """Gets the Fabric client from the DCC. This ensures that the same client
    is used, instead of a new one being created each time one is requiredself.

    Returns:
        Fabric Client.

    """

    client = None
    #contextID = pm.FabricCanvasGetContextID()
    #print "contextID",contextID
    #if contextID == '':
    #    raise ValueError('Kraken Maya could not construct a client!')

    options = {
        'reportCallback': fabricCallback,
        'guarded': True
    }

    client = rigging.beam.FabricEngine.Core.createClient(options)

    return client