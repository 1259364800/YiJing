from config import config
from datetime import datetime
import json
import math


def getGan(ganZhi):
    if len(ganZhi) == 0:
        return ""
    elif len(ganZhi) == 1:
        return ganZhi
    return ganZhi[0]


def getZhi(ganZhi):
    if len(ganZhi) == 0:
        return ""
    elif len(ganZhi) == 1:
        return ganZhi
    return ganZhi[1]


def makeProvinceInfo():
    config.PROVINCE_INFO = {}
    f = open('./config/province_data.json', encoding='utf-8')
    data = json.load(f)
    for province in data:
        provinceName = province['name']
        config.PROVINCE_INFO[provinceName] = {}
        for city in province['city']:
            cityName = city['name']
            config.PROVINCE_INFO[provinceName][cityName] = []
            for area in city['area']:
                config.PROVINCE_INFO[provinceName][cityName].append(area)


def makeTimeZoneData():
    f = open('./config/time_zone.json', encoding='utf-8')
    config.TIME_ZONE_DATA = json.load(f)


def getProvinceInfo():
    if config.PROVINCE_INFO is None:
        makeProvinceInfo()
    return config.PROVINCE_INFO


def getTimeZoneData():
    if config.TIME_ZONE_DATA is None:
        makeTimeZoneData()
    return config.TIME_ZONE_DATA


# 安全性检查
def zoneCheck(province, city):
    timeZoneData = getTimeZoneData()
    if province in timeZoneData:
        if city in timeZoneData[province]:
            return True
    return False


def getTimeOffsetByZone(province, city):
    if not zoneCheck(province, city):
        return
    timeZoneData = getTimeZoneData()
    timeZone = timeZoneData[province][city]
    offset = timeZone - config.STANDARD_TIME_ZONE
    return offset


def mergeDict(dictA, dictB):
    for key in dictB:
        if key not in dictA:
            dictA[key] = dictB[key]
    return dictA


def addDict(dictA, dictB):
    for key in dictB:
        if key not in dictA:
            dictA[key] = dictB[key]
        else:
            dictA[key] = dictA[key] + dictB[key]
    return dictA


def calculateElemScore(ganZhiDict, numAttribute):
    scores = {}
    if numAttribute == 4:
        scores = {'火': 0, '金': 0, '水': 0, '木': 0}
    elif numAttribute == 5:
        scores = {'火': 0, '土': 0, '金': 0, '水': 0, "木": 0}
    elemWeights = getWeightsByAttribute(numAttribute)
    elems = getElemsByAttribute(numAttribute)
    for key in elems:
        scores[key] = 0
    for key in ganZhiDict:
        if ganZhiDict[key] != "":
            if numAttribute == 4:
                val = config.FOUR_ELEM_SCORE[getZhi(ganZhiDict[key])]
            elif numAttribute == 5:
                val = config.FIVE_ELEM_SCORE[getZhi(ganZhiDict[key])]
            for elem in val:
                scores[elem] = float('%.2f' % (scores[elem] + val[elem] * elemWeights[key]))
    return scores


def getWeightsByAttribute(numAttribute):
    if numAttribute == 4:
        return config.FOUR_ELEM_WEIGHTS
    elif numAttribute == 5:
        return config.FIVE_ELEM_WEIGHTS


def getElemsByAttribute(numAttribute):
    ret = []
    if numAttribute == 4:
        elemScore = config.FOUR_ELEM_SCORE["子"]
    elif numAttribute == 5:
        elemScore = config.FIVE_ELEM_SCORE["子"]
    for key in elemScore:
        ret.append(key)
    return ret


def weightSum(elemWeights):
    val = 0
    for key in elemWeights:
        val += elemWeights[key]
    return val


def changeWeightsByAttribute(numAttribute, params):
    if numAttribute == 4:
        config.FOUR_ELEM_WEIGHTS = params
    elif numAttribute == 5:
        config.FIVE_ELEM_WEIGHTS = params


def formatDateTime(dates):
    ret = [datetime.strptime(d, '%Y-%m').date() for d in dates]
    return ret


def dealScores(scores, numAttribute):
    ret = {}
    if numAttribute == 4:
        ret = {"金木": [], "水火": [], "综合能量": []}
    elif numAttribute == 5:
        ret = {"金": [], "木": [], "水": [], "火": [], "土": []}
    for oneScore in scores:
        if numAttribute == 4:
            ret["金木"].append(oneScore["木"] - oneScore["金"])
            ret["水火"].append(oneScore["火"] - oneScore["水"])
        elif numAttribute == 5:
            for key in oneScore:
                ret[key].append(oneScore[key])
    if numAttribute == 4:
        ret["综合能量"] = squareSum(ret["金木"], ret["水火"])
    return ret


def squareSum(listA, listB):
    ret = []
    for i in range(len(listA)):
        tmp = math.sqrt(listA[i] ** 2 + listB[i] ** 2)
        ret.append(tmp)
    return ret


def dict2List(dictA):
    if dictA is None:
        return None
    ret = []
    for key in dictA:
        ret.append(dictA[key])
    return ret


def readSpecDataList():
    return config.SPEC_DATA_LIST


def readSpecTypeDataList(specType):
    return config.SPEC_DATA_LIST[specType]


if __name__ == "__main__":
    a = {'a': 1, 'b': 2}
    b = {'a': 2, 'b': 3}
    print(a | b)
