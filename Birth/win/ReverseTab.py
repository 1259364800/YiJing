from ui_codes import Reverse
import time
from PyQt5.QtWidgets import QWidget, QMessageBox
from utils import BaZi2Birth


def fullStr(ganZhiList):
    return ganZhiList[0] + ganZhiList[1]


def mkHourStr(hourList):
    ret = ""
    for hour in hourList:
        ret = ret + str(hour) + "/"
    return ret.strip("/")


class ReverseTab(Reverse.Ui_Form, QWidget):

    def __init__(self, callback, parent=None):
        super(ReverseTab, self).__init__(parent)
        self.setupUi(self)
        self.initUI()
        self.initSignal()
        self.year = 2000
        self.month = ["甲", "子"]
        self.day = ["甲", "子"]
        self.hour = ["甲", "子"]

        self.resultYear = None
        self.resultMonth = None
        self.resultDay = None
        self.resultHour = None

        self.callback = callback

    def initUI(self):
        pass

    def initSignal(self):
        self.spinBoxYear.valueChanged.connect(self.changeYear)
        self.comboMonthGan.currentTextChanged.connect(self.changeMonthGan)
        self.comboMonthZhi.currentTextChanged.connect(self.changeMonthZhi)
        self.comboDayGan.currentTextChanged.connect(self.changeDayGan)
        self.comboDayZhi.currentTextChanged.connect(self.changeDayZhi)
        self.comboHourGan.currentTextChanged.connect(self.changeHourGan)
        self.comboHourZhi.currentTextChanged.connect(self.changeHourZhi)
        self.btnReverse.clicked.connect(self.onBtnReverse)
        self.btnShowFigure.clicked.connect(self.onBtnShowFigure)

    def changeYear(self):
        self.year = int(self.sender().text())

    def changeMonthGan(self):
        self.month[0] = self.sender().currentText()

    def changeMonthZhi(self):
        self.month[1] = self.sender().currentText()

    def changeDayGan(self):
        self.day[0] = self.sender().currentText()

    def changeDayZhi(self):
        self.day[1] = self.sender().currentText()

    def changeHourGan(self):
        self.hour[0] = self.sender().currentText()

    def changeHourZhi(self):
        self.hour[1] = self.sender().currentText()

    def onBtnReverse(self):
        reverse = BaZi2Birth.BaZi2Birth(self.year, fullStr(self.month), fullStr(self.day), fullStr(self.hour))
        check = reverse.check()

        if check:
            QMessageBox.information(self, "提示", check, QMessageBox.Ok)
            return
        month, day, hour = reverse.search()
        if month == -1:
            QMessageBox.information(self, "提示", "月份出错,没有对应的月份！", QMessageBox.Ok)
            return
        elif day == -1:
            QMessageBox.information(self, "提示", "日期出错,没有对应的日期！", QMessageBox.Ok)
            return
        elif hour == -1:
            QMessageBox.information(self, "提示", "时辰出错,没有对应的时辰！", QMessageBox.Ok)
            return
        self.resultYear = self.year
        self.resultMonth = month
        self.resultDay = day
        self.resultHour = hour[0]
        self.lbResult.setText("倒推得到的日期为%d年%d月%d日%s时" % (self.year, month, day, mkHourStr(hour)))

    def onBtnShowFigure(self):
        if self.resultYear is None or self.resultMonth is None \
                or self.resultDay is None or self.resultHour is None:
            QMessageBox.information(self, "提示", "没有逆推返回结果！", QMessageBox.Ok)
            return
        self.callback(self.year, self.resultMonth, self.resultDay, self.resultHour)
