# !/usr/bin/env python
#  -*- coding:utf-8 -*-

""" 汉字处理的工具:
判断unicode是否是汉字，数字，英文，或者其他字符。
全角符号转半角符号。 """
import chardet
import sys
from time import sleep


def is_chinese(uchar):
    """ 判断一个unicode是否是汉字 """
    if uchar >= u'\u4e00' and uchar <= u'\u9fa5':
        return True
    else:
        return False


def is_number(uchar):
    """ 判断一个unicode是否是数字 """
    if uchar >= u'\u0030' and uchar <= u'\u0039':
        return True
    else:
        return False


def is_alphabet(uchar):
    """ 判断一个unicode是否是英文字母 """
    if (uchar >= u'\u0041' and uchar <= u'\u005a') or (uchar >= u'\u0061' and uchar <= u'\u007a'):
        return True
    else:
        return False


def is_other(uchar):
    """ 判断是否非汉字，数字，英文字符 """
    if not (is_chinese(uchar) or is_number(uchar) or is_alphabet(uchar)):  # or (uchar == u'\u0028') or (uchar == u'\u0029')
        return True
    else:
        return False


def contain(unchar, word1, word2, word3):
    sen1 = unchar.partition(word1)
    if sen1[0] == unchar:
        return False
    else:
        sen2 = sen1[2].partition(word2)
        if sen2[0] == sen1[2]:
            return False
        else:
            if word3:
                sen3 = sen2[2].partition(word3)
                if sen3[0] == sen2[2]:
                    return False
                else:
                    # print sen3,unchar
                    return True
            else:
                # print unchar,sen2
                return True

with open('input.txt') as file:
    keyfile = open('keywords.txt', 'rb')
    keyword = [i.strip().decode('utf-8') for i in keyfile.readlines()]
    keyfile.close()
    locatefile = open('area.lst', 'rb')
    locate = [i.split('㈱')[0].strip().decode('utf-8')
              for i in locatefile.readlines()]
    locatefile.close()
    startfile = open('start.txt', 'rb')
    start = [i.strip().decode('utf-8') for i in startfile.readlines()]
    startfile.close()
    conttfile = open('contt.txt', 'rb')
    contt = [i.strip().decode('utf-8') for i in conttfile.readlines()]
    conttfile.close()
    numlist = u'一二三四五六七八九十两个'
    code = u'·“”””? ** “...  {  }'

    flag = True
    result = []
    j=0
    while flag:
        j +=1
        line = file.readline().strip()
        if len(line) != 0:
            lineu = line.decode('utf-8')
            work = 0

            # 判断是否包含数字和字母
            nums = 0
            for i in lineu:
                if is_number(i) or is_alphabet(i):
                    nums += 1
            if nums:
                work += 1

            # 判断是否包含指定标点
            for i in code:
                if i in lineu:
                    work += 1

            # 判断包含指定词
            for i in keyword:
                if i in lineu:
                    work += 1

            # 判断包含开始词
            for i in start:
                if lineu.startswith(i):
                    work += 1

            for i in locate:
                # 判断（地名）开头
                if lineu.startswith(u'（' + i) or lineu.startswith(u'(' + i):
                    work += 1
                # 判断地名+到
                elif contain(lineu, i, u'到', u''):
                    work += 1
                # 判断地名重叠
                elif contain(lineu, i, i, u''):
                    work += 1
                # 判断地名+'一'
                elif (i+u'一') in lineu: #contain(lineu, i, u'一', u''):
                    work += 1
                else:
                    pass
            #for i in contt:
            #    if contain(lineu,i,u'公司',u''):
            #        work +=1

            for i in numlist:
                if contain(lineu, u'日本', i, u'大') or contain(lineu, u'日本', i, u'家') or contain(lineu, u'世界', i, u'大'):
                    work += 1
                elif contain(lineu, u'日本', u'前', i) or contain(lineu, u'日本', u'全国', i):
                    work += 1
                else:
                    pass

            if work > 0:
                result.append(lineu)

            print 'Comparing! Done number:',j
            sys.stdout.flush()
            #sleep(1)

        else:
            flag = False
    output=open('result.txt','wb')
    for i in result:
        output.write(i.encode('utf-8'))
        output.write('\n')
    #output.writelines(result)
    output.close()
    #for i in result:
    #    print i,len(result)
    print 'done!'
    raw_input()
    # print lineu

    # print lineu
    # print lineu,type(lineu)  ,j
