import pymysql
import pandas as pd

# 데이터베이스에서 데이터 읽기 함수
def read_data_from_db(symbols, db_connection):
    cursor = db_connection.cursor()
    prices_data = {}

    for sym in symbols:
        query = f"SELECT * FROM {sym}"
        cursor.execute(query)
        results = cursor.fetchall()

        # 데이터가 존재하지 않으면 건너뜀
        if not results:
            continue

        # 열 이름 추출
        columns = [desc[0] for desc in cursor.description]

        # Pandas DataFrame으로 변환
        ohlcv_df = pd.DataFrame(results, columns=columns)
        ohlcv_df['timestamp'] = pd.to_datetime(ohlcv_df['timestamp'])

        prices_data[sym] = ohlcv_df

    return prices_data
