import os
import csv
from flask import Blueprint, jsonify, request


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
