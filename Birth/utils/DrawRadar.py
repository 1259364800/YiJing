import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np

from utils import DealData


class DrawRadar(FigureCanvasQTAgg):

    def __init__(self, width=10, height=10, dpi=100):
        plt.rcParams['font.sans-serif'] = 'simHei'  # 用于正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示符号
        plt.style.use('ggplot')
        self.figs = Figure(figsize=(width, height), dpi=dpi)
        super(DrawRadar, self).__init__(self.figs)
        self.axes = self.figs.add_subplot(111, polar=True)
        # self.axes.set_position([0.31, 0.11, 0.5, 0.7], which='both')
        self.initRadar(4)  # 默认生成4属性

    def initRadar(self, numAttribute):
        weightSum = DealData.weightSum(DealData.getWeightsByAttribute(numAttribute))
        avgWeight = weightSum / numAttribute
        self.radarAngles = np.linspace(0, 2 * np.pi, numAttribute, endpoint=False)
        self.axes.set_theta_zero_location('N')
        if numAttribute == 4:
            self.radarAngles = np.concatenate((self.radarAngles, [self.radarAngles[0]]))
            self.axes.set_thetagrids(self.radarAngles * 180 / np.pi, ['金', '木', '水', '火'])
        elif numAttribute == 5:
            self.radarAngles = np.concatenate((self.radarAngles, [self.radarAngles[0]]))
            self.axes.set_thetagrids(self.radarAngles * 180 / np.pi, ['金', '木', '水', '火', '土'])
        ticks = [i*avgWeight*10 for i in range(numAttribute+1)]
        self.axes.set_yticks(ticks)
        self.axes.tick_params('y', labelleft=False)
        self.axes.set_ylim(0, weightSum * 10)
        self.axes.grid(True)

    def drawRadar(self, numAttribute, daYunList, birthList, dateStr):
        self.axes.cla()
        self.initRadar(numAttribute)
        self.drawOneType(birthList, "终生四柱")
        if daYunList:
            self.drawOneType(daYunList, "大运")
            self.axes.text(x=5 / 6 * np.pi, y=250, s=dateStr)

        self.axes.legend(bbox_to_anchor=(1.4, 1.05), loc=1, borderaxespad=0)
        self.figs.canvas.draw()
        self.figs.canvas.flush_events()

    def drawOneType(self, attrList, label):
        attrList = np.concatenate((attrList, [attrList[0]]))
        self.axes.plot(self.radarAngles, attrList, 'o-', linewidth=1, clip_on=False, label=label)
        self.axes.fill(self.radarAngles, attrList, 'y', alpha=0.25)
        for a, b in zip(self.radarAngles, attrList):
            self.axes.annotate(str(b), xy=(a, b), xytext=(a, b+15))

