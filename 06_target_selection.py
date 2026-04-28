import pandas as pd
from pandas import DataFrame
from pandas import Series
import seaborn as sns
import numpy as np

# 데이터 불러오기
df = pd.read_csv('raw_data.csv')
df_recent = pd.read_csv('recent_reservation_data.csv')

# 무효 예약번호 제외
df = df[df["유효예약번호"] == "Y"]

# 내부 정책상 발송 제외 대상
df = df[~df["상세구분"].str.contains("제외코드1|제외코드2", na=False)]

# 수검자 중복 대상 최신 검진일 예약번호 1건만 잔류
df= df.loc[df.groupby("수검자번호")["검진일"].idxmax()]

# 동일 연락처 제외
df['휴대폰번호'] = (df['휴대폰번호'].fillna('').astype(str).str.replace(r'\D', '', regex=True).str.zfill(11))
dupes = df[df['휴대폰번호'].duplicated(keep=False)]
df = df[~df['휴대폰번호'].isin(dupes['휴대폰번호'])]

# 최근 예약자 제외
df_recent['휴대폰번호'] = (df_recent['휴대폰번호'].fillna('').astype(str).str.replace(r'\D', '', regex=True).str.zfill(11))
df = df[~df['휴대폰번호'].isin(df_recent['휴대폰번호'])]

# 최종 발송 대상자 내보내기
df.to_csv('최종 발송 대상자.csv', index=False, encoding='utf-8-sig')