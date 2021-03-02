"""
----------2021.1.14需求----------
  1.标注三合、反拱、对冲月份，其中三合、反拱标注中间的月份，即子午卯酉，申子辰就标注子，对冲标注流年所在地支（结束）
  2.查询复吟，复吟即流年干支和大运干支相同，其中流月标注也是标注流年所在地支（结束）
----------2021.1.30需求----------
一、原局的八字修正：
1、年柱不变，其能量图见表一
2、月柱要修改：按照原局的月柱向前推两个月，然后根据表一去取值。如某福主的是正月出生，当年的月柱为戊寅，则调整后的月柱为丙子；注意：调整后改变原局的八字，今后冲、合、拱、同的判断都根据新调整的八字来判断。
因为八字改变了，月支的能量图仍然用表一。
3、日柱的调整规则：传统的日柱以“子时”为分界线，棱婴调整后的规则以太阳升起为分界线，即日出后为当天，日出前为前一天的日柱（即向前推一个）。根据太阳升起由寒变热（阴转阳）定义日出进“子”，日落进“酉”。因一年四季的太阳升起的时间是变化的，先根据福主的原始出生月份，进入一年四季的查询表中进行查询，如果是日出后（到次日日出前）即为当日原局的日柱，否则为前一天的日柱。具体一年四季日出时间见表二：

	春	夏	秋	冬
日出进子（时间）	6:00-7:59	5:00-7:20	6:00-7:59	7:00-8:40
日落进酉（时间）	18:00-21:59	19:00-22:20	18:00-21:59	17:00-21:40

4、时柱的调整规则：根据太阳升起由寒变热（阴转阳），定义日出进“子”，日落进“酉”。因此其12地支不是均匀分布的，也会根据一年四季的变化而变化。具体实现时，先根据福主的原始出生月份，进入一年四季的查询表中，依据出生的北京时间找出其地支的时辰，再推其天干，就得出福主的时柱。具体依据时间查地支的表见如下表三：
表二：时支、日支能量修正表
春、秋季节：
地支	子	丑	寅	卯	辰	巳	午	未	申	酉	戌	亥
时间	6-7:59	8-9:59	10-11:59	12-12:59	13-13:59	14-14:59	15-15:59	16-16:59	17-17:59	18-21:59	22-1：59	2-5:59
分界	初升									日落


夏季：
地支	子	丑	寅	卯	辰	巳	午	未	申	酉	戌	亥
时间	5-7:20	7:20-9:40	9:40-11:59	12-12:59	13-13:59	14-14:59	15-16:20	16:20-17:40	17:40-18:59	19-22:20	22:20-1：40	1:40-4:59
分界	初升									日落

冬季：
地支	子	丑	寅	卯	辰	巳	午	未	申	酉	戌	亥
时间	7-8:40	8:40-10:20	10:20-11:59	12-12:59	13-13:59	14-14:59	15-15:40	15:40-16:20	16:20-16:59	17-21:40	21:40-2：20	2:20-6:59
分界	初升									日落

如某福主出生于正月初六辰时（上午8:30），其原局为戊寅月、壬辰日、甲辰时；则调整后为：丙子月（前移了两个月）、壬辰日（查表春季上午6:00以后，为当日）、辛丑（查表上午8:30为丑时，与正规时辰提前了三个，对于的天干也提前即为辛）。


二、大运的调整改变：
1、 按照前述已改变的出生月份，本月为第一大运，后续大运一律倒排，没有传统规定中的顺排。
2、每段大运的管辖时间不再是固定的10年，同时运用两种时间长度，即大运天干管10年，大运地支管12年。此时每个流年所对应的大运不再按照六十花甲的组合来表达，而是分开表达，每个大运的天干与地支会出现人生后半段大运中，大运天干和地支的交错，因为管辖长度不一样，这是可取的，不算错误。也有可能出现阳干阴支或阴干阳支的情况如天干为甲、地支为丑等情况。
3、大运的推算方法：出生时即当月起运，为第一小运。推算方式为天干、地支分别推算。先根据出生日期倒数到月令交接的天数，天数除3取整为第一个天干的起运年龄时间点，天数除2.5取整为地支的起运年龄时间点。
例如福主1965年2月17日早晨8:30出生（当年2月4号进寅，为戊寅月），则原局八字：乙巳、戊寅、丁未、甲辰，棱婴算法调整后的八字：乙巳年、丙子月、丁未日、辛丑时
第一个小运为丙子，天干为丙、地支为子。
天干4岁（1969）起第一大运“乙”（17-4=13,13/3=4年另4个月）、14（1979）岁为“甲”、24岁（1989）为“癸”、34岁（1999）为“壬”、44岁（2009）为“辛”、54岁（2019）为“庚”、64岁为“己”、74岁为“戊”、84岁为“丁”、94岁为“丙”；
地支5岁（1970）起第一大运“亥”（17-4=13,13/2.5=5年另？个月）、17岁（1982）起第二地支大运“戌”、29岁（1995）起第三地支大运“酉”、41岁（2007）起第四地支大运“申”、53岁（2019）起第五地支大运“未”、65岁（2031）起第六地支大运“午”、77岁（2043）起第七地支大运“巳”、89岁（2055）起第八地支大运“辰”。
因此调整后流年大运的表示方法与原局的不同了。如以上福主：2020年庚子（流年）、大运：天干为“庚”、地支大运为“未”
4、总结：全部调整就是两方面，即原局的调整和大运的调整，此外与传统方案都一样。以上调整后不影响以前的合、冲、拱、同、会等规则。

    def getLYSeason(self):
        jieqi_table = self.getJieQiTable()
        spring = jieqi_table['立春']
        summer = jieqi_table['立夏']
        fall = jieqi_table['立秋']
        winter = jieqi_table['立冬']
        if compTime(spring, self.__solar) and compTime(self.__solar, summer):
            return "春"
        elif compTime(summer, self.__solar) and compTime(self.__solar, fall):
            return "夏"
        elif compTime(fall, self.__solar) and compTime(self.__solar, winter):
            return "秋"
        elif compTime(winter, self.__solar):
            return "冬"

"""