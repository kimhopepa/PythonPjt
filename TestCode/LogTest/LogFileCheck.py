import re
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib.dates as mdates
from datetime import datetime
import matplotlib.font_manager as fm

# 한글 폰트 설정
font_path = '/usr/share/fonts/truetype/nanum/NanumGothic.ttf'  # 시스템에 맞는 한글 폰트 경로 설정
font_prop = fm.FontProperties(fname=font_path)
plt.rcParams['font.family'] = font_prop.get_name()


def parse_logs(file_name):
    # 파일 읽기
    with open(file_name, 'r', encoding='utf-8') as file:
        log_data = file.read()

    # 정규 표현식 패턴 정의
    log_pattern = re.compile(r"""
        ^WCCOAs7\s+\(1\),\s+        # 장치 및 인스턴스
        (?P<timestamp>[\d.:\s]+),\s # 타임스탬프
        SYS,\s+                     # 시스템 식별자
        (?P<level>\w+),\s+          # 로그 레벨
        (?P<code>[\w\/]+),\s+       # 코드
        (?P<message>.+)             # 메시지
        """, re.VERBOSE | re.MULTILINE)

    # 로그 파싱하여 데이터프레임 생성
    logs = []
    for match in log_pattern.finditer(log_data):
        logs.append(match.groupdict())

    df = pd.DataFrame(logs)

    # 타임스탬프를 datetime으로 변환
    df['timestamp'] = pd.to_datetime(df['timestamp'], format='%Y.%m.%d %H:%M:%S.%f')

    return df


def aggregate_and_plot(df):
    # 로그 레벨별 집계
    log_level_counts = df['level'].value_counts()

    # 시간별 로그 발생 수 집계 (시간 단위)
    df.set_index('timestamp', inplace=True)
    hourly_counts = df.groupby(['level']).resample('H').size().unstack(level=0, fill_value=0)

    # 시각화
    plt.figure(figsize=(14, 7))

    # 로그 레벨별 집계 차트
    plt.subplot(1, 2, 1)
    log_level_counts.plot(kind='bar', color='skyblue')
    plt.title('로그 레벨별 발생 수')
    plt.xlabel('로그 레벨')
    plt.ylabel('발생 수')

    # 시간별 로그 발생 수 차트 (로그 레벨별 색상)
    plt.subplot(1, 2, 2)
    ax = hourly_counts.plot(kind='line', marker='o', ax=plt.gca())
    plt.title('시간별 로그 발생 수')
    plt.xlabel('시간')
    plt.ylabel('로그 수')

    # 한글로 시간 표시 설정
    date_form = DateFormatter("%Y년 %m월 %d일 %H시", fontproperties=font_prop)
    ax.xaxis.set_major_formatter(date_form)

    # 틱 간격 설정 (예: 6시간 간격)
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))  # 6시간 간격으로 설정

    plt.legend(title='로그 레벨')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


# 파일 이름 입력 받기
# file_name = input("분석할 로그 파일의 이름을 입력하세요: ")
file_name = r'D:\SIT_PROGRAM\316\SVR_P2_M154_UPS\log\PVSS_II.log'
# 로그 파일 파싱
df = parse_logs(file_name)

# 데이터 집계 및 시각화
aggregate_and_plot(df)