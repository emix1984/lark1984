#
# https://zhuanlan.zhihu.com/p/360444190


# # tqdm模块
#
import time
from tqdm import tqdm
for i in tqdm(range(100)):
    time.sleep(0.05)


# # progress模块
#
# import time
# from progress.bar import Bar
# #可以通过fill设置进度条填充符号，默认“#”
# #可以通过suffix设置成百分比显示
# bar = Bar("Loading", fill='$', max = 100, suffix = '%(percent)d%%')
# for i in bar.iter(range(100)):
#     time.sleep(0.01)