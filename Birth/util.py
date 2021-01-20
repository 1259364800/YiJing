import json
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
import numpy as np
import math
from datetime import datetime, timedelta
from lunar import Solar, Lunar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backend_bases import MouseButton

from matplotlib.figure import Figure

province_dict = {}
energy_dict = {}

standard_time_zone = 8.0
score_weights = {"年": 1, "月": 4, "日": 1, "时": 2, "大运": 2, "流年": 2, "流月": 1}
#   三合
SAN_HE = [['申', '子', '辰'], ['寅', '午', '戌'], ['亥', '卯', '未'], ['巳', '酉', '丑']]
#   反拱
FAN_GONG = [['寅', '子', '戌'], ['申', '午', '辰'], ['巳', '卯', '丑'], ['亥', '酉', '未']]
#   对冲
DUI_CHONG = [['子', '午'], ['丑', '未'], ['寅', '申'], ['卯', '酉'], ['辰', '戌'], ['巳', '亥']]

#   读取省市列表
f = open('./config/province_data.json', encoding='utf-8')
data = json.load(f)
for province in data:
    pro_name = province['name']
    province_dict[pro_name] = {}
    for city in province['city']:
        city_name = city['name']
        province_dict[pro_name][city_name] = []
        for area in city['area']:
            province_dict[pro_name][city_name].append(area)

#   读取金木、水火能量表
f = open('./config/energy_data.json', encoding='utf-8')
energy_dict = json.load(f)

#   读取省市时区
f = open('./config/time_zone.json', encoding='utf-8')
time_zone_data = json.load(f)


def getGan(gan_zhi):
    if len(gan_zhi) == 0:
        return ""
    return gan_zhi[0]


def getZhi(gan_zhi):
    if len(gan_zhi) == 0:
        return ""
    return gan_zhi[1]


def mergeDict(dict_a, dict_b):
    for key in dict_b:
        if key not in dict_a:
            dict_a[key] = dict_b[key]
    return dict_a


def calculateElmScore(gan_zhi_dict):
    scores = {'金': 0, '木': 0, '水': 0, '火': 0}
    for key in gan_zhi_dict:
        if gan_zhi_dict[key] == "":
            val = {'金': 0, '木': 0, '水': 0, '火': 0}
        else:
            val = energy_dict[getZhi(gan_zhi_dict[key])]
        for elm in val:
            scores[elm] = float('%.2f' % (scores[elm] + val[elm] * score_weights[key]))
    return scores


def weightSum():
    s = 0
    for key in score_weights:
        s += score_weights[key]
    return s * 10


class SearchElm:

    def __init__(self, zhi_dict=None):
        if zhi_dict:
            self.zhi_dict = zhi_dict.copy()
            self.values = zhi_dict.values()
        self.pat = ""
        self.type = ""
        self.year = 0
        self.month = []
        self.date_str = []
        self.combine = {}

    def __str__(self):
        s = "查找类型为%s，匹配的组是%s，是%d年，" % (self.type, self.pat, self.year)
        for key in self.combine:
            s = s + "其中" + key + "为" + self.combine[key] + "，"
        return s

    def setPattern(self, pat):
        self.pat = ""
        for ch in pat:
            self.pat += ch

    def markLiuYue(self, liu_yue):
        for yue in liu_yue:
            month = yue.getIndex() + 1
            yue_zhi = getZhi(yue.getGanZhi())
            if self.type == "三合" or self.type == "反拱":
                mid = self.pat[1]
                if yue_zhi == mid:
                    self.month.append(month)
            elif self.type == "对冲":
                if yue_zhi == self.combine["流年"]:
                    self.month.append(month)
            elif self.type == "复吟":
                if yue_zhi == getZhi(self.combine["流年"]):
                    self.month.append(month)
        self.setDateStr()

    def setDateStr(self):
        for m in self.month:
            ds = str(self.year) + '-' + str(m)
            self.date_str.append(ds)


#   搜索匹配模板
def searchPattern(pat_lst, zhi_dict, search_type, year):
    target_pat = None
    for pat in pat_lst:
        if zhi_dict['流年'] in pat:
            target_pat = pat.copy()
            break
    if target_pat is None:
        return None
    search_elm = SearchElm(zhi_dict)
    search_elm.setPattern(target_pat)
    target_pat.remove(zhi_dict['流年'])
    if set(target_pat).issubset(set(search_elm.values)):
        search_elm.combine["流年"] = zhi_dict["流年"]
        search_elm.year = year
        for key in zhi_dict:
            if zhi_dict[key] in target_pat:
                search_elm.combine[key] = zhi_dict[key]
        search_elm.type = search_type
        return search_elm
    else:
        return None


#   查询复吟
def searchFuYin(liu_nian_gan_zhi, gan_zhi_dict, year):
    elm = SearchElm()
    elm.year = year
    elm.type = "复吟"
    for key in gan_zhi_dict:
        if key != "流年" and gan_zhi_dict[key] == liu_nian_gan_zhi:
            elm.combine[key] = gan_zhi_dict[key]
    if len(elm.combine) == 0:
        return None
    else:
        elm.combine["流年"] = liu_nian_gan_zhi
        return elm


class RadarFigure(FigureCanvasQTAgg):

    def __init__(self, width=10, height=10, dpi=100):
        plt.rcParams['font.sans-serif'] = 'simHei'  # 用于正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示符号
        plt.style.use('ggplot')
        self.figs = Figure(figsize=(width, height), dpi=dpi)
        super(RadarFigure, self).__init__(self.figs)
        self.axes = self.figs.add_subplot(111, polar=True)
        # self.axes.set_position([0.31, 0.11, 0.5, 0.7], which='both')
        self.di_zhi_lst = ["卯", "辰", "巳", "午", "未", "申", "酉", "戌", "亥", "子", "丑", "寅"]
        self.initRadar()

    def initRadar(self):
        self.radar_angles = np.linspace(0, 2 * np.pi, 4, endpoint=False)
        self.radar_angles = np.concatenate((self.radar_angles, [self.radar_angles[0]]))
        self.axes.set_thetagrids(self.radar_angles * 180 / np.pi, ['木', '火', '金', '水'])
        w_s = weightSum()
        qua_w_s = w_s / 4
        self.axes.set_yticks([0, qua_w_s, qua_w_s * 2, qua_w_s * 3, w_s])
        self.axes.tick_params('y', labelleft=False)
        self.axes.set_ylim(0, w_s)
        self.axes.grid(True)

    def initPie(self):
        self.pie_angles = np.linspace(0, 2 * np.pi, 12, endpoint=False)
        self.pie_angles = np.concatenate((self.pie_angles, [self.pie_angles[0]]))
        self.zhi_angles = np.linspace(1, 25, 12, endpoint=False)
        blank = []

        for i in range(12):
            blank.append("")
        self.axes.set_thetagrids(self.pie_angles * 180 / np.pi, blank)
        self.axes.tick_params('y', labelleft=False)
        lim = math.sqrt(max(score_weights.values()))
        self.axes.set_ylim(0, lim)
        for i in range(len(self.zhi_angles)):
            if 3 <= i <= 8:
                self.axes.text(x=self.zhi_angles[i] * np.pi / 12, y=1.2 * lim, s=self.di_zhi_lst[i])
            else:
                self.axes.text(x=self.zhi_angles[i] * np.pi / 12, y=1.1 * lim, s=self.di_zhi_lst[i])

        qua_w_s = lim / 4
        self.axes.set_yticks([0, qua_w_s, qua_w_s * 2, qua_w_s * 3, lim])
        self.axes.grid(True)

    def drawPie(self, gan_zhi_dict, date_str):
        self.axes.cla()
        self.initPie()
        for key in gan_zhi_dict:
            radius = math.sqrt(score_weights[key])
            index = self.di_zhi_lst.index(getZhi(gan_zhi_dict[key]))
            angle = self.pie_angles[index]
            self.axes.bar(angle, radius, width=np.pi / 6, align='edge', label=key, alpha=0.25)
            # self.axes.fill(self.radar_angles, lst, 'y', alpha=0.25)
        # self.axes.legend(bbox_to_anchor=(1.3, 1.15), loc="upper left", borderaxespad=0, font)
        lim = math.sqrt(max(score_weights.values()))
        if len(gan_zhi_dict) == 7:
            self.axes.text(x=np.pi * 3 / 8, y=1.3 * lim, s=date_str)
        self.axes.legend(loc=(-0.38, 0.4))
        self.figs.canvas.draw()
        self.figs.canvas.flush_events()

    def drawRadar(self, da_yun_lst, birth_lst, date_str):
        self.axes.cla()
        self.initRadar()
        self.drawStep(birth_lst, "终生四柱")

        if da_yun_lst:
            self.drawStep(da_yun_lst, "大运")
            self.axes.text(x=5 / 6 * np.pi, y=250, s=date_str)

        self.axes.legend(bbox_to_anchor=(1.3, 1.15), loc=1, borderaxespad=0)
        self.figs.canvas.draw()
        self.figs.canvas.flush_events()

    def drawStep(self, lst, lb):
        lst = np.concatenate((lst, [lst[0]]))
        self.axes.plot(self.radar_angles, lst, 'o-', linewidth=1, clip_on=False, label=lb)
        self.axes.fill(self.radar_angles, lst, 'y', alpha=0.25)
        for a, b in zip(self.radar_angles, lst):
            self.axes.text(a, b, b, ha='center', va='bottom', fontsize=8)


def ping_fang_he(a_scores, b_scores):
    pfh = []
    for i in range(len(a_scores)):
        s = math.sqrt(a_scores[i] ** 2 + b_scores[i] ** 2)
        pfh.append(s)
    return pfh


class LineFigure(FigureCanvasQTAgg):

    def __init__(self, width=10, height=10, dpi=100, callback=None):
        plt.rcParams['font.sans-serif'] = 'simHei'  # 用于正常显示中文
        plt.rcParams['axes.unicode_minus'] = False  # 用于正常显示符号
        plt.style.use('ggplot')
        self.figs = Figure(figsize=(width, height), dpi=dpi)
        super(LineFigure, self).__init__(self.figs)
        self.axes = self.figs.add_subplot(111)
        self.axes.set_position([0.05, 0.1, 0.93, 0.88], which='both')
        self._xypress = []
        self.press_id = None
        self.moving = False
        self.callback = callback
        self.figs.canvas.mpl_connect('scroll_event', self.onScroll)
        self.figs.canvas.mpl_connect('button_press_event', self.onMousePress)
        self.figs.canvas.mpl_connect('button_release_event', self.onMouseRelease)
        self.figs.canvas.mpl_connect('motion_notify_event', self.onMouseMove)

    def drawLine(self, dates, jinmu_scores, shuihuo_scores, spec_data):
        dates = [datetime.strptime(d, '%Y-%m').date() for d in dates]
        self.axes.cla()
        self.axes.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))
        pfh = ping_fang_he(jinmu_scores, shuihuo_scores)
        self.axes.plot(dates, shuihuo_scores, label='水火')
        self.axes.plot(dates, jinmu_scores, label='金木')
        self.axes.plot(dates, pfh, label='综合能量')
        self.drawSpecialPoint(spec_data)
        self.axes.set_xlim(dates[0], dates[12])
        self.axes.legend(loc="upper left")
        self.figs.canvas.draw()
        self.figs.canvas.flush_events()

    def drawSpecialPoint(self, spec_data):
        for key in spec_data:
            points = []
            dates = []
            for year in spec_data[key]:
                elm = spec_data[key][year]
                for d in elm.date_str:
                    dates.append(datetime.strptime(d, '%Y-%m'))
                    points.append(weightSum())
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


class DateTime:

    def __init__(self, year, month, day, hour):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour

    def __add__(self, hour: int):
        tmpDatetime = datetime(self.year, self.month, self.day, self.hour)
        offset = timedelta(hours=hour)
        tmpDatetime = tmpDatetime + offset
        self.year = tmpDatetime.year
        self.month = tmpDatetime.month
        self.day = tmpDatetime.day
        self.hour = tmpDatetime.hour
        return self

    def changeYear(self, year):
        self.year = year

    def changeMonth(self, month):
        self.month = month

    def changeDay(self, day):
        self.day = day

    def changeHour(self, hour):
        self.hour = hour


class BirthInfo:

    def __init__(self, birth_time: DateTime, isSolar, province, city, sex):
        self.birth_time = birth_time  # 跟据时区修改的时间
        self.beijing_time = birth_time  # 填写时的北京时间
        self.isSolar = isSolar  # 是否是阳历
        self.province = province
        self.city = city
        self.sex = sex  # 女：0，男：1
        self.changeSolar(isSolar)
        self.daYun = self.lunar_date.getDaYun(self.sex).getDaYun()
        self.search()

    #   安全性检查
    def zoneCheck(self):
        if self.province in time_zone_data:
            if self.city in time_zone_data[self.province]:
                return True
        return False

    def clickCheck(self, year):
        start_year = self.daYun[0].getStartYear()
        end_year = self.daYun[-1].getEndYear()
        if year < start_year or year > end_year:
            return False
        return True

    def timeZoneCorrect(self):
        if not self.zoneCheck():
            return
        timeZone = time_zone_data[self.province][self.city]
        offset = timeZone - standard_time_zone
        self.birth_time = self.beijing_time + offset

    def changeDateTime(self):
        if self.isSolar:
            self.solar_date = Solar.fromYmdHms(self.birth_time.year, self.birth_time.month, self.birth_time.day,
                                               self.birth_time.hour, 0, 0)
            self.lunar_date = self.solar_date.getLunar()
        else:
            self.lunar_date = Lunar.fromYmdHms(self.birth_time.year, self.birth_time.month, self.birth_time.day,
                                               self.birth_time.hour, 0, 0)
            self.solar_date = self.lunar_date.getSolar()

    def changeHour(self, hour):
        self.birth_time.changeHour(hour)
        self.changeDateTime()

    def changeSolar(self, isSolar):
        self.isSolar = isSolar
        self.changeDateTime()

    def changeProvince(self, province):
        self.province = province

    def changeCity(self, city):
        self.city = city
        self.timeZoneCorrect()

    def changeSex(self, sex):
        self.sex = sex

    def getDaYun(self):
        self.daYun = self.lunar_date.getDaYun(self.sex).getDaYun()

    def getDateGanZhi(self):
        year_gan_zhi = self.lunar_date.getYearInGanZhi()
        month_gan_zhi = self.lunar_date.getMonthInGanZhi()
        day_gan_zhi = self.lunar_date.getDayInGanZhi()
        hour_gan_zhi = self.lunar_date.getTimeInGanZhi()
        return {"年": year_gan_zhi, "月": month_gan_zhi, "日": day_gan_zhi, "时": hour_gan_zhi}

    def search(self):
        self.san_he = {}
        self.fan_gong = {}
        self.dui_chong = {}
        self.fu_yin = {}
        birth_gan_zhi = self.getDateGanZhi()
        zhi_dict = {}
        gan_zhi_dict = {}
        for key in birth_gan_zhi:
            zhi_dict[key] = getZhi(birth_gan_zhi[key])
            gan_zhi_dict[key] = birth_gan_zhi[key]
        for yun in self.daYun:
            if yun.getIndex() == 0:
                yun_gan_zhi = ""
            else:
                yun_gan_zhi = yun.getGanZhi()
            liu_nian = yun.getLiuNian()
            yun_zhi = getZhi(yun_gan_zhi)
            zhi_dict["大运"] = yun_zhi
            gan_zhi_dict["大运"] = yun_gan_zhi
            for nian in liu_nian:
                year = nian.getYear()
                liu_nian_gan_zhi = nian.getGanZhi()
                liu_nian_zhi = getZhi(liu_nian_gan_zhi)
                zhi_dict["流年"] = liu_nian_zhi
                san_he = searchPattern(SAN_HE, zhi_dict, "三合", year)
                fan_gong = searchPattern(FAN_GONG, zhi_dict, "反拱", year)
                dui_chong = searchPattern(DUI_CHONG, zhi_dict, "对冲", year)
                fu_yin = searchFuYin(liu_nian_gan_zhi, gan_zhi_dict, year)

                liu_yue = nian.getLiuYue()

                if san_he:
                    san_he.markLiuYue(liu_yue)
                    self.san_he[year] = san_he
                if fan_gong:
                    fan_gong.markLiuYue(liu_yue)
                    self.fan_gong[year] = fan_gong
                if dui_chong:
                    dui_chong.markLiuYue(liu_yue)
                    self.dui_chong[year] = dui_chong
                if fu_yin:
                    fu_yin.markLiuYue(liu_yue)
                    self.fu_yin[year] = fu_yin

    def getDaYunGanZhi(self, year, month):
        for yun in self.daYun:
            if yun.getStartYear() <= year <= yun.getEndYear():
                target_yun = yun
                break
        yun_index = target_yun.getIndex()
        if yun_index == 0:
            da_yun_gan_zhi = ""
        else:
            da_yun_gan_zhi = "%s" % target_yun.getGanZhi()
        liu_nian = target_yun.getLiuNian()
        for nian in liu_nian:
            if nian.getYear() == year:
                target_nian = nian
                break
        nian_gan_zhi = "%s" % target_nian.getGanZhi()
        liu_yue = target_nian.getLiuYue()
        for yue in liu_yue:
            if yue.getIndex() == month - 1:
                target_yue = yue
                break
        yue_gan_zhi = "%s" % target_yue.getGanZhi()
        return {"大运": da_yun_gan_zhi, "流年": nian_gan_zhi, "流月": yue_gan_zhi}

    def calculateLineScore(self):
        #   先计算出生的得分，木火是正值，金水是负值
        #   出生的score只有1组,大运的score是9组,流年的score是90组,流月的score是90*12=1080组
        #   但事实上，其实每个流年的流月干支是一样的，理论上而言，score是12组
        birth_scores = calculateElmScore(self.getDateGanZhi())
        birth_gan_zhi = self.getDateGanZhi()
        birth_zhi = []
        for key in birth_gan_zhi:
            birth_zhi.append(getZhi(birth_gan_zhi[key]))
        dates = []
        fin_jinmu = []
        fin_shuihuo = []
        for yun in self.daYun:
            if yun.getIndex() == 0:
                yun_zhi = ""
            else:
                yun_zhi = getZhi(yun.getGanZhi())
            liu_nian = yun.getLiuNian()
            for nian in liu_nian:
                this_nian = nian.getYear()
                nian_zhi = getZhi(nian.getGanZhi())
                liu_yue = nian.getLiuYue()
                for yue in liu_yue:
                    scores = {'金': 0, '木': 0, '水': 0, '火': 0}
                    this_yue = yue.getIndex() + 1
                    yue_zhi = getZhi(yue.getGanZhi())
                    zhi_dict = {'大运': yun_zhi, '流年': nian_zhi, '流月': yue_zhi}
                    one_date = "%d-%d" % (this_nian, this_yue)
                    dates.append(one_date)
                    for key in zhi_dict:  # 计算大运、流年、流月分数
                        if zhi_dict[key] != '':
                            val = energy_dict[zhi_dict[key]]
                            for elm in val:
                                scores[elm] = float('%.2f' % (scores[elm] + val[elm] * score_weights[key]))

                    for key in scores:
                        scores[key] += birth_scores[key]
                    jinmu_score = scores['木'] - scores['金']
                    shuihuo_score = scores['火'] - scores['水']
                    fin_jinmu.append(jinmu_score)
                    fin_shuihuo.append(shuihuo_score)
        return fin_jinmu, fin_shuihuo, dates


if __name__ == "__main__":
    s = Solar.fromYmdHms(2000, 1, 1, 0, 30, 0)
    l = s.getLunar()
    dayun = l.getDaYun(1).getDaYun()
    for yun in dayun:
        print("从%d岁开始，干支为%s" % (yun.getStartAge(), yun.getGanZhi()))
