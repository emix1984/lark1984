def getext():
    fname=input("请输入要打开的文件路径及名称，以txt结尾：")
    fo=open(fname)      #打开该文件，默认是文本文件，文本文件其实就是一个字符串
    txt=fo.read()       #<文件名>.read()  默认是读取文件全部内容
    txt=txt.lower()     #将文本所有字母小写
    for ch in '!"#$%()*+<_>/:;<>=?@[\]\^_{}|~':
        txt=txt.replace(ch,'')       #将文本中含有的所有上述字符都变为空格
    return txt
hamlettxt=gettext()
words=hamlettxt.split()      #默认值，是将文本中单词按照空格分成一个一个的单词，并将结果保存成列表类型
counts={}                    #定义一个空字典类型，因为我们希望单词和该单词出现的次数作为一个键值对
for word in words:           #遍历words列表的每一个值
    counts[word]=counts.get(word,0)+1
items=list(counts.items())      #将该字典转化成一个列表,其中的键值对是以元组的形式存在
items.sort(key=lambda x:x[1],reverse=True)
for i in range(10):
    word,count=items[i]       #items[i] 是个元组，元组可以带括号，可以不带括号；赋值
    print("{:<10}{:>5}".format(word,count))