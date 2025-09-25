import os
import csv

from flask import Blueprint, jsonify, request
import pandas as pd
import yfinance as yf
from flask import session
industry_api = Blueprint('industry_api', __name__)

# API endpoint to download OHLC and screen bullish stocks
@industry_api.route('/api/bullish-stocks', methods=['POST'])
def bullish_stocks():
    symbols = request.json.get('symbols')
    if not symbols or not isinstance(symbols, list):
        return jsonify({'error': 'symbols (list) required'}), 400
    # Download OHLC data
    data = {}
    for symbol in symbols:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period='6mo', interval='1d')
            if not hist.empty:
                data[symbol] = hist[['Open', 'High', 'Low', 'Close', 'Volume']]
        except Exception as e:
            data[symbol] = f"Error: {e}"
    # Screen for bullish stocks
    bullish = []
    for symbol, df in data.items():
        if isinstance(df, str) or len(df) < 150:
            continue
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['SMA150'] = df['Close'].rolling(window=150).mean()
        latest = df.iloc[-1]
        if latest['Close'] > latest['SMA50'] and latest['Close'] > latest['SMA150']:
            bullish.append(symbol)
    return jsonify({'bullish_stocks': bullish})
import os
import csv

from flask import Blueprint, jsonify, request
import pandas as pd


from flask import session
industry_api = Blueprint('industry_api', __name__)

# Helper to check if user is logged in (not admin)
def require_user_session():
    user_data = session.get('mock_user_data')
    if not user_data or user_data.get('is_admin', False):
        return False
    return True

CSV_PATH = os.path.join(os.path.dirname(__file__), 'Stocks002025Format.csv')

# Helper to read CSV and cache results
_industry_cache = None
_symbol_cache = None

def _load_csv():
    global _industry_cache, _symbol_cache
    if _industry_cache is not None and _symbol_cache is not None:
        return _industry_cache, _symbol_cache
    industries = set()
    symbols_by_industry = {}
    with open(CSV_PATH, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            industry = row.get('industry')
            symbol = row.get('symbol')
            if industry:
                industries.add(industry)
                if industry not in symbols_by_industry:
                    symbols_by_industry[industry] = set()
                if symbol:
                    symbols_by_industry[industry].add(symbol)
    _industry_cache = sorted(list(industries))
    _symbol_cache = {k: sorted(list(v)) for k, v in symbols_by_industry.items()}
    return _industry_cache, _symbol_cache


# Only logged-in users can list industries
@industry_api.route('/api/industries', methods=['GET'])
def get_industries():
    if not require_user_session():
        return jsonify({'error': 'Unauthorized'}), 401
    industries, _ = _load_csv()
    return jsonify({'industries': industries})


# Only logged-in users can list symbols
@industry_api.route('/api/symbols', methods=['GET'])
def get_symbols():
    if not require_user_session():
        return jsonify({'error': 'Unauthorized'}), 401
    industry = request.args.get('industry')
    _, symbol_cache = _load_csv()
    symbols = symbol_cache.get(industry, [])
    return jsonify({'symbols': symbols})


# New endpoint: Upload CSV and calculate industry benchmark (skeleton)
@industry_api.route('/api/industry-benchmark', methods=['POST'])
def industry_benchmark():
    file = request.files.get('file')
    if not file:
        return jsonify({'error': 'No file uploaded'}), 400
    try:
        df = pd.read_csv(file)
        # Ensure required columns exist
        required_cols = {'symbol', 'industry', 'market_cap', 'price_vs_sma_pct'}
        if not required_cols.issubset(df.columns):
            return jsonify({'error': f'Missing columns: {required_cols - set(df.columns)}'}), 400

        # Convert market_cap to numeric
        df['market_cap'] = pd.to_numeric(df['market_cap'], errors='coerce').fillna(0)
        # Convert price_vs_sma_pct to numeric (remove % and convert to float)
        df['price_vs_sma_pct'] = df['price_vs_sma_pct'].astype(str).str.replace('%','').astype(float)

        # Normalize price_vs_sma_pct to 1.0 on first day (simulate with min value per symbol)
        df['normalized_price'] = df.groupby('symbol')['price_vs_sma_pct'].transform(lambda x: x / x.iloc[0] if x.iloc[0] != 0 else 1)

        # Group by industry and calculate benchmarks
        industry_results = {}
        industry_benchmarks = {}
        for industry, group in df.groupby('industry'):
            total_market_cap = group['market_cap'].sum()
            if total_market_cap == 0:
                continue
            group = group.copy()
            group['weight'] = group['market_cap'] / total_market_cap
            # Weighted average benchmark for industry
            benchmark = (group['weight'] * group['normalized_price']).sum()
            industry_benchmarks[industry] = benchmark
            industry_results[industry] = {
                'benchmark': benchmark,
                'symbols': group['symbol'].tolist(),
                'weights': group['weight'].round(4).tolist(),
                'normalized_prices': group['normalized_price'].round(4).tolist()
            }

        # Calculate MRS for each stock: (Industry_Normalized / Stock_Normalized) – 1
        mrs_results = {}
        for idx, row in df.iterrows():
            industry = row['industry']
            stock_norm = row['normalized_price']
            industry_norm = industry_benchmarks.get(industry, None)
            if stock_norm and industry_norm is not None and stock_norm != 0:
                mrs = (industry_norm / stock_norm) - 1
            else:
                mrs = None
            mrs_results[row['symbol']] = mrs

        # Detect bullish and bearish industries
        # Criteria: price_vs_sma_pct > 0 (i.e., price above 50SMA) OR weekly_growth > 0.2 (20%)
        bullish_industries = set()
        bearish_industries = set()
        for industry, group in df.groupby('industry'):
            above_50sma = (group['price_vs_sma_pct'] > 0).any()
            weekly_growth = pd.to_numeric(group.get('weekly_growth', 0), errors='coerce').fillna(0)
            strong_growth = (weekly_growth > 0.2).any()
            if above_50sma or strong_growth:
                bullish_industries.add(industry)
            else:
                bearish_industries.add(industry)

        return jsonify({
            'industry_benchmarks': industry_results,
            'mrs': mrs_results,
            'bullish_industries': list(bullish_industries),
            'bearish_industries': list(bearish_industries)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
