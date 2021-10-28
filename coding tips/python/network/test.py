# coding=utf-8

import  re

#re.search()方法验证字符串是否符合正则表达式
s1 = "asdCVE , command, Command,"
an = re.search ('(cve|command)', s1, re.IGNORECASE)
if an :
    print("yes")
else :
    print("no")