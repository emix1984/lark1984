# -*- coding: UTF-8 -*-

# https://blog.csdn.net/python_limiao/article/details/83549280

from PIL import Image, ImageDraw, ImageFont
img = Image.open("db1.jpg")
draw = ImageDraw.Draw(img) # 生成绘制对象draw
typeface1 = ImageFont.truetype('simkai.ttf', 80)
typeface2 = ImageFont.truetype('simkai.ttf', 53)
shopname = "店铺名称"
shopid = "2909755020"
shopweb = "www.tmall.com"
channel = "天猫国际渠道"

datefrom = "2021   01   01      2022+++12+++12"
today = "2022   01   13"
code = "a20222022022013"

text1 = f"{shopname}   \n{shopid}   \n{shopweb}   \n{channel}"
text2 = f"{datefrom}   \n{today}   \n{code}"
# darw.text()回执文字并生成图片
draw.text((800, 850), text1, fill=(120, 0, 60),
font=typeface1)
draw.text((490, 1600), text2, fill=(120, 0, 60),
font=typeface2)
# img.show()
img.save("斗图小组.jpg") # 保存
