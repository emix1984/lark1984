# 判断空值
# 发现Nonetype类型，其实就是值为None，Nonetype和空值是不一致的，可以理解为Nonetype为不存在这个参数。空值表示参数存在，但是值为空。
# https://blog.csdn.net/fu6543210/article/details/89462036
p1 = () #空元组
p2 = [] #空列表
p3 = {} #空字典
p4 = 0  #变量0
p5 = '' #变量空字符串
p6 = False #变量假
p7= None # None相当于NoneType 注意大小写

# 判断代码示例
if review_4 is None:
    print(type(review_4), 'review4空')
    review_4 = ""
else:
    review_4 = review_4.strip()
    print(type(review_4), "review4非空")

## continue、pass、break的区别
# pass
#
# 不做任何事情，只起到占位的作用，也就是说它是一个空操作
#
# continue
#
# 当continue语句在循环结构中执行时，并不会退出循环结构，而是立即结束本次循环，重新开始下一轮循环，也就是说，跳过循环体中在continue语句之后的所有语句，继续下一轮循环。
#
# break
#
# 当break语句在循环结构中执行时，它会导致立即跳出循环结构，转而执行该结构后面的语句。
#
# exit()
#
# 结束整个程序