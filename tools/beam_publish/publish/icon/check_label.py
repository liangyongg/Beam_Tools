#!/usr/bin/env python
# -*- coding: utf-8 -*-
from publish.ui.head import *

class Checklabel_yes(QLabel):

    def __init__(self):
        super(Checklabel_yes, self).__init__()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(event, qp)
        qp.end()

    def draw(self, event, qp):
        qp.setBrush(QBrush(Qt.green,Qt.SolidPattern))
        qp.drawEllipse(20,20,160,160)

class Checklabel_no(QLabel):

    def __init__(self):
        super(Checklabel_no, self).__init__()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw(event, qp)
        qp.end()

    def draw(self, event, qp):
        qp.setBrush(QBrush(Qt.red,Qt.SolidPattern))
        qp.drawEllipse(20,20,160,160)
