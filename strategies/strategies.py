import pandas as pd
import numpy as np

# 전략 1: 매수 후 보유
def buy_and_hold(data):
    signals = pd.DataFrame(index=data.index)
    signals['position'] = 1  # 항상 매수
    return pd.concat([data, signals], axis=1)

# 전략 2: 이동 평균 교차
def moving_average_crossover(data, short_window=3, long_window=12):
    signals = pd.DataFrame(index=data.index)
    signals['short_mavg'] = data['close'].rolling(window=short_window, min_periods=1).mean()
    signals['long_mavg'] = data['close'].rolling(window=long_window, min_periods=1).mean()
    
    signals['signal'] = 0
    signals['signal'] = np.where(signals['short_mavg'] > signals['long_mavg'], 1, signals['signal'])
    signals['signal'] = np.where(signals['short_mavg'] < signals['long_mavg'], -1, signals['signal'])
    
    signals['position'] = signals['signal'].ffill().fillna(0)
    
    return pd.concat([data, signals.drop(columns=['signal'])], axis=1)

# 전략 3: RSI 전략
def rsi_strategy(data, period=14, oversold=30, overbought=70):
    delta = data['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    
    signals = pd.DataFrame(index=data.index)
    signals['rsi'] = rsi
    signals['signal'] = 0
    signals.loc[rsi < oversold, 'signal'] = 1
    signals.loc[rsi > overbought, 'signal'] = -1
    
    signals['position'] = signals['signal'].ffill().fillna(0)
    
    return pd.concat([data, signals.drop(columns=['signal'])], axis=1)
