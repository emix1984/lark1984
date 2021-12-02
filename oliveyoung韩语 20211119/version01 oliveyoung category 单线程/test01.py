import random
import re
bi_5 = '■ 제조자 : Otsuka Phamrceuticl Co., Ltd  ■ 판매자 : 한국오츠카제약'
bi_5_1_raw = re.findall(r"제조.*:(.*)■", bi_5, re.S)[0]
bi_5_1 = "".join(bi_5_1_raw).strip()
bi_5_2_raw = re.findall(r"판매.*:(.*)", bi_5, re.S)[0]
bi_5_2 = "".join(bi_5_2_raw).strip()
print('=1======', bi_5_1)
print('=2======', bi_5_2)