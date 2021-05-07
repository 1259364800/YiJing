import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
import math

from utils import DealData


class DrawPie(FigureCanvasQTAgg):

    def __init__(self, width=10, height=10, dpi=100):
        plt.rcParams['font.sans-serif'] = 'simHei'  # 用于正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示符号
        plt.style.use('ggplot')
        self.figs = Figure(figsize=(width, height), dpi=dpi)
        super(DrawPie, self).__init__(self.figs)
        self.axes = self.figs.add_subplot(111, polar=True)
        # self.axes.set_position([0.31, 0.11, 0.5, 0.7], which='both')
        self.zhiList = ["卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑", "寅"]
        self.initPie(4)  # 默认初始化为4

    def initPie(self, numAttribute):
        self.pieAngles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
        self.pieAngles = np.concatenate((self.pieAngles, [self.pieAngles[0]]))
        self.zhiAngles = np.linspace(1, 25, 12, endpoint=False)

        blank = []
        for i in range(12):
            blank.append("")

        self.axes.set_thetagrids(self.pieAngles * 180 / np.pi, blank)
        self.axes.tick_params('y', labelleft=False)
        lim = math.sqrt(max(DealData.getWeightsByAttribute(numAttribute).values()))
        self.axes.set_ylim(0, lim)
        for i in range(len(self.zhiAngles)):
            if 3 <= i <= 8:
                self.axes.text(x=self.zhiAngles[i] * np.pi / 12, y=1.2 * lim, s=self.zhiList[i])
            else:
                self.axes.text(x=self.zhiAngles[i] * np.pi / 12, y=1.1 * lim, s=self.zhiList[i])

        avg = lim / numAttribute
        ticks = [i * avg for i in range(numAttribute + 1)]
        self.axes.set_yticks(ticks)
        self.axes.grid(True)

    def drawPie(self, ganZhiDict, dateStr, numAttribute):
        self.axes.cla()
        self.initPie(numAttribute)
        for key in ganZhiDict:
            radius = math.sqrt(DealData.getWeightsByAttribute(numAttribute)[key])
            zhi = DealData.getZhi(ganZhiDict[key])
            if zhi == '':
                radius = 0
                index = 0
            else:
                index = self.zhiList.index(DealData.getZhi(ganZhiDict[key]))
            angle = self.pieAngles[index]
            self.axes.bar(angle, radius, width=np.pi / 6, align='edge', label=key, alpha=0.25)
            # self.axes.fill(self.radar_angles, lst, 'y', alpha=0.25)
        # self.axes.legend(bbox_to_anchor=(1.3, 1.15), loc="upper left", borderaxespad=0, font)
        lim = math.sqrt(max(DealData.getWeightsByAttribute(numAttribute).values()))

        if len(ganZhiDict) == 7:
            self.axes.text(x=np.pi * 3 / 8, y=1.3 * lim, s=dateStr)

        self.axes.legend(bbox_to_anchor=(1.5, 1.05), loc=1, borderaxespad=0)
        self.figs.canvas.draw()
        self.figs.canvas.flush_events()
