# 调试提示颜色
# https://blog.csdn.net/qq_33567641/article/details/82769523
# Python基础之控制台输出颜色

print("△▽▽▽▽▽▽▽▽▽▽字体颜色调试▽▽▽▽▽▽▽▽▽▽△")
print("\033[31m这是红色字体\033[0m")
print("\033[32m这是绿色字体\033[0m")
print("\033[33m这是黄色字体\033[0m")
print("\033[34m这是蓝色字体\033[0m")
print("\033[38m这是默认字体\033[0m")  # 大于37将显示默认字体

print("△▽▽▽▽▽▽▽▽▽▽背景色调试▽▽▽▽▽▽▽▽▽▽△")
print(">>>\033[00;40m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;41m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;42m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;43m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;44m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;45m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;46m页面内商品不存在或已下架！\033[0m")
print(">>>\033[00;47m页面内商品不存在或已下架！\033[0m")