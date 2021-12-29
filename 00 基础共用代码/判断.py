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