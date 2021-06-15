from ui_codes import YiJing
from utils import DealData, DrawLines, DrawPie, DrawRadar, NormalBirth, DealSql
from win import RecordTab, ReverseTab

from PyQt5.QtWidgets import QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QHeaderView
from PyQt5.QtCore import Qt
from datetime import datetime


#   调整header的一些格式
def setHeaderFormat(header: QTableWidgetItem, fontSize=None):
    header.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    if fontSize:
        font = header.font()
        font.setPointSize(fontSize)
        header.setFont(font)
    return header


class YiJingWin(YiJing.Ui_YiJing, QMainWindow):

    def __init__(self, parent=None):
        super(YiJingWin, self).__init__(parent)
        self.setupUi(self)

        #   初始化的一些工作
        self.clicked = False
        self.clickYear, self.clickMonth = 0, 0  # 点击曲线图上的某点
        #   初始年份2000年
        self.spinYear.setValue(2000)
        self.originYear = 2000
        hour = 0
        province = '北京市'
        city = '北京市'
        self.birthInfo = NormalBirth.NormalBirth(NormalBirth.TimeInfo(2000, 1, 1, hour), True, province, city, 0)
        self.initClick()
        self.initUI()

    def initClick(self):
        #   pushbutton事件
        self.btnChangeWeight.clicked.connect(self.onBtnChangeWeight)
        self.btnCalculate.clicked.connect(self.onBtnCalculate)
        self.btnReset.clicked.connect(self.onBtnReset)
        self.btnSave.clicked.connect(self.onBtnSave)
        #   combobox事件
        self.spinYear.valueChanged.connect(self.changeYear)
        self.comboMonth.currentIndexChanged.connect(self.changeMonth)
        self.comboDay.currentIndexChanged.connect(self.changeDay)
        self.comboTime.currentIndexChanged.connect(self.changeHour)
        self.comboProvince.currentIndexChanged.connect(self.changeProvince)
        self.comboCity.currentIndexChanged.connect(self.changeCity)
        self.comboCounty.currentIndexChanged.connect(self.changeCounty)
        self.comboElems.currentIndexChanged.connect(self.changeElems)
        self.comboSex.currentIndexChanged.connect(self.changeSex)
        #   radiobutton事件
        self.radBtnBeiJingTime.toggled.connect(self.onBtnBeiJingTime)
        self.radBtnZoneTime.toggled.connect(self.onBtnZoneTime)
        self.radBtnSolar.toggled.connect(self.onBtnSolar)
        self.radBtnLunar.toggled.connect(self.onBtnLunar)

    def initUI(self):
        #
        self.tabWidget.addTab(RecordTab.RecordTab(self.loadSqlCallback), "读取")
        self.tabWidget.addTab(ReverseTab.ReverseTab(self.reverseCallback), "倒推")
        #   绘图控件
        self.lineArea = DrawLines.DrawLines(callback=self.clickOnLine)
        self.radarArea = DrawRadar.DrawRadar()
        self.pieArea = DrawPie.DrawPie()
        self.boxLines.addWidget(self.lineArea)
        self.boxRadar.addWidget(self.radarArea)
        self.boxPie.addWidget(self.pieArea)
        #   初始化表格
        self.initTableView()
        #   添加省份信息
        provinces = DealData.getProvinceInfo()
        for province in provinces:
            self.comboProvince.addItem(province)
        self.showWeights()

    def initTableView(self):
        #   禁止编辑
        self.tblOverview.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tblDetail.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #   终生四柱,位置为（0,0）
        self.tblOverview.setSpan(0, 0, 3, 1)
        header1 = QTableWidgetItem('终 生\n\n四 柱')
        header1 = setHeaderFormat(header1, 12)
        self.tblOverview.setItem(0, 0, header1)
        #   年月日时，位置为（0,1）
        self.tblOverview.setSpan(0, 1, 3, 21)
        header2 = QTableWidgetItem('年\t月\t日\t时\n')
        header2 = setHeaderFormat(header2, 12)
        self.tblOverview.setItem(0, 1, header2)
        #   大运：人生各阶段，位置为（3,0）
        self.tblOverview.setSpan(3, 0, 2, 1)
        header3 = QTableWidgetItem('大运：人生各阶段')
        header3 = setHeaderFormat(header3, 12)
        self.tblOverview.setItem(3, 0, header3)
        #   各阶段所含流年，位置为（5,0）
        self.tblOverview.setSpan(5, 0, 12, 1)
        header4 = QTableWidgetItem('各\n阶\n段\n所\n含\n流\n年')
        header4 = setHeaderFormat(header4, 12)
        self.tblOverview.setItem(5, 0, header4)
        #   调整单元格大小
        for i in range(1, self.tblOverview.columnCount() + 1):
            self.tblOverview.setSpan(3, i, 2, 2)
            self.tblOverview.setSpan(5, i, 2, 2)
        #   初始化格
        for i in range(1, self.tblOverview.columnCount()):
            self.tblOverview.setItem(3, i, setHeaderFormat(QTableWidgetItem("")))
            self.tblOverview.setItem(5, i, setHeaderFormat(QTableWidgetItem("")))
            for j in range(10):
                self.tblOverview.setItem(7 + j, i, setHeaderFormat(QTableWidgetItem("")))

        for i in range(1, self.tblDetail.rowCount()):
            for j in range(1, self.tblDetail.columnCount()):
                self.tblDetail.setItem(i, j, setHeaderFormat(QTableWidgetItem("")))

        self.tblOverview.itemClicked.connect(self.onClickOverview)
        self.tblDetail.itemClicked.connect(self.onClickDetail)

    def onClickOverview(self, item: QTableWidgetItem):
        data = item.data(100)
        if data is not None:
            self.clickYear = data[0].getYear()
            self.refreshDetail(data)
            nianGanZhi = data[0].getGanZhi()
            self.labelDaYun.setText("%s、%s、%s" % (data[1], nianGanZhi, ""))

    def onClickDetail(self, item: QTableWidgetItem):
        if self.clickYear == 0:
            return
        row = item.row()
        year = self.clickYear
        if row > 0:
            self.clickMonth = row
            self.clickOnLine("%d-%d" % (year, row))

    def clickOnLine(self, time):
        try:
            year, month = time.split('-')
        except  Exception:
            return
        year = int(year)
        month = int(month)
        self.clickYear, self.clickMonth = year, month
        self.clicked = True
        if not self.birthInfo.clickCheck(year):
            return
        self.refreshAfterClick(year, month)

    def refreshAfterClick(self, year, month):
        daYunGanZhi = self.birthInfo.getDaYunGanZhi(year, month)
        self.labelDaYun.setText("%s、%s、%s" % (daYunGanZhi["大运"], daYunGanZhi["流年"], daYunGanZhi["流月"]))
        # 绘图
        self.drawRadar(True)
        self.drawPie()
        # 设置表格
        ganZhi = None
        targetNian = None
        for yun in self.birthInfo.daYun:
            if yun.getStartYear() <= self.clickYear <= yun.getEndYear():
                ganZhi = yun.getGanZhi()
                liuNian = yun.getLiuNian()
                targetNian = liuNian[year - yun.getStartYear()]
                break
        data = (targetNian, ganZhi)
        self.refreshDetail(data)

    def refreshOverview(self):
        #   设置年月日时
        header = self.tblOverview.item(0, 1)
        ganZhiDict = self.birthInfo.getBirthGanZhi()
        header.setText('年\t月\t日\t时\n%s\t%s\t%s\t%s\n%s\t%s\t%s\t%s\n' % (
            DealData.getGan(ganZhiDict["年"]), DealData.getGan(ganZhiDict["月"]),
            DealData.getGan(ganZhiDict["日"]), DealData.getGan(ganZhiDict["时"]),
            DealData.getZhi(ganZhiDict["年"]), DealData.getZhi(ganZhiDict["月"]),
            DealData.getZhi(ganZhiDict["日"]), DealData.getZhi(ganZhiDict["时"])
        ))
        #   设置大运
        self.birthInfo.getDaYun()
        daYun = self.birthInfo.daYun
        length = len(daYun)

        self.tblOverview.item(3, 1).setText("")
        self.tblOverview.item(5, 1).setText("")
        for i in range(0, 10):
            self.tblOverview.item(7 + i, 1).setText("")
            self.tblOverview.item(7 + i, 1).setData(100, None)
            self.tblOverview.item(7 + i, 2).setText("")
            self.tblOverview.item(7 + i, 2).setData(100, None)
        for i in range(0, length):
            yun = daYun[i]
            if i == 0:
                yunGanZhiStr = "从出生开始算起的大运"
                startYearAge = "从%d年\n%d岁开始" % (yun.getStartYear(), yun.getStartAge())
            else:
                yunGanZhiStr = "%s\n10年状态" % yun.getGanZhi()
                startYearAge = "从%d年\n%d岁开始" % (yun.getStartYear(), yun.getStartAge())
            self.tblOverview.item(3, i * 2 + 1).setText(yunGanZhiStr)
            self.tblOverview.item(5, i * 2 + 1).setText(startYearAge)
            liuNian = yun.getLiuNian()
            for j in range(len(liuNian)):
                year = liuNian[j].getYear()
                liuNianStr = "%d %s" % (liuNian[j].getYear(), liuNian[j].getGanZhi())
                specStr = ""
                for specType in self.birthInfo.specData:
                    if year in self.birthInfo.specData[specType].keys():
                        specStr = specStr + specType + " "
                self.tblOverview.item(7 + j, i * 2 + 1).setText(liuNianStr)
                self.tblOverview.item(7 + j, i * 2 + 2).setText(specStr)
                self.tblOverview.item(7 + j, i * 2 + 1).setData(100, (liuNian[j], yun.getGanZhi()))
                self.tblOverview.item(7 + j, i * 2 + 2).setData(100, (liuNian[j], yun.getGanZhi()))

    def refreshDetail(self, data):
        numAttributes = self.getNumAttributes()
        liuNian = data[0]
        yunGanZhi = data[1]
        self.lbDetailYear.setText("%d年" % liuNian.getYear())
        nianGanZhi = liuNian.getGanZhi()
        liuYue = liuNian.getLiuYue()
        for i in range(1, self.tblDetail.rowCount()):
            daYunGanZhi = DealData.mergeDict(self.birthInfo.getBirthGanZhi(),
                                             self.birthInfo.getDaYunGanZhi(liuNian.getYear(),
                                                                           liuYue[i - 1].getIndex() + 1))
            yueGanZhi = liuYue[i - 1].getGanZhi()
            self.tblDetail.item(i, 1).setText(yunGanZhi)
            self.tblDetail.item(i, 2).setText(nianGanZhi)
            self.tblDetail.item(i, 3).setText(yueGanZhi)
            scores = DealData.calculateElemScore(daYunGanZhi, numAttributes)
            self.tblDetail.item(i, 4).setText(str(scores["金"]))
            self.tblDetail.item(i, 5).setText(str(scores["木"]))
            self.tblDetail.item(i, 6).setText(str(scores["水"]))
            self.tblDetail.item(i, 7).setText(str(scores["火"]))
            if numAttributes == 5:
                self.tblDetail.item(i, 8).setText(str(scores["土"]))

    def onBtnChangeWeight(self):
        numAttributes = self.getNumAttributes()
        try:
            params = {"年": float(self.editYearWight.toPlainText()),
                      "月": float(self.editMonthWeight.toPlainText()),
                      "日": float(self.editDayWeight.toPlainText()),
                      "时": float(self.editHourWeight.toPlainText()),
                      "大运": float(self.editDaYunWeight.toPlainText()),
                      "流年": float(self.editLiuNianWeight.toPlainText()),
                      "流月": float(self.editLiuYueWeight.toPlainText())}
        except Exception:
            QMessageBox.information(self, "错误", "权重数字输入不正确！", QMessageBox.Ok)
            return
        else:
            DealData.changeWeightsByAttribute(numAttributes, params)
            self.showWeights()

    def onBtnCalculate(self):
        #   更新表格信息
        self.refreshOverview()
        #   生辰八字
        birthGanZhi = self.birthInfo.getBirthGanZhi()
        self.labelBaZi.setText("%s年 %s月 %s日 %s时" % (birthGanZhi["年"], birthGanZhi["月"],
                                                    birthGanZhi["日"], birthGanZhi["时"]))
        #   绘图
        self.drawRadar(False)
        self.drawPie()
        self.drawLine()

    def onBtnSave(self):
        name = self.editName.toPlainText()
        if name.strip('\n') == '':
            QMessageBox.information(self, "错误", "未输入姓名！", QMessageBox.Ok)
            return
        curTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sex = self.birthInfo.sex
        birth = self.birthInfo.beiJingTime
        birthTime = datetime(birth.year, birth.month, birth.day, birth.hour, 0, 0).strftime('%Y-%m-%d %H:%M:%S')

        sqlOp = DealSql.SqlOp('./data/data.db')
        sqlOp.connect()
        insert = "INSERT INTO base_info VALUES ('%s', '%s', '%s', %d)" % (curTime, birthTime, name, sex)
        sqlOp.execNonQuery(insert)
        sqlOp.closeDB()
        QMessageBox.information(self, "提示", "保存成功！", QMessageBox.Ok)

    def loadSqlCallback(self, info):
        self.tabWidget.setCurrentIndex(0)
        birthDate = datetime.strptime(info[1], "%Y-%m-%d %H:%M:%S")
        year = birthDate.year
        month = birthDate.month
        day = birthDate.day
        hour = birthDate.hour
        self.setTimeAndRefresh(year, month, day, hour, info[3], info[2])

    def reverseCallback(self, year, month, day, hour):
        self.tabWidget.setCurrentIndex(0)
        self.setTimeAndRefresh(year, month, day, hour)

    def setTimeAndRefresh(self, year, month, day, hour, sex=0, name=""):
        self.spinYear.setValue(year)
        self.comboMonth.setCurrentIndex(month - 1)
        self.comboDay.setCurrentIndex(day - 1)
        self.comboTime.setCurrentIndex(hour)
        self.comboSex.setCurrentIndex(sex)
        self.editName.setText(name)
        self.radBtnLunar.setChecked(False)
        self.radBtnSolar.setChecked(True)
        self.onBtnCalculate()

    def drawRadar(self, drawDaYun=False):
        numAttributes = self.getNumAttributes()
        daYunScore = None
        dateStr = None
        if drawDaYun:
            if not self.clickYear:
                return
            daYunGanZhi = DealData.mergeDict(self.birthInfo.getBirthGanZhi(),
                                             self.birthInfo.getDaYunGanZhi(self.clickYear, self.clickMonth))
            daYunScore = DealData.calculateElemScore(daYunGanZhi, numAttributes)
        birthGanZhi = self.birthInfo.getBirthGanZhi()
        birthScore = DealData.calculateElemScore(birthGanZhi, numAttributes)
        self.radarArea.drawRadar(numAttributes, DealData.dict2List(daYunScore), DealData.dict2List(birthScore), dateStr)

    def drawPie(self):
        finGanZhi = self.birthInfo.getBirthGanZhi()
        if self.clicked:
            daYunGanZhi = self.birthInfo.getDaYunGanZhi(self.clickYear, self.clickMonth)
            finGanZhi = DealData.mergeDict(finGanZhi, daYunGanZhi)
        self.pieArea.drawPie(finGanZhi, None, self.getNumAttributes())

    def drawLine(self):
        numAttributes = self.getNumAttributes()
        scoreDict, dates = self.birthInfo.calculateLineScore(numAttributes)
        dates = DealData.formatDateTime(dates)
        specPoints = self.birthInfo.specData
        self.lineArea.drawLines(dates, scoreDict, specPoints, numAttributes)

    def onBtnReset(self):
        self.clicked = False
        self.drawRadar(False)
        self.drawPie()

    def resetTime(self):
        self.spinYear.setValue(2000)
        self.comboMonth.setCurrentIndex(0)
        self.comboDay.setCurrentIndex(0)

    def dateWrongCheck(self, error):
        if error:
            msg = QMessageBox.information(self, "错误", "不存在该日期，请重新选择！", QMessageBox.Ok)
            if msg == QMessageBox.Ok:
                self.resetTime()

    def changeYear(self):
        error = self.birthInfo.changeYear(int(self.sender().value()))
        self.dateWrongCheck(error)

    def changeMonth(self):
        error = self.birthInfo.changeMonth(int(self.sender().currentIndex() + 1))
        self.dateWrongCheck(error)

    def changeDay(self):
        error = self.birthInfo.changeDay(int(self.sender().currentIndex() + 1))
        self.dateWrongCheck(error)

    def changeHour(self):
        self.birthInfo.changeHour(int(self.sender().currentIndex()))

    def changeProvince(self):
        province = self.sender().currentText()
        self.birthInfo.changeProvince(province)
        self.comboCity.clear()
        provinces = DealData.getProvinceInfo()
        for city in provinces[province]:
            self.comboCity.addItem(city)

    def changeCity(self):
        province = self.birthInfo.province
        city = self.sender().currentText()
        if city == '':
            return
        self.birthInfo.changeCity(city)
        provinces = DealData.getProvinceInfo()
        self.comboCounty.clear()
        self.comboCounty.addItems(provinces[province][city])

    def changeCounty(self):
        county = self.sender().currentText()

    def changeElems(self):
        self.showWeights()

    def changeSex(self):
        index = self.sender().currentIndex()
        self.birthInfo.changeSex(index)

    def onBtnBeiJingTime(self):
        if self.sender().isChecked():
            self.birthInfo.setUseZoneTime(False)

    def onBtnZoneTime(self):
        if self.sender().isChecked():
            self.birthInfo.setUseZoneTime(True)

    def onBtnSolar(self):
        if self.sender().isChecked():
            error = self.birthInfo.changeSolar(True)
            self.dateWrongCheck(error)

    def onBtnLunar(self):
        if self.sender().isChecked():
            error = self.birthInfo.changeSolar(False)
            self.dateWrongCheck(error)

    def showWeights(self):
        numAttributes = self.getNumAttributes()
        weights = DealData.getWeightsByAttribute(numAttributes)
        self.lbYearWeight.setText(str(weights["年"]))
        self.lbMonthWeight.setText(str(weights["月"]))
        self.lbDayWeight.setText(str(weights["日"]))
        self.lbHourWeight.setText(str(weights["时"]))
        self.lbDaYunWeight.setText(str(weights["大运"]))
        self.lbLiuNianWeight.setText(str(weights["流年"]))
        self.lbLiuYueWeight.setText(str(weights["流月"]))

    def getNumAttributes(self):
        return int(self.comboElems.currentText())
