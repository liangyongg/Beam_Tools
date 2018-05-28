import traceback
try:
    import maya.cmds as cmds
    tool_in_app="maya"
except:
    pass

try:
    import nuke
    tool_in_app="nuke"
except:
    pass

class master_check():

    def __init__(self):
        self.check_name = "Inspection description information"
        self.description = "Inspection description information"
        self.auto_fix = False
        return

    def do_check(self):
        try:
            publish_info_tex=self.publish_widget.publish_info_plainTextEdit.toPlainText()
            if not publish_info_tex:
                if tool_in_app == "nuke":
                    return "Need to fill in the release information,Explain what is updated in this version"
                return "Need to fill in the release information,Explain what is updated in this version"
            return ""
        except:
            return traceback.format_exc()

    def do_fix(self):
        return

    def get_check_name(self):
        return self.check_name

    def get_description(self):
        return self.description

    def get_auto_fix(self):
        return self.auto_fix