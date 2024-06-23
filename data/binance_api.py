import ccxt

# Binance 선물 API 초기화
exchange = ccxt.binanceusdm()

# USDT 페어 영구 선물 종목 조회
def get_usdt_perpetual_futures_symbols():
    markets = exchange.fapiPublicGetExchangeInfo()
    symbols = [
        market['symbol'] for market in markets['symbols']
        if market['quoteAsset'] == 'USDT' and market['contractType'] == 'PERPETUAL'
    ]
    return symbols

# 종목 변환 함수
def convert_symbol(symbol):
    return symbol.replace('USDT', '/USDT')
