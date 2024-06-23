import os
import pandas as pd
import pymysql
import random
from data.database_utils import connect_to_database, create_sqlalchemy_engine, upload_data_to_db, get_table_names
from data.data_reader import read_data_from_db
from strategies.strategies import buy_and_hold, moving_average_crossover, rsi_strategy
from backtesting.backtest import backtest_strategy
from analysis.performance import select_symbols_and_period, calculate_cumulative_returns

# 설정
db_name = '1d'
host = 'localhost'
user = 'root'
password = 'kjk26363'  # 여기에 실제 비밀번호를 입력하세요

# 데이터베이스 연결
try:
    db_connection = connect_to_database(host, user, password, db_name)
    engine = create_sqlalchemy_engine(user, password, host, db_name)
except pymysql.err.OperationalError as e:
    print(f"Error connecting to the database: {e}")
    exit(1)

# 데이터베이스에서 테이블 목록 가져오기
symbols = get_table_names(db_connection)
print("Symbols from the database:", symbols)

# 데이터베이스에서 데이터 읽기
prices_data = read_data_from_db(symbols, db_connection)

# 데이터베이스에 데이터가 없으면 다운로드 및 업로드
if not prices_data:
    print("No data found in the database. Please make sure the database is populated with data.")
    exit(1)

# 사용자가 심볼을 지정하는 옵션 추가
# user_defined_symbols = input("Enter the symbols you want to use (comma separated), or press Enter to select random symbols: ")
user_defined_symbols = []

if user_defined_symbols:
    selected_symbols = user_defined_symbols.split(',')
    selected_symbols = [sym.strip() for sym in selected_symbols if sym.strip() in symbols]
    if not selected_symbols:
        print("No valid symbols entered. Exiting.")
        exit(1)
else:
    # 랜덤으로 10종목 선택
    selected_symbols = random.sample(symbols, 30)

print("Selected symbols:", selected_symbols)

# 선택된 종목과 기간 출력
selected_data = select_symbols_and_period(prices_data, selected_symbols=selected_symbols, period_days=365, same_period=True)

# 각 전략의 누적 수익률 계산
strategies = [buy_and_hold, moving_average_crossover, rsi_strategy]
cumulative_returns_df = calculate_cumulative_returns(selected_data, strategies)

# 결과 출력
print(cumulative_returns_df)
print("Average Buy and Hold Return:", cumulative_returns_df['buy_and_hold'].mean())
print("Average Moving Average Return:", cumulative_returns_df['moving_average_crossover'].mean())
print("Average RSI Return:", cumulative_returns_df['rsi_strategy'].mean())

# 연결 종료
db_connection.close()
