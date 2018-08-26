# -*- coding: utf-8 -*-

import os
import sys
import functools
from rigging.check.ui.head import *
from rigging.check.ui.ui_main_window import ui_main_window
from rigging.check.ui.re_item_form import Item_form
from rigging.check.ui.re_info_form import Info_form
#from PySide import QtGui,QtCore
class From(QtWidgets.QMainWindow):

    def __init__(self,parent = None):
        super(From,self).__init__(parent)
        self._plugins_path = []
        self.item_list = []
        self.item_data = {}
        self.info_list = []
        self.cmd = None

        self.setWindowTitle ("rigging_check")
        self.setupUI()

    def setupUI (self):
        self.ui_main_window = ui_main_window ()
        self.ui_main_window.ui_check_widget.item_area_group.setStyleSheet ('QGroupBox{font-size:18px; font-weight:bold;}')
        self.ui_main_window.ui_check_widget.info_area_group.setStyleSheet ('QGroupBox{font-size:18px; font-weight:bold;}')
        self.ui_main_window.ui_check_widget.logo_label.setPixmap (os.path.join (self._get_icon_path (), 'icons/validation.png'))
        refresh_icon = QtWidgets.QIcon()
        refresh_icon.addFile(os.path.join(self._get_icon_path(), 'icons/refresh.png'))
        self.ui_main_window.ui_check_widget.refresh_btn.setIcon (refresh_icon)
        continue_icon = QtWidgets.QIcon()
        continue_icon.addFile(os.path.join(self._get_icon_path(), 'icons/gono.png'))
        self.ui_main_window.ui_check_widget.continue_btn.setIcon (continue_icon)
        run_icon = QtWidgets.QIcon()
        run_icon.addFile(os.path.join(self._get_icon_path(), 'icons/play_icon.png'))
        self.ui_main_window.ui_check_widget.run_btn.setIcon(run_icon)
        self.ui_main_window.ui_check_widget.skip_btn.setVisible (0)
        self._get_plugin_path()
        self._add_item()
        self.ui_main_window.ui_check_widget.refresh_btn.clicked.connect(self.refresh_ui)
        self.ui_main_window.ui_check_widget.continue_btn.clicked.connect(self._on_continue_btn_clicked)
        self.ui_main_window.ui_check_widget.run_btn.clicked.connect(self._on_run_btn_clicked)
        self.ui_main_window.ui_check_widget.skip_btn.clicked.connect(self._on_skip_btn_clicked)
        self.setCentralWidget (self.ui_main_window)

    def _get_plugin_path (self):
        path_str = os.getenv ('BEAM_SCRIPT_PATH')
        if not path_str:
            return
        if ';' in path_str:
            path_list = path_str.split(';')
            for path in path_list:
                if not os.path.isdir(path):
                    continue
                self._plugins_path.append(path)
        else:
            if not os.path.isdir(path_str):
                return
            self._plugins_path.append(path_str)

    def refresh_ui(self):
        self._clear_item_list()
        self._clear_info_list()
        self._add_item()

    def register_plugins_path(self, path):
        if not os.path.isdir(path):
            return
        if path in self._plugins_path:
            return
        self._plugins_path.append(path)
        self._clear_info_list()
        self._clear_item_list()
        self._add_item()

    def deregister_plugins_path(self, path):
        if not os.path.isdir(path):
            return
        if path not in self._plugins_path:
            return
        self._plugins_path.remove(path)
        self._clear_info_list()
        self._clear_item_list()
        self._add_item()

    def register_skip_command(self, cmd):
        self.cmd = cmd
        self.ui_main_window.ui_check_widget.skip_btn.setVisible(1)

    def _on_skip_btn_clicked(self):
        try:
            self.cmd()
        except:pass
        self.close()

    def register_cancle_button_command(self, cmd):
        try:
            self.ui_main_window.ui_check_widget.continue_btn.clicked.connect(cmd)
        except:
            pass

    def _on_run_btn_clicked(self):
        self._update_item_list()
        self._update_info_list()
        self.item_current_list = [item for item in self.item_list]
        self._checker_run(self.item_list)

    def _add_item(self):
        instance_list = self.get_instance ()
        if not instance_list:
            return
        for instance in instance_list:
            if hasattr (instance, 'check_name'):
                item_name = instance.check_name
                if item_name in self.item_list:
                    item_name = instance.__module__ + ':' + instance.check_name
                    if item_name in self.item_list:
                        continue
            else:
                item_name = instance.__module__
                if item_name in self.item_list:
                    continue
        item_form = Item_form ()
        item_form._ui.item_name.setText (item_name)
        self.item_list.append (item_name)
        self.item_data [item_name] = dict (instance = instance, item_form = item_form)
        item_form._ui.skip_btn.clicked.connect (
            functools.partial (self._on_item_skip_btn_clicked, item_name))
        #if correct_order:
        #    item_form._ui.correct_btn.clicked.connect (
        #        functools.partial (self._on_item_correct_btn_clicked, instance.correct))

        self.ui_main_window.ui_check_widget.item_area_layout.addWidget (item_form)

    def get_instance(self):
        module_list = self.get_module()
        instance_list = []
        index_list = []
        for module in module_list:
            if not hasattr (module, 'Rigging_Check'):
                continue
            Rigging_Check_instance = module.Rigging_Check ()
            if not hasattr (Rigging_Check_instance, 'do_check'):
                continue
            if not hasattr (Rigging_Check_instance, 'do_fix'):
                continue
            if not index_list:
                instance_list.append(Rigging_Check_instance)
        return instance_list

    def get_module(self):
        module_list = []
        plugin_path_list = self._plugins_path
        if not plugin_path_list:
            return module_list
        for plugin_path in plugin_path_list:
            if os.path.isdir (plugin_path):
                file_list = [i for i in os.listdir (plugin_path) if not i.startswith ('__') and i.endswith ('.py')]
                module_name_list = [os.path.splitext (i) [0] for i in file_list]
                sys.path.append (plugin_path)
                for name in module_name_list:
                    module = __import__ (name)
                    module_list.append (module)
        return module_list

    def _on_item_correct_btn_clicked(self, correct):
        correct()
        self._on_continue_btn_clicked()

    def _on_continue_btn_clicked(self):
        self._update_info_list()
        if not self.item_current_list:
            return
        self._checker_run(self.item_current_list)

    def _on_item_skip_btn_clicked(self, name):
        item_form = self.item_data[name].get('item_form')
        item_form.close()
        self.item_list.remove(name)
        try:
            self.item_current_list.remove(name)
        except:
            pass

    def _get_icon_path(self):
        return os.path.dirname(os.path.dirname(__file__))

    def _checker_run (self, item_list):
        if not item_list:
            return
        # cmds.refresh()
        self.refresh_ui ()
        temp_list = [item for item in item_list]
        self.ui_main_window.ui_check_widget.logging_label.setStyleSheet ('color:yellow;')
        for item in temp_list:
            self._update_info_list ()
            self.ui_main_window.ui_check_widget.logging_label.setText ("  %s is running......" % item)
            item_form = self.item_data [item].get ('item_form')
            instance = self.item_data [item].get ('instance')
            data = instance.do_check ()
            if data:
                if hasattr (instance, "correct"):
                    item_form._ui.correct_btn.setVisible (1)
                item_form._ui.item_icon.setPixmap (
                    QtWidgets.QPixmap (os.path.join (self._get_icon_path (), 'icons/failure.png')))
                item_form._ui.item_icon.setScaledContents (True)
                if not isinstance (data, dict):
                    return
                self._add_info_item (instance, data)
                self.ui_main_window.ui_check_widget.logging_label.setText ("  %s wrong !" % item)
                self._refresh_ui ()
                return
            item_form._ui.item_icon.setPixmap (
                QtWidgets.QPixmap (os.path.join (self._get_icon_path (), 'icons/success.png')))
            item_form._ui.item_icon.setScaledContents (True)
            item_form._ui.correct_btn.setVisible (0)
            self.item_current_list.remove (item)
            self.ui_main_window.ui_check_widget.logging_label.setText ("  %s ok" % item)
            self._refresh_ui ()
        # self._command()
        self.ui_main_window.ui_check_widget.logging_label.setText (u"  检查完毕")
        self.ui_main_window.ui_check_widget.skip_btn.setText ('Next')

    def _update_item_list(self):
        for item in self.item_list:
            item_form = self.item_data[item].get('item_form')
            item_form._ui.item_icon.setPixmap(
                QtWidgets.QPixmap(os.path.join(self._get_icon_path(), 'icons/clock.png')))
            item_form._ui.item_icon.setScaledContents(True)

    def _clear_item_list(self):
        for item in self.item_list:
            item_form = self.item_data[item].get('item_form')
            item_form.close()
        self.item_list = []
        self.item_current_list = []
        self.item_data = {}
        self.ui_main_window.ui_check_widget.logging_label.setText('')

    def _clear_info_list(self):
        if not self.info_list:
            return
        for info in self.info_list:
            info.close()
        self.info_list = []

    def _update_info_list(self):
        if not self.info_list:
            return
        temp_list = [item for item in self.info_list]
        for info in temp_list:
            self.info_list.remove(info)
            info.close()

    def showWinodow(self):
        self.myapp = From()
        self.myapp.show()
        return self.myapp

if __name__=="__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = From()
    ui.showWinodow()
    sys.exit(app.exec_())