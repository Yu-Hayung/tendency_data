import numpy as np
import pandas as pd

df = pd.read_csv('all_data.csv')
mask = df['pass_video'].isin(['x'])
df = df[~mask]

mask = df['MBTI_result'].isin(['err'])
df = df[~mask]
print(df)



print("tendency_dataframe >>>> ", df)

df.to_csv("C:/Users/yuhay/Desktop/module/tendency_data/fin_data.csv", mode='w')