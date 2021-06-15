from lunar import Lunar, Solar

JIA_ZI = (
    "甲子", "乙丑", "丙寅", "丁卯", "戊辰", "己巳", "庚午", "辛未", "壬申", "癸酉", "甲戌", "乙亥", "丙子", "丁丑", "戊寅", "己卯", "庚辰", "辛巳", "壬午",
    "癸未", "甲申", "乙酉", "丙戌", "丁亥", "戊子", "己丑", "庚寅", "辛卯", "壬辰", "癸巳", "甲午", "乙未", "丙申", "丁酉", "戊戌", "己亥", "庚子", "辛丑",
    "壬寅", "癸卯", "甲辰", "乙巳", "丙午", "丁未", "戊申", "己酉", "庚戌", "辛亥", "壬子", "癸丑", "甲寅", "乙卯", "丙辰", "丁巳", "戊午", "己未", "庚申",
    "辛酉", "壬戌", "癸亥")

MONTH_DAYS_NORMAL = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
MONTH_DAYS_RUN = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]


def check(ganZhi):
    if ganZhi in JIA_ZI:
        return True
    return False


class BaZi2Birth:

    def __init__(self, year, monthGanZhi, dayGanZhi, hourGanZhi):
        self.year = year
        self.monthInfo = monthGanZhi
        self.dayInfo = dayGanZhi
        self.hourInfo = hourGanZhi

    def check(self):
        if not check(self.monthInfo):
            return "月份干支选择不合法！"
        if not check(self.dayInfo):
            return "日期干支选择不合法！"
        if not check(self.hourInfo):
            return "时辰干支选择不合法！"
        return None

    def isRunYear(self):
        if self.year % 100 != 0:
            if self.year % 4 != 0:
                return False
            else:
                return True
        else:
            if self.year % 400 != 0:
                return False
            else:
                return True

    def search(self):
        daysList = MONTH_DAYS_NORMAL
        month, day, hour = 0, 0, []
        monthList = []
        findDay = False
        if self.isRunYear():
            daysList = MONTH_DAYS_RUN
        for i in range(12):
            startSolar = Solar.fromYmdHms(self.year, i + 1, 1, 0, 0, 0)
            endSolar = Solar.fromYmdHms(self.year, i + 1, daysList[i], 23, 59, 59)
            startLunar = startSolar.getLunar()
            endLunar = endSolar.getLunar()
            startIndex = JIA_ZI.index(startLunar.getMonthInGanZhi())
            endIndex = JIA_ZI.index(endLunar.getMonthInGanZhi())
            for j in range(startIndex, endIndex + 1):
                if self.monthInfo == JIA_ZI[j]:
                    monthList.append(i + 1)
        if len(monthList) == 0:
            return -1, 0, 0
        for tmpMonth in monthList:
            for i in range(daysList[tmpMonth - 1]):
                tempSolar = Solar.fromYmdHms(self.year, tmpMonth, i + 1, 0, 0, 0)
                tempLunar = tempSolar.getLunar()
                if tempLunar.getDayInGanZhi() == self.dayInfo:
                    month = tmpMonth
                    day = i + 1
                    findDay = True
                    break
        if not findDay:
            return 0, -1, 0
        for i in range(24):
            tempSolar = Solar.fromYmdHms(self.year, month, day, i, 0, 0)
            tempLunar = tempSolar.getLunar()
            if tempLunar.getTimeInGanZhi() == self.hourInfo:
                hour.append(i)
        if len(hour) == 0:
            return 0, 0, -1
        return month, day, hour
