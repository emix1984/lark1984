# -*- coding: UTF-8 -*-

# https://blog.csdn.net/python_limiao/article/details/83549280

from PIL import Image, ImageDraw, ImageFont
img = Image.open("b.jpg")
draw = ImageDraw.Draw(img) # 生成绘制对象draw
typeface = ImageFont.truetype('simkai.ttf', 38)
shopname = "店铺名称"
shopid = "2909755020"
shopweb = "www.tmall.com"

text = f"{shopname}   \n{shopid}   \n{shopweb}"


# darw.text()回执文字并生成图片
draw.text((60, 150), text, fill=(120, 0, 60),
font=typeface)
# img.show()
img.save("斗图小组.png") # 保存
