from utils import DealData


class SearchElm:

    def __init__(self, ganZhiDict=None):
        if ganZhiDict:
            self.ganZhiDict = ganZhiDict.copy()
            self.values = list(ganZhiDict.values())
            for i in range(len(self.values)):
                self.values[i] = DealData.getZhi(self.values[i])

        self.pat = ""
        self.type = ""
        self.year = 0
        self.month = []
        self.dateStr = []
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

    def markLiuYue(self, liuYue):
        for yue in liuYue:
            month = yue.getIndex() + 1
            yueZhi = DealData.getZhi(yue.getGanZhi())
            if self.type == "三合" or self.type == "反拱":
                mid = self.pat[1]
                if yueZhi == mid:
                    self.month.append(month)
            elif self.type == "对冲" or self.type == "复吟":
                if yueZhi == DealData.getZhi(self.combine["流年"]):
                    self.month.append(month)
        self.setDateStr()

    def setDateStr(self):
        for m in self.month:
            ds = str(self.year) + '-' + str(m)
            self.dateStr.append(ds)


def searchSpecType(searchType, *args):
    if searchType == "复吟":
        return searchFuYin(*args)
    else:
        return searchPattern(searchType, *args)


def searchPattern(searchType, ganZhiDict, year, patList):
    targetPat = None
    for pat in patList:
        if DealData.getZhi(ganZhiDict['流年']) in pat:
            targetPat = pat.copy()
            break
    if targetPat is None:
        return None
    searchElm = SearchElm(ganZhiDict)
    searchElm.setPattern(targetPat)
    targetPat.remove(DealData.getZhi(ganZhiDict['流年']))
    if set(targetPat).issubset(set(searchElm.values)):
        searchElm.combine["流年"] = DealData.getZhi(ganZhiDict["流年"])
        searchElm.year = year
        for key in ganZhiDict:
            if DealData.getZhi(ganZhiDict[key]) in targetPat:
                searchElm.combine[key] = DealData.getZhi(ganZhiDict[key])
        searchElm.type = searchType
        return searchElm
    else:
        return None


#   查询复吟
def searchFuYin(ganZhiDict, year, patList):
    elm = SearchElm()
    elm.year = year
    elm.type = "复吟"
    liuNianGanZhi = ganZhiDict["流年"]
    for key in ganZhiDict:
        if key != "流年" and ganZhiDict[key] == liuNianGanZhi:
            elm.combine[key] = ganZhiDict[key]
    if len(elm.combine) == 0:
        return None
    else:
        elm.combine["流年"] = liuNianGanZhi
        return elm
