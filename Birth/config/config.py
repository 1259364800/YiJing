FOUR_ELEM_WEIGHTS = {"年": 1, "月": 4, "日": 1, "时": 2, "大运": 2, "流年": 2, "流月": 1}
FIVE_ELEM_WEIGHTS = {"年": 1, "月": 4, "日": 1, "时": 2, "大运": 2, "流年": 2, "流月": 0.5}

FOUR_ELEM_SCORE = {
    "子": {"金": 0, "木": 2.68, "水": 10, "火": 0},
    "丑": {"金": 0, "木": 7.32, "水": 7.32, "火": 0},
    "寅": {"金": 0, "木": 10, "水": 2.68, "火": 0},
    "卯": {"金": 0, "木": 10, "水": 0, "火": 2.68},
    "辰": {"金": 0, "木": 7.32, "水": 0, "火": 7.32},
    "巳": {"金": 0, "木": 2.68, "水": 0, "火": 10},
    "午": {"金": 2.68, "木": 0, "水": 0, "火": 10},
    "未": {"金": 7.32, "木": 0, "水": 0, "火": 7.32},
    "申": {"金": 10, "木": 0, "水": 0, "火": 2.68},
    "酉": {"金": 10, "木": 0, "水": 2.68, "火": 0},
    "戌": {"金": 7.32, "木": 0, "水": 7.32, "火": 0},
    "亥": {"金": 2.68, "木": 0, "水": 10, "火": 0}
}
FIVE_ELEM_SCORE = {
    "子": {"金": 3.72, "木": 6.28, "水": 9.77, "火": 0.23, "土": 0.23},
    "丑": {"金": 1.5, "木": 8.5, "水": 8.5, "火": 1.5, "土": 1.5},
    "寅": {"金": 0.23, "木": 9.77, "水": 6.28, "火": 3.72, "土": 3.72},
    "卯": {"金": 0.23, "木": 9.77, "水": 3.72, "火": 6.28, "土": 6.28},
    "辰": {"金": 1.5, "木": 8.5, "水": 1.5, "火": 8.5, "土": 8.5},
    "巳": {"金": 3.72, "木": 6.28, "水": 0.23, "火": 9.77, "土": 9.77},
    "午": {"金": 6.28, "木": 3.72, "水": 0.23, "火": 9.77, "土": 9.77},
    "未": {"金": 8.5, "木": 1.5, "水": 1.5, "火": 8.5, "土": 8.5},
    "申": {"金": 9.77, "木": 0.23, "水": 3.72, "火": 6.28, "土": 6.28},
    "酉": {"金": 9.77, "木": 0.23, "水": 6.28, "火": 3.72, "土": 3.72},
    "戌": {"金": 8.5, "木": 1.5, "水": 8.5, "火": 1.5, "土": 1.5},
    "亥": {"金": 6.28, "木": 3.72, "水": 9.77, "火": 0.23, "土": 0.23}
}

SPEC_DATA_LIST = {
    "三合": [['申', '子', '辰'], ['寅', '午', '戌'], ['亥', '卯', '未'], ['巳', '酉', '丑']],
    "对冲": [['子', '午'], ['丑', '未'], ['寅', '申'], ['卯', '酉'], ['辰', '戌'], ['巳', '亥']],
    "反拱": [['寅', '子', '戌'], ['申', '午', '辰'], ['巳', '卯', '丑'], ['亥', '酉', '未']],
    "复吟": None
}

PROVINCE_INFO = None
TIME_ZONE_DATA = None
STANDARD_TIME_ZONE = 8.0
