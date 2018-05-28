import maya.utils as utils
import sys
#sys.path.append(r"E:\Beam_tools\tools\module")
sys.path.append(r"E:\Beam_tools\tools\toolset\application\maya\lib")
sys.path.append(r"E:\Beam_tools\tools\toolset\lib")
sys.path.append(r"E:\Beam_tools\tools\toolset\tool")
sys.path.append(r"E:\Beam_tools\tools\beam_publish")
sys.path.append(r"E:\Beam_tools\tools\toolset\tool\rigging\edward\python")
import CreateMenu
reload(CreateMenu)
utils.executeDeferred("CreateMenu.main()")