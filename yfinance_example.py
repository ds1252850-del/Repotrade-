import yfinance as yf

def fetch_stock_data(ticker):
    # Download historical market data for the given ticker
    data = yf.download(ticker, period="5d")
    print(f"Data for {ticker}:")
    print(data)

if __name__ == "__main__":
    fetch_stock_data("AAPL")  # Example: Apple Inc.
