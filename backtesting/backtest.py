import pandas as pd

# 백테스트 및 로그 생성
def backtest_strategy(signals):
    if signals.empty:
        raise ValueError("Signals DataFrame is empty.")
    
    # 수익률 계산
    signals['returns'] = signals['close'].pct_change().fillna(0)
    
    # 로그를 저장할 리스트
    log = []

    current_position = 0
    entry_price = 0
    entry_date = None

    for index, row in signals.iterrows():
        if current_position == 0 and row['position'] != 0:
            # 새로운 포지션 진입
            entry_date = row['timestamp']
            entry_price = row['close']
            current_position = row['position']
            log.append({
                'entry_date': entry_date,
                'position': 'buy' if current_position == 1 else 'sell',
                'entry_size': current_position,
                'entry_price': entry_price,
                'exit_date': None,
                'exit_price': None,
                'profit': None,
                'holding_period': None
            })
        elif current_position != 0 and row['position'] == 0:
            # 포지션 청산
            exit_date = row['timestamp']
            exit_price = row['close']
            holding_period = (exit_date - entry_date).days
            for entry in log:
                if entry['exit_date'] is None:
                    entry['exit_date'] = exit_date
                    entry['exit_price'] = exit_price
                    entry['profit'] = (exit_price - entry['entry_price']) / entry['entry_price'] * current_position
                    entry['holding_period'] = holding_period
                    break
            current_position = 0
            
        elif current_position != 0 and row['position'] != current_position:
            # 포지션 전환 (기존 포지션 청산 후 새로운 포지션 진입)
            exit_date = row['timestamp']
            exit_price = row['close']
            holding_period = (exit_date - entry_date).days
            for entry in log:
                if entry['exit_date'] is None:
                    entry['exit_date'] = exit_date
                    entry['exit_price'] = exit_price
                    entry['profit'] = (exit_price - entry['entry_price']) / entry['entry_price'] * current_position
                    entry['holding_period'] = holding_period
                    break
            # 새로운 포지션 진입
            entry_date = row['timestamp']
            entry_price = row['close']
            current_position = row['position']
            log.append({
                'entry_date': entry_date,
                'position': 'buy' if current_position == 1 else 'sell',
                'entry_size': current_position,
                'entry_price': entry_price,
                'exit_date': None,
                'exit_price': None,
                'profit': None,
                'holding_period': None
            })
            
    if current_position != 0:
        exit_date = signals.iloc[-1]['timestamp']
        exit_price = signals.iloc[-1]['close']
        holding_period = (exit_date - entry_date).days
        for entry in log:
            if entry['exit_date'] is None:
                entry['exit_date'] = exit_date
                entry['exit_price'] = exit_price
                entry['profit'] = (exit_price - entry['entry_price']) / entry['entry_price'] * current_position
                entry['holding_period'] = holding_period
                break

    # 로그를 데이터프레임으로 변환
    log_df = pd.DataFrame(log)
    return signals, log_df
