"""Maya Plug-in."""

import os


def dccTest():
    """

    .. note::
        The variable value to activate the Maya plugin is: `Maya`.

    Returns:
        bool: True if the environment variable is set to use this plugin.

    """

    #beamDCC = os.environ.get('BEAM_DCC')
    #if beamDCC == "Maya":
    #    return True
    #else:
    #    return False
    return True
