import jieba
fname=input("请输入要打开的文件地址及文本名称，以.txt结尾，路径要使用/:")
fo=open(fname,encoding="utf-8")
txt=fo.read()
liebiao=jieba.lcut(txt)     #分词后形成的是列表形式
counts={}
for word in liebiao:
    if len(word)==1:
        continue
    else:
        counts[word] = counts.get(word, 0) + 1
items=list(counts.items())
items.sort(key=lambda x:x[1],reverse=True)
for i in range(15):
    word,count=items[i]
    print('{:<10}{:>5}'.format(word,count))