import yfinance as yf
import pandas as pd

def download_ohlc(symbols, period='6mo', interval='1d'):
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period=period, interval=interval)
            if not hist.empty:
                data[symbol] = hist[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            print(f"Error downloading {symbol}: {e}")
    return data

def calculate_bullish_stocks(ohlc_data):
    bullish = []
    for symbol, df in ohlc_data.items():
        if len(df) < 150:
            continue
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['SMA150'] = df['Close'].rolling(window=150).mean()
        latest = df.iloc[-1]
        # Bullish if price above both SMAs
        if latest['Close'] > latest['SMA50'] and latest['Close'] > latest['SMA150']:
            bullish.append(symbol)
    return bullish

if __name__ == "__main__":
    # Example usage
    symbols = ['AAPL', 'MSFT', 'TSLA', 'GOOGL']
    ohlc_data = download_ohlc(symbols)
    bullish_stocks = calculate_bullish_stocks(ohlc_data)
    print("Bullish stocks:", bullish_stocks)
