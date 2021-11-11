import numpy as np
import pandas as pd

df = pd.read_csv('Group_result.csv')
# mask = df['pass_video'].isin(['x'])
# df = df[~mask]

Group = df['qzGroup']
Group_list = list(np.array(Group.tolist()))

import pymysql

#####  DB 접근 하는 방법   ###############################################################################
host = 'withmindim.ciravsrvnjpk.ap-northeast-2.rds.amazonaws.com'
port = 3306
database ="kangmin"
username = "root"
password = "withmind1!"


conn = pymysql.connect(host=host,
                       user=username,
                       db=database,
                       password=password,
                       use_unicode=True,
                       charset='utf8')
cursor = conn.cursor()

########################################################################################################

data_df = {
    'qzGroup':'0000',
    'Key_word':[['구체적','체계적','열성적','경험적','논리적','현실적','개방성','능동적',]],
    'E':0,
    'I':0,
    'T':0,
    'F':0,
    'MBTI_result': 'ET'
}

tendency_dataframe = pd.DataFrame(data_df)
print(tendency_dataframe)

num = 1
Group_list_len = len(Group_list)

for i in Group_list:
    sql = "SELECT MK_KEYWORD AS keyWord \
            FROM IM_MTBI_DATA AS MD \
            LEFT OUTER JOIN IM_MTBI_KEYWORD AS MK \
            ON MD.MK_PK=MK.MK_PK \
            WHERE MD.QZ_GROUP = {}\
            ORDER BY MD.MT_PICK ASC ; " .format(i)

    cursor.execute(sql)
    result = cursor.fetchall()
    print('result >>> ', result)


    E = 0
    I = 0
    T = 0
    F = 0
    etc = 0

    result_txt = []

    for j in result:
        result_txt.append(j[0])

        if j[0] in '능동적':
            E += 1
        elif j[0] in '표현적':
            E += 1
        elif j[0] in '열성적':
            E += 1
        elif j[0] in '보유적':
            I += 1
        elif j[0] in '정적':
            I += 1
        elif j[0] in '행동안전성':
            I += 1
        elif j[0] in '논리적':
            T += 1
        elif j[0] in '이성적':
            T += 1
        elif j[0] in '비평적':
            T += 1
        elif j[0] in '정서적':
            F += 1
        elif j[0] in '감성적':
            F += 1
        elif j[0] in '허용적':
            F += 1
        else:
            etc += 1


    if E > I and T > F:
        MBTI_result = 'ET'
    elif E < I and T < F:
        MBTI_result = 'IF'
    elif E < I and T > F:
        MBTI_result = 'IT'
    elif E > I and T < F:
        MBTI_result = 'EF'
    else:
        MBTI_result = 'err'

    print('E : {}, I : {}, T : {}, F : {}, etc : {} , MBTI_result :{} '.format(E, I, T, F, etc, MBTI_result))


    i_data = {
        'qzGroup': i,
        'Key_word': result_txt,
        'E': E,
        'I': I,
        'T': T,
        'F': F,
        'MBTI_result': MBTI_result,
    }
    tendency_dataframe = tendency_dataframe.append(i_data, ignore_index=True)

    print('{}번째 분석중 - 총 : {}'.format(num, Group_list_len))
    num += 1

conn.commit()
conn.close()


print("tendency_dataframe >>>> ", tendency_dataframe)

tendency_dataframe.to_csv("C:/Users/yuhay/Desktop/module/tendency_data/tendency_df.csv", mode='w')


