import traceback

class master_check():

    def __init__(self):
        self.check_name = "Inspection description information"
        self.description = "Inspection description information"
        self.auto_fix = False
        return

    def do_check(self):
        try:
            print "check ...."
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