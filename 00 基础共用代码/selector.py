# 原文链接：https://blog.csdn.net/weixin_42046939/article/details/104271025
# 需求：获取article标签下的所有子标签的文本内容
# 方法：
# /text()：只能获取到第一个p标签下的文本；
# //text()：可以获取所有子标签的文本，以列表形式储存每一个子标签的文本内容；

intro = html_1.xpath('//*[@id="award"]/main/div[1]/div[3]/div[1]/div[1]/article[@class="intro  tj_"]//text()')
intro = '\n'.join(intro).strip()  #用回车符将列表里的每个元素进行分割
