# import sys
#
# from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QTableWidgetItem, QAbstractItemView, QWidget
# from PyQt5.QtCore import QDate, Qt
# from PyQt5.QtGui import QIntValidator
#
# import util
# import birth
#
#
# #   调整header的一些格式
# def setHeaderFormat(header: QTableWidgetItem, fontSize=None):
#     header.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
#     if fontSize:
#         font = header.font()
#         font.setPointSize(fontSize)
#         header.setFont(font)
#     return header
#
#
# class Birth(birth.Ui_MainWindow, QMainWindow):
#
#     def __init__(self, parent=None):
#         super(Birth, self).__init__(parent)
#         self.setupUi(self)
#
#         #   数据初始化
#         self.click_year, self.click_month = 0, 0
#         init_year = QDate(2000, 1, 1)
#         self.birth_edit.setDate(init_year)
#         self.origin_date = init_year
#         hour = 0
#         province = '北京市'
#         city = '北京市'
#         self.birthInfo = util.BirthInfo(util.DateTime(init_year.year(), init_year.month(),
#                                                       init_year.day(), hour), True, province, city, 1)
#
#         self.clicked = False
#         self.fig = '雷达图'
#         self.setBaZi()
#         self.setClick()
#         self.setOtherUI()
#         self.drawByFig(self.clicked)
#         self.refreshOverview()
#
#     def afterChange(self):
#         self.setBaZi()
#         self.birthInfo.getDaYun()
#         self.clicked = False
#         self.click_year = 0
#         self.click_month = 0
#         self.drawByFig(self.clicked)
#         self.birthInfo.search()
#         self.judge()
#         self.refreshOverview()
#
#     def setOtherUI(self):
#         self.radar_area = util.RadarFigure()
#         self.vbox_radar.addWidget(self.radar_area)
#         self.line_area = util.LineFigure(callback=self.clickOnLine)
#         self.hbox_line.addWidget(self.line_area)
#         self.info_widget.setStyleSheet('background-color:white')
#         #
#         self.lb_detail_date.setStyleSheet('background-color:white')
#         self.initTableView()
#
#         #   添加省
#         for province in util.province_dict:
#             self.combo_province.addItem(province)
#
#         #   限制输入范围
#         self.edt_year.setValidator(QIntValidator(0, 65535))
#         self.edt_month.setValidator(QIntValidator(0, 65535))
#         self.edt_day.setValidator(QIntValidator(0, 65535))
#         self.edt_hour.setValidator(QIntValidator(0, 65535))
#         self.edt_da_yun.setValidator(QIntValidator(0, 65535))
#         self.edt_liu_nian.setValidator(QIntValidator(0, 65535))
#         self.edt_liu_yue.setValidator(QIntValidator(0, 65535))
#         self.showWeights()
#
#     def initTableView(self):
#         #   禁止编辑
#         self.tbl_overview.setEditTriggers(QAbstractItemView.NoEditTriggers)
#         self.tbl_detail.setEditTriggers(QAbstractItemView.NoEditTriggers)
#         #   终生四柱,位置为（0,0）
#         self.tbl_overview.setSpan(0, 0, 3, 1)
#         header1 = QTableWidgetItem('终 生\n\n四 柱')
#         header1 = setHeaderFormat(header1, 12)
#         self.tbl_overview.setItem(0, 0, header1)
#         #   年月日时，位置为（0,1）
#         self.tbl_overview.setSpan(0, 1, 3, 21)
#         header2 = QTableWidgetItem('年\t月\t日\t时\n')
#         header2 = setHeaderFormat(header2, 12)
#         self.tbl_overview.setItem(0, 1, header2)
#         #   大运：人生各阶段，位置为（3,0）
#         self.tbl_overview.setSpan(3, 0, 2, 1)
#         header3 = QTableWidgetItem('大运：人生各阶段')
#         header3 = setHeaderFormat(header3, 12)
#         self.tbl_overview.setItem(3, 0, header3)
#         #   各阶段所含流年，位置为（5,0）
#         self.tbl_overview.setSpan(5, 0, 12, 1)
#         header4 = QTableWidgetItem('各\n阶\n段\n所\n含\n流\n年')
#         header4 = setHeaderFormat(header4, 12)
#         self.tbl_overview.setItem(5, 0, header4)
#         #   调整单元格大小
#         for i in range(1, self.tbl_overview.columnCount() + 1):
#             self.tbl_overview.setSpan(3, i, 2, 2)
#             self.tbl_overview.setSpan(5, i, 2, 2)
#         #   初始化格
#         for i in range(1, self.tbl_overview.columnCount()):
#             self.tbl_overview.setItem(3, i, setHeaderFormat(QTableWidgetItem("")))
#             self.tbl_overview.setItem(5, i, setHeaderFormat(QTableWidgetItem("")))
#             for j in range(10):
#                 self.tbl_overview.setItem(7 + j, i, setHeaderFormat(QTableWidgetItem("")))
#
#         for i in range(1, self.tbl_detail.rowCount()):
#             for j in range(1, self.tbl_detail.columnCount()):
#                 self.tbl_detail.setItem(i, j, setHeaderFormat(QTableWidgetItem("")))
#
#         self.tbl_overview.itemClicked.connect(self.onClickOverview)
#         self.tbl_detail.itemClicked.connect(self.onClickDetail)
#
#     def onClickOverview(self, item: QTableWidgetItem):
#         data = item.data(100)
#         if data is not None:
#             data = item.data(100)
#             self.refreshDetail(data)
#
#     def onClickDetail(self, item: QTableWidgetItem):
#         year_str = self.lb_detail_date.text()
#         if year_str == "":
#             return
#         row = item.row()
#         year = int(year_str.split("年")[0])
#         if row > 0:
#             self.clickOnLine("%d-%d" % (year, row))
#
#     def refreshOverview(self):
#         #   设置年月日时
#         header = self.tbl_overview.item(0, 1)
#         gan_zhi_dict = self.birthInfo.getDateGanZhi()
#         header.setText('年\t月\t日\t时\n%s\t%s\t%s\t%s\n%s\t%s\t%s\t%s\n' % (
#             util.getGan(gan_zhi_dict["年"]), util.getGan(gan_zhi_dict["月"]),
#             util.getGan(gan_zhi_dict["日"]), util.getGan(gan_zhi_dict["时"]),
#             util.getZhi(gan_zhi_dict["年"]), util.getZhi(gan_zhi_dict["月"]),
#             util.getZhi(gan_zhi_dict["日"]), util.getZhi(gan_zhi_dict["时"])
#         ))
#         #   设置大运
#         da_yun = self.birthInfo.daYun
#         length = len(da_yun)
#
#         self.tbl_overview.item(3, 1).setText("")
#         self.tbl_overview.item(5, 1).setText("")
#         for i in range(0, 10):
#             self.tbl_overview.item(7 + i, 1).setText("")
#             self.tbl_overview.item(7 + i, 1).setData(100, None)
#             self.tbl_overview.item(7 + i, 2).setText("")
#             self.tbl_overview.item(7 + i, 2).setData(100, None)
#         for i in range(0, length):
#             yun = da_yun[i]
#             if i == 0:
#                 yun_gan_zhi_str = "从出生开始算起的大运"
#                 start_year_age = "从%d年\n%d岁开始" % (yun.getStartYear(), yun.getStartAge())
#             else:
#                 yun_gan_zhi_str = "%s\n10年状态" % yun.getGanZhi()
#                 start_year_age = "从%d年\n%d岁开始" % (yun.getStartYear(), yun.getStartAge())
#             self.tbl_overview.item(3, i * 2 + 1).setText(yun_gan_zhi_str)
#             self.tbl_overview.item(5, i * 2 + 1).setText(start_year_age)
#             liu_nian = yun.getLiuNian()
#             for j in range(len(liu_nian)):
#                 year = liu_nian[j].getYear()
#                 liu_nian_str = "%d %s" % (liu_nian[j].getYear(), liu_nian[j].getGanZhi())
#                 spec_str = ""
#                 if year in self.birthInfo.san_he.keys():
#                     spec_str += "三合 "
#                 if year in self.birthInfo.fan_gong.keys():
#                     spec_str += "反拱 "
#                 if year in self.birthInfo.dui_chong.keys():
#                     spec_str += "对冲 "
#                 if year in self.birthInfo.fu_yin.keys():
#                     spec_str += "复吟"
#                 self.tbl_overview.item(7 + j, i * 2 + 1).setText(liu_nian_str)
#                 self.tbl_overview.item(7 + j, i * 2 + 2).setText(spec_str)
#                 self.tbl_overview.item(7 + j, i * 2 + 1).setData(100, (liu_nian[j], yun.getGanZhi()))
#                 self.tbl_overview.item(7 + j, i * 2 + 2).setData(100, (liu_nian[j], yun.getGanZhi()))
#
#     def refreshDetail(self, data):
#         liu_nian = data[0]
#         yun_gan_zhi = data[1]
#         self.lb_detail_date.setText("%d年" % liu_nian.getYear())
#         nian_gan_zhi = liu_nian.getGanZhi()
#         liu_yue = liu_nian.getLiuYue()
#         for i in range(1, self.tbl_detail.rowCount()):
#             da_yun_gan_zhi = util.mergeDict(self.birthInfo.getDateGanZhi(),
#                                             self.birthInfo.getDaYunGanZhi(liu_nian.getYear(),
#                                                                           liu_yue[i - 1].getIndex() + 1))
#
#             yue_gan_zhi = liu_yue[i - 1].getGanZhi()
#             self.tbl_detail.item(i, 1).setText(yun_gan_zhi)
#             self.tbl_detail.item(i, 2).setText(nian_gan_zhi)
#             self.tbl_detail.item(i, 3).setText(yue_gan_zhi)
#             scores = util.calculateElmScore(da_yun_gan_zhi)
#             self.tbl_detail.item(i, 4).setText(str(scores["金"]))
#             self.tbl_detail.item(i, 5).setText(str(scores["木"]))
#             self.tbl_detail.item(i, 6).setText(str(scores["水"]))
#             self.tbl_detail.item(i, 7).setText(str(scores["火"]))
#
#     def showWeights(self):
#         weights_str = "当前权重为："
#         for key in util.score_weights:
#             tmp_str = "%s：%d，" % (key, util.score_weights[key])
#             weights_str += tmp_str
#         self.lb_weights.setText(weights_str)
#
#     def clickOnLine(self, time):
#         year, month = time.split('-')
#         self.click_year, self.click_month = int(year), int(month)
#         self.clicked = True
#         check = self.clickCheck(self.click_year)
#         if check == QMessageBox.Ok:
#             return
#         self.setYun(int(year), int(month))
#         self.drawByFig(self.clicked)
#
#         gan_zhi = None
#         target_nian = None
#         for yun in self.birthInfo.daYun:
#             if yun.getStartYear() <= self.click_year <= yun.getEndYear():
#                 gan_zhi = yun.getGanZhi()
#                 liu_nian = yun.getLiuNian()
#                 for nian in liu_nian:
#                     if self.click_year == nian.getYear():
#                         target_nian = nian
#                         break
#         data = (target_nian, gan_zhi)
#         self.refreshDetail(data)
#
#     def check(self, year):
#         if int(year) < 1900 or int(year) > 2099:
#             msg = QMessageBox.information(self, "错误", "该软件仅支持1900年-2099年的查询！", QMessageBox.Ok)
#             return msg
#         else:
#             return None
#
#     def drawRadar(self, drawDaYun=False):
#         da_yun_lst = None
#         date_str = None
#         if drawDaYun:
#             if not self.click_year:
#                 return
#             da_yun_gan_zhi = util.mergeDict(self.birthInfo.getDateGanZhi(),
#                                             self.birthInfo.getDaYunGanZhi(self.click_year, self.click_month))
#             da_yun_score = util.calculateElmScore(da_yun_gan_zhi)
#             da_yun_lst = [da_yun_score['木'], da_yun_score['火'], da_yun_score['金'], da_yun_score['水']]
#             date_str = "%d年%d月" % (self.click_year, self.click_month)
#         birth_gan_zhi = self.birthInfo.getDateGanZhi()
#         birth_score = util.calculateElmScore(birth_gan_zhi)
#         birth_lst = [birth_score['木'], birth_score['火'], birth_score['金'], birth_score['水']]
#         self.radar_area.drawRadar(da_yun_lst, birth_lst, date_str)
#
#     def drawPie(self):
#         if self.clicked:
#             da_yun_gan_zhi = util.mergeDict(self.birthInfo.getDateGanZhi(),
#                                             self.birthInfo.getDaYunGanZhi(self.click_year, self.click_month))
#         else:
#             da_yun_gan_zhi = self.birthInfo.getDateGanZhi()
#         self.radar_area.drawPie(da_yun_gan_zhi, "%d年%d月" % (self.click_year, self.click_month))
#
#     def setClick(self):
#         self.combo_isSolar.currentIndexChanged.connect(self.chooseSolar)
#         self.combo_province.currentIndexChanged.connect(self.chooseProvince)
#         self.combo_city.currentIndexChanged.connect(self.chooseCity)
#         self.combo_county.currentIndexChanged.connect(self.chooseCounty)
#         self.birth_edit.dateChanged.connect(self.chooseDate)
#         self.combo_hour.currentIndexChanged.connect(self.changeHour)
#         self.combo_sex.currentIndexChanged.connect(self.changeSex)
#         self.btn_change_weights.clicked.connect(self.changeWeights)
#         self.combobox_change_fig.currentTextChanged.connect(self.changeFig)
#         self.btn_reset.clicked.connect(self.reset)
#         self.btn_birth.clicked.connect(self.onBtnBirth)
#
#     def reset(self):
#         pass
#
#     def onBtnBirth(self):
#         self.clicked = False
#         self.drawByFig(self.clicked)
#
#     def changeFig(self, text):
#         self.fig = text
#         self.drawByFig(self.clicked)
#
#     def drawByFig(self, drawDaYun=False):
#         if self.fig == "雷达图":
#             self.drawRadar(drawDaYun)
#         else:
#             self.drawPie()
#
#     def changeWeights(self):
#         util.score_weights["年"] = util.score_weights["年"] if self.edt_year.text() == "" else int(self.edt_year.text())
#         util.score_weights["月"] = util.score_weights["月"] if self.edt_month.text() == "" else int(self.edt_month.text())
#         util.score_weights["日"] = util.score_weights["日"] if self.edt_day.text() == "" else int(self.edt_day.text())
#         util.score_weights["时"] = util.score_weights["时"] if self.edt_hour.text() == "" else int(self.edt_hour.text())
#         util.score_weights["大运"] = util.score_weights["大运"] if self.edt_da_yun.text() == "" else int(
#             self.edt_da_yun.text())
#         util.score_weights["流年"] = util.score_weights["流年"] if self.edt_liu_nian.text() == "" else int(
#             self.edt_liu_nian.text())
#         util.score_weights["流月"] = util.score_weights["流月"] if self.edt_liu_yue.text() == "" else int(
#             self.edt_liu_yue.text())
#         self.showWeights()
#         self.judge()
#         self.drawByFig(True)
#
#     def chooseSolar(self):
#         text = self.sender().currentText()
#         self.birthInfo.changeSolar(True if text == '阳历' else False)
#         self.afterChange()
#
#     def chooseProvince(self):
#         province = self.sender().currentText()
#         self.birthInfo.changeProvince(province)
#         self.combo_city.clear()
#         for city in util.province_dict[province]:
#             self.combo_city.addItem(city)
#
#     def chooseCity(self):
#         province = self.combo_province.currentText()
#         city = self.sender().currentText()
#         self.birthInfo.changeCity(city)
#         self.judge()
#         self.refreshOverview()
#         if city == '':
#             return
#         self.combo_county.clear()
#         self.combo_county.addItems(util.province_dict[province][city])
#
#     def chooseCounty(self):
#         county = self.sender().currentText()
#
#     def chooseDate(self, date: QDate):
#         check = self.check(date.year())
#         if check == QMessageBox.Ok:
#             self.birth_edit.setDate(self.origin_date)
#             return
#         self.birthInfo.birth_time.changeYear(date.year())
#         self.birthInfo.birth_time.changeMonth(date.month())
#         self.birthInfo.birth_time.changeDay(date.day())
#         self.birthInfo.changeDateTime()
#         self.origin_date = date
#         self.afterChange()
#
#     def setBaZi(self):
#         bazi = "生辰八字：%s年 %s月 %s日 %s时"
#         bazi = bazi % (self.birthInfo.lunar_date.getYearInGanZhi(),
#                        self.birthInfo.lunar_date.getMonthInGanZhi(),
#                        self.birthInfo.lunar_date.getDayInGanZhi(),
#                        self.birthInfo.lunar_date.getTimeInGanZhi())
#         self.lb_bazi.setText(bazi)
#
#     def setYun(self, year, month):
#         da_yun_gan_zhi = self.birthInfo.getDaYunGanZhi(year, month)
#         self.lb_dayun.setText("大运：" + da_yun_gan_zhi['大运'])
#         self.lb_liunian.setText("流年：" + da_yun_gan_zhi['流年'])
#         self.lb_liuyue.setText("流月：" + da_yun_gan_zhi['流月'])
#
#     def clickCheck(self, year):
#         check = self.birthInfo.clickCheck(year)
#         if not check:
#             msg = QMessageBox.information(self, "错误", "请不要点击曲线以外的地方！", QMessageBox.Ok)
#             return msg
#         return None
#
#     def changeHour(self):
#         index = self.sender().currentIndex()
#         self.birthInfo.changeHour(index)
#         self.afterChange()
#
#     def changeSex(self):
#         sex = self.sender().currentText()
#         if sex == '女':
#             self.birthInfo.changeSex(0)
#         else:
#             self.birthInfo.changeSex(1)
#         self.afterChange()
#
#     def judge(self):
#         if self.birthInfo is None:
#             return
#         jinmu_scores, shuihuo_scores, dates = self.birthInfo.calculateLineScore()
#
#         spec_data = {"三合": self.birthInfo.san_he,
#                      "反拱": self.birthInfo.fan_gong,
#                      "对冲": self.birthInfo.dui_chong,
#                      "复吟": self.birthInfo.fu_yin}
#         self.line_area.drawLine(dates, jinmu_scores, shuihuo_scores, spec_data)
#
#
# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     ui = Birth()
#     ui.show()
#     sys.exit(app.exec_())
