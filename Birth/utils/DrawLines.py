import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backend_bases import MouseButton
from matplotlib.figure import Figure
from datetime import datetime
from utils import DealData


class DrawLines(FigureCanvasQTAgg):

    def __init__(self, width=10, height=10, dpi=100, callback=None):
        plt.rcParams['font.sans-serif'] = 'simHei'  # 用于正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示符号
        plt.style.use('ggplot')
        self.figs = Figure(figsize=(width, height), dpi=dpi)
        super(DrawLines, self).__init__(self.figs)
        self.axes = self.figs.add_subplot(111)
        self.axes.set_position([0.05, 0.1, 0.93, 0.88], which='both')
        self._xypress = []
        self.press_id = None
        self.moving = False
        self.callback = callback
        #   连接鼠标事件
        self.figs.canvas.mpl_connect('scroll_event', self.onScroll)
        self.figs.canvas.mpl_connect('button_press_event', self.onMousePress)
        self.figs.canvas.mpl_connect('button_release_event', self.onMouseRelease)
        self.figs.canvas.mpl_connect('motion_notify_event', self.onMouseMove)

    def drawOneLine(self, dates, vals, label):
        self.axes.plot(dates, vals, label=label)

    def drawLines(self, dates, scoreDict, specPoints, numAttribute):
        self.axes.cla()
        self.axes.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))
        for key in scoreDict:
            self.drawOneLine(dates, scoreDict[key], key)
        self.drawSpecialPoint(specPoints, numAttribute)
        self.axes.set_xlim(dates[0], dates[12])
        self.axes.legend(loc="upper left")
        self.figs.canvas.draw()
        self.figs.canvas.flush_events()

    def drawSpecialPoint(self, specPoints, numAttribute):
        for key in specPoints:
            points = []
            dates = []
            for year in specPoints[key]:
                elm = specPoints[key][year]
                for d in elm.dateStr:
                    dates.append(datetime.strptime(d, '%Y-%m'))
                    points.append(DealData.weightSum(DealData.getWeightsByAttribute(numAttribute))*10)

            if key == "三合":
                self.axes.scatter(x=dates, y=points, s=70, marker='o', label='三合')
            elif key == "反拱":
                self.axes.scatter(x=dates, y=points, s=70, marker='^', label='反拱')
            elif key == "对冲":
                self.axes.scatter(x=dates, y=points, s=100, marker='1', label='对冲')
            elif key == "复吟":
                self.axes.scatter(x=dates, y=points, s=100, marker='$=$', label='复吟')

    def onMousePress(self, event):
        self.press_id = event.button
        x, y = event.x, event.y
        self._xypress = []
        for i, a in enumerate(self.figs.canvas.figure.get_axes()):
            if (x is not None and y is not None and a.in_axes(event) and
                    a.get_navigate() and a.can_pan()):
                a.start_pan(x, y, event.button)
                self._xypress.append((a, i))

    def onMouseRelease(self, event):
        if not self.moving:
            if event.inaxes:
                time = event.inaxes.format_xdata(event.xdata)
                if self.callback:
                    self.callback(time)
        else:
            for a, ind in self._xypress:
                a.end_pan()

        self._xypress = []
        self.press_id = None
        self.moving = False

    def onMouseMove(self, event):
        if self.press_id == MouseButton.LEFT:
            self.moving = True
            for a, ind in self._xypress:
                a.drag_pan(self.press_id, event.key, event.x, event.y)
        self.figs.canvas.draw_idle()

    def onScroll(self, event):
        axtemp = event.inaxes
        if axtemp is None:
            return
        x_min, x_max = axtemp.get_xlim()
        x_range = (x_max - x_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + x_range, x_max - x_range))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - x_range, x_max + x_range))
        self.figs.canvas.draw_idle()  # 绘图动作实时反映在图像上
