from utils import DealData


class SearchElm:

    def __init__(self, zhiDict=None):
        if zhiDict:
            self.zhiDict = zhiDict.copy()
            self.values = zhiDict.values()
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
            elif self.type == "对冲":
                if yueZhi == self.combine["流年"]:
                    self.month.append(month)
            elif self.type == "复吟":
                if yueZhi == DealData.getZhi(self.combine["流年"]):
                    self.month.append(month)
        self.setDateStr()

    def setDateStr(self):
        for m in self.month:
            ds = str(self.year) + '-' + str(m)
            self.dateStr.append(ds)


def searchPattern(patList, zhiDict, searchType, year):
    targetPat = None
    for pat in patList:
        if zhiDict['流年'] in pat:
            targetPat = pat.copy()
            break
    if targetPat is None:
        return None
    searchElm = SearchElm(zhiDict)
    searchElm.setPattern(targetPat)
    targetPat.remove(zhiDict['流年'])
    if set(targetPat).issubset(set(searchElm.values)):
        searchElm.combine["流年"] = zhiDict["流年"]
        searchElm.year = year
        for key in zhiDict:
            if zhiDict[key] in targetPat:
                searchElm.combine[key] = zhiDict[key]
        searchElm.type = searchType
        return searchElm
    else:
        return None


#   查询复吟
def searchFuYin(liuNianGanZhi, ganZhiDict, year):
    elm = SearchElm()
    elm.year = year
    elm.type = "复吟"
    for key in ganZhiDict:
        if key != "流年" and ganZhiDict[key] == liuNianGanZhi:
            elm.combine[key] = ganZhiDict[key]
    if len(elm.combine) == 0:
        return None
    else:
        elm.combine["流年"] = liuNianGanZhi
        return elm
