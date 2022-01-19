import re
# a = "1"
# if a == "":
#     print("zhaodao")
# elif a == "1":
#     print('1')
# elif a == "2":
#     print('1')
# else:
#     print('feikong')

url ="원baidu.com"
a = f'http://s'+url
a = re.sub(f'원', '999', a)
print(a)