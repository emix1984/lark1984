
import re
s = '*\/:?"<>|'     #这9个字符在Windows系统下是不可以出现在文件名中的
str1 = '코스메카 >■/브이티코스메틱' # 测试用文字串 '\巴拉■한글□❸<1"!11【】>1*hgn/p:?|'
lis = f'[^\*"/:?\\|<>■□]'
# a = re.findall(lis, str1, re.S) # 去除中括号内部的符号，可以自定义
# b = "".join(a).strip()
# print(b)
if "/" in str1:
    b = "".join(re.findall(r"(.*)/", str1, re.S)[0]).strip()
    print(type(b))
    c = re.findall(r"/(.*)", str1, re.S)
    #b = "".join(b).strip()
    c = "".join(c).strip()
else:
    b = c = a
    print("1", b)
    print("2", c)

