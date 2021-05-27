import cpca
import pandas as pd
import numpy as np
from pandas import DataFrame

location_str = ["浙江杭州桐庐"]
df = cpca.transform(location_str)
# 首先将pandas读取的数据转化为array
data_array = np.array(df)
print(data_array)
# 然后转化为list形式
data_list =data_array.tolist()
print(data_list[0][0]+data_list[0][1])