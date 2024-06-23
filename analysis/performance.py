import pandas as pd
import random
from datetime import datetime, timedelta
from backtesting.backtest import backtest_strategy

# 선택된 종목과 시작일을 선택
def select_symbols_and_period(prices_data, selected_symbols, period_days=365, same_period=True):
    current_date = datetime.now()
    
    selected_data = {}
    
    if same_period:
        # 같은 기간을 모든 종목에 적용
        symbol_data = prices_data[selected_symbols[0]]
        symbol_data['timestamp'] = pd.to_datetime(symbol_data['timestamp'])
        max_start_date = symbol_data['timestamp'].max() - timedelta(days=period_days)
        
        # 랜덤 시작일 선택
        while True:
            start_date = symbol_data['timestamp'].min() + timedelta(days=random.randint(0, (symbol_data['timestamp'].max() - symbol_data['timestamp'].min()).days - period_days))
            end_date = start_date + timedelta(days=period_days)
            period_data = symbol_data[(symbol_data['timestamp'] >= start_date) & (symbol_data['timestamp'] <= end_date)]
            if len(period_data) >= period_days:  # 데이터가 충분한 경우에만 선택
                break
        
        for symbol in selected_symbols:
            symbol_data = prices_data[symbol]
            symbol_data['timestamp'] = pd.to_datetime(symbol_data['timestamp'])
            data = symbol_data[(symbol_data['timestamp'] >= start_date) & (symbol_data['timestamp'] <= end_date)]
            selected_data[symbol] = {
                'data': data,
                'start_date': start_date,
                'end_date': end_date
            }
    else:
        # 종목별로 다른 기간을 적용
        for symbol in selected_symbols:
            symbol_data = prices_data[symbol]
            symbol_data['timestamp'] = pd.to_datetime(symbol_data['timestamp'])
            symbol_start_date = symbol_data['timestamp'].min()
            symbol_end_date = symbol_data['timestamp'].max()
            
            # 최대 시작 날짜를 설정 (최소 시작 날짜에서 period_days 이전)
            max_start_date = symbol_end_date - timedelta(days=period_days)
            max_start_date = max(symbol_start_date, max_start_date)
            
            # 랜덤 시작일 선택
            while True:
                start_date = symbol_start_date + timedelta(days=random.randint(0, (symbol_end_date - symbol_start_date).days - period_days))
                end_date = start_date + timedelta(days=period_days)
                period_data = symbol_data[(symbol_data['timestamp'] >= start_date) & (symbol_data['timestamp'] <= end_date)]
                if len(period_data) >= period_days:  # 데이터가 충분한 경우에만 선택
                    break
            
            selected_data[symbol] = {
                'data': period_data,
                'start_date': start_date,
                'end_date': end_date
            }
    
    return selected_data

# 각 전략의 누적 수익률 계산
def calculate_cumulative_returns(selected_data, strategies):
    cumulative_returns_df = pd.DataFrame(columns=[strategy.__name__ for strategy in strategies])

    for symbol, info in selected_data.items():
        data = info['data']
        returns = {}
        
        for strategy in strategies:
            signals = strategy(data)
            _, log_df = backtest_strategy(signals)
            cumulative_return = log_df['profit'].sum()
            returns[strategy.__name__] = cumulative_return
        
        cumulative_returns_df.loc[symbol] = returns

    cumulative_returns_df.loc['Total'] = cumulative_returns_df.mean()
    return cumulative_returns_df
