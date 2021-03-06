from datetime import datetime, timedelta
from lunar import Solar, Lunar
from utils import DealData, Search
from config import config


class TimeInfo:

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

    def setYear(self, year):
        self.year = year

    def setMonth(self, month):
        self.month = month

    def setDay(self, day):
        self.day = day

    def setHour(self, hour):
        self.hour = hour


class NormalBirth:

    def __init__(self, birthTime: TimeInfo, isSolar, province, city, sex, useZoneTime=False):
        self.zoneTime = birthTime  # 跟据时区修改的时间
        self.beiJingTime = birthTime  # 填写时的标准北京时间
        self.isSolar = isSolar  # 是否是阳历
        self.province = province
        self.city = city
        self.sex = sex  # 女：0，男：1
        self.wrong = False
        self.useZoneTime = useZoneTime
        self.useTime()
        self.specData = {}
        self.changeSolar(isSolar)

    def makeSpecDataDict(self):
        specDataList = DealData.readSpecDataList()
        self.specData = {}
        for key in specDataList:
            self.specData[key] = {}

    def useTime(self):
        self.usingTime = self.zoneTime if self.useZoneTime else self.beiJingTime
        self.changeDateTime()

    def setUseZoneTime(self, use):
        self.useZoneTime = use
        self.useTime()

    def clickCheck(self, year):
        start_year = self.daYun[0].getStartYear()
        end_year = self.daYun[-1].getEndYear()
        if year < start_year or year > end_year:
            return False
        return True

    def setZoneTime(self):
        self.zoneTime = self.beiJingTime + DealData.getTimeOffsetByZone(self.province, self.city)

    def changeDateTime(self):
        if self.isSolar:
            try:
                self.solarDate = Solar.fromYmdHms(self.usingTime.year, self.usingTime.month, self.usingTime.day,
                                                  self.usingTime.hour, 0, 0)
            except Exception:
                self.wrong = True
                return True
            else:
                self.lunarDate = self.solarDate.getLunar()
                self.wrong = False
        else:
            try:
                self.lunarDate = Lunar.fromYmdHms(self.usingTime.year, self.usingTime.month, self.usingTime.day,
                                                  self.usingTime.hour, 0, 0)
            except Exception:
                self.wrong = True
                return True
            else:
                self.solarDate = self.lunarDate.getSolar()
                self.wrong = False
        self.getDaYun()
        self.search()

    def changeYear(self, year):
        self.beiJingTime.setYear(year)
        return self.changeDateTime()

    def changeMonth(self, month):
        self.beiJingTime.setMonth(month)
        return self.changeDateTime()

    def changeDay(self, day):
        self.beiJingTime.setDay(day)
        return self.changeDateTime()

    def changeHour(self, hour):
        self.beiJingTime.setHour(hour)
        return self.changeDateTime()

    def changeSolar(self, isSolar):
        self.isSolar = isSolar
        return self.changeDateTime()

    def changeProvince(self, province):
        self.province = province

    def changeCity(self, city):
        self.city = city
        self.setZoneTime()

    def changeSex(self, sex):
        self.sex = sex
        self.changeDateTime()

    def getDaYun(self):
        self.daYun = self.lunarDate.getDaYun(self.sex).getDaYun()

    def getBirthGanZhi(self):
        yearGanZhi = self.lunarDate.getYearInGanZhi()
        monthGanZhi = self.lunarDate.getMonthInGanZhi()
        dayGanZhi = self.lunarDate.getDayInGanZhi()
        hourGanZhi = self.lunarDate.getTimeInGanZhi()
        return {"年": yearGanZhi, "月": monthGanZhi, "日": dayGanZhi, "时": hourGanZhi}

    def search(self):
        self.makeSpecDataDict()
        birthGanZhi = self.getBirthGanZhi()
        ganZhiDict = {}
        for key in birthGanZhi:
            ganZhiDict[key] = birthGanZhi[key]

        index = 0
        for yun in self.daYun:
            liuNian = yun.getLiuNian()
            for nian in liuNian:
                year = nian.getYear()
                daYunGanZhi = self.getDaYunGanZhi(year, None, index)
                for key in daYunGanZhi:
                    # zhiDict[key] = DealData.getZhi(daYunGanZhi[key])
                    ganZhiDict[key] = daYunGanZhi[key]
                for specType in self.specData:
                    searchRes = Search.searchSpecType(specType, ganZhiDict, year,
                                                      DealData.readSpecTypeDataList(specType))
                    if searchRes is not None:
                        liuYue = nian.getLiuYue()
                        searchRes.markLiuYue(liuYue)
                        self.specData[specType][year] = searchRes
            index += 1
        self.checkFanGong()

    def checkFanGong(self):
        #   反拱必须独立出现
        fanGongYears = list(self.specData["反拱"].keys())
        for year in fanGongYears:
            mid = self.specData["反拱"][year].pat[1]
            for specType in self.specData:
                if specType != "反拱":
                    specYears = list(self.specData[specType].keys())
                    if year in specYears:
                        pat = self.specData[specType][year].pat
                        if mid in pat:
                            self.specData["反拱"].pop(year)
                            break

    def getDaYunGanZhi(self, year, month=None, daYunIndex=None):
        if daYunIndex is None:
            for yun in self.daYun:
                if yun.getStartYear() <= year <= yun.getEndYear():
                    targetYun = yun
                    break
            yunIndex = targetYun.getIndex()
        else:
            yunIndex = daYunIndex
            targetYun = self.daYun[yunIndex]
        if yunIndex == 0:
            daYunGanZhi = ""
        else:
            daYunGanZhi = "%s" % targetYun.getGanZhi()
        liuNian = targetYun.getLiuNian()
        targetNian = liuNian[year - targetYun.getStartYear()]
        nianGanZhi = "%s" % targetNian.getGanZhi()
        if month:
            liuYue = targetNian.getLiuYue()
            targetYue = liuYue[month - 1]
            yueGanZhi = "%s" % targetYue.getGanZhi()
            return {"大运": daYunGanZhi, "流年": nianGanZhi, "流月": yueGanZhi}
        else:
            return {"大运": daYunGanZhi, "流年": nianGanZhi}

    def calculateLineScore(self, numAttribute):
        scores = []
        birthGanZhi = self.getBirthGanZhi()
        birthScore = DealData.calculateElemScore(birthGanZhi, numAttribute)
        dates = []
        index = 0
        for yun in self.daYun:
            liuNian = yun.getLiuNian()
            for nian in liuNian:
                year = nian.getYear()
                liuYue = nian.getLiuYue()
                for yue in liuYue:
                    month = yue.getIndex() + 1
                    daYunGanZhi = self.getDaYunGanZhi(year, month, index)
                    daYunScore = DealData.calculateElemScore(daYunGanZhi, numAttribute)
                    date = "%d-%d" % (year, month)
                    dates.append(date)
                    scores.append(DealData.addDict(daYunScore, birthScore))
            index += 1
        scoreDict = DealData.dealScores(scores, numAttribute)
        return scoreDict, dates


if __name__ == "__main__":
    a = {"a": 1, "b": 2, "c": 3}
    # a.pop("c")
    # print(a)

