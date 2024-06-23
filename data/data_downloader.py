import pandas as pd
import ccxt

# Binance 선물 API 초기화
exchange = ccxt.binanceusdm()

# 데이터 다운로드 함수
def download_data(symbol, timeframe='1d', since=exchange.parse8601('2018-01-01T00:00:00Z'), limit=500):
    all_data = []
    since_timestamp = since
    
    while True:
        data = exchange.fetch_ohlcv(symbol, timeframe, since=since_timestamp, limit=limit)
        if not data:
            break
        since_timestamp = data[-1][0] + 1  # 다음 요청의 시작 시간 설정
        all_data += data
        if len(data) < limit:
            break

    df = pd.DataFrame(all_data, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    return df
