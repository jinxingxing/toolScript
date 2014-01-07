#coding: utf-8
#转为罗马数值显示(代码处理不完全， 部分数值转化后的结果不对)
#roman


def toRoman(num):
    if not 1 <= num <= 4000:
        raise ValueError(u"超出范围")
    baseNum = [1, 5, 10, 50, 100, 500, 1000]
    baseNum.reverse()
    baseRoman = ['I', 'V', 'X', 'L', 'C', 'D', 'M']
    baseRoman.reverse()
    ret = []
    for i in xrange(len(baseNum)):
        curr_num = baseNum[i]
        while num >= curr_num:
            num = num - curr_num
            ret.append(baseRoman[i])
    return ''.join(ret)
def fromRoman(string):
    pass
   
def test():
    print toRoman(8)
    #print toRoman(-1)
if __name__ == '__main__':
    test()