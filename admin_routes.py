
from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
import datetime
import csv
import io
import models
from app import db
User = models.User
Watchlist = models.Watchlist
import json
import tempfile

# Blueprint must be defined before any route decorators
admin_bp = Blueprint('admin', __name__)

# In-memory storage for uploaded screening stocks (for demo; replace with DB for production)
SCREENING_STOCKS = []


# Admin-only endpoint for CSV upload for screening (only admin can upload industry CSVs)
@admin_bp.route('/admin/api/screening-csv-upload', methods=['POST'])
def screening_csv_upload():
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    # Only admin can upload industry CSVs
    if 'csvFile' not in request.files:
        return jsonify({'success': False, 'error': 'No file uploaded'}), 400
    file = request.files['csvFile']
    if not file.filename.endswith('.csv'):
        return jsonify({'success': False, 'error': 'Invalid file type'}), 400
    try:
        stream = io.StringIO(file.stream.read().decode('utf-8'))
        reader = csv.DictReader(stream)
        new_stocks = []
        for row in reader:
            # Basic fields: symbol, name, sector, price, etc.
            stock = {
                'symbol': row.get('symbol', '').upper(),
                'name': row.get('name', ''),
                'sector': row.get('sector', ''),
                'price': row.get('price', ''),
                'industry': row.get('industry', ''),
                'market_cap': row.get('market_cap', ''),
                'latest_volume': row.get('latest_volume', ''),
            }
            new_stocks.append(stock)
        # Store in-memory for demo (replace with DB in production)
        global SCREENING_STOCKS
        SCREENING_STOCKS = new_stocks
        return jsonify({'success': True, 'count': len(new_stocks)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Endpoint to get uploaded screening stocks
@admin_bp.route('/admin/api/screening-uploaded-stocks', methods=['GET'])
def get_screening_uploaded_stocks():
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    return jsonify({'success': True, 'stocks': SCREENING_STOCKS})

from flask import Blueprint, render_template, session, redirect, url_for, jsonify, request
import datetime
import csv
import io
import models
from app import db
User = models.User
Watchlist = models.Watchlist
import json

# Blueprint must be defined before any route decorators
admin_bp = Blueprint('admin', __name__)

def require_admin_session():
    """Check if user is logged in as admin in session"""
    user_data = session.get('mock_user_data')
    if not user_data or not user_data.get('is_admin', False):
        return False
    return True

# TEMPORARY: Public test endpoint to list all users
@admin_bp.route('/admin/api/test-all-users', methods=['GET'])
def test_all_users():
    all_users = User.query.all()
    result = []
    for u in all_users:
        result.append({
            'id': u.id,
            'email': getattr(u, 'email', None),
            'full_name': getattr(u, 'full_name', None),
            'subscription_tier': getattr(u, 'subscription_tier', None)
        })
    return jsonify({'success': True, 'users': result})

# TEMPORARY: Public test endpoint to verify Entry Zone and Breakout watchlists data
@admin_bp.route('/admin/api/test-all-watchlists', methods=['GET'])
def test_all_watchlists():
    all_watchlists = Watchlist.query.all()
    result = []
    for wl in all_watchlists:
        result.append({
            'id': wl.id,
            'name': wl.name,
            'user_id': wl.user_id,
            'watchlist_type': wl.watchlist_type,
            'stocks': wl.stocks,
            'created_at': wl.created_at.isoformat() if wl.created_at else None
        })
    return jsonify({'success': True, 'watchlists': result})

# Entry Zone and Breakout Stocks endpoints
# Get all Entry Zone Stocks (admin)
@admin_bp.route('/admin/api/entry-zone-stocks', methods=['GET'])
def get_entry_zone_stocks():
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    entry_lists = Watchlist.query.filter_by(watchlist_type='entry').all()
    stocks = []
    for wl in entry_lists:
        for s in wl.stocks:
            stocks.append({
                'symbol': s.get('symbol'),
                'industry': s.get('industry'),
                'latest_volume': s.get('latest_volume'),
                'total_market_cap_formatted': s.get('total_market_cap_formatted')
            })
    return jsonify({'success': True, 'stocks': stocks})

# Get all Breakout Stocks (admin)
@admin_bp.route('/admin/api/breakout-stocks', methods=['GET'])
def get_breakout_stocks():
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    breakout_lists = Watchlist.query.filter_by(watchlist_type='breakout').all()
    stocks = []
    for wl in breakout_lists:
        for s in wl.stocks:
            stocks.append({
                'symbol': s.get('symbol'),
                'industry': s.get('industry'),
                'latest_volume': s.get('latest_volume'),
                'total_market_cap_formatted': s.get('total_market_cap_formatted')
            })
    return jsonify({'success': True, 'stocks': stocks})

# Mock data for admin functionality
MOCK_USERS = [
    {
        'id': '1',
        'email': 'admin@tradinggrow.com',
        'full_name': 'Admin User',
        'subscription_tier': 'pro',
        'is_admin': True,
        'created_at': '2024-01-01T00:00:00Z'
    },
    {
        'id': '2',
        'email': 'demo@tradinggrow.com',
        'full_name': 'Demo User',
        'subscription_tier': 'pro',
        'is_admin': False,
        'created_at': '2024-01-15T00:00:00Z'
    },
    {
        'id': '3',
        'email': 'user1@example.com',
        'full_name': 'John Smith',
        'subscription_tier': 'medium',
        'is_admin': False,
        'created_at': '2024-02-01T00:00:00Z'
    },
    {
        'id': '4',
        'email': 'user2@example.com',
        'full_name': 'Jane Doe',
        'subscription_tier': 'free',
        'is_admin': False,
        'created_at': '2024-02-15T00:00:00Z'
    },
    {
        'id': '5',
        'email': 'user3@example.com',
        'full_name': 'Bob Wilson',
        'subscription_tier': 'free',
        'is_admin': False,
        'created_at': '2024-03-01T00:00:00Z'
    }
]

MOCK_STOCKS = [
    {'id': '1', 'symbol': 'AAPL', 'industry': 'Technology', 'market_cap': '2500000000000', 'market_cap_formatted': '$2.5T', 'latest_volume': '100000000', 'mrs_current': '1.2', 'weekly_growth': '+2.5%', 'total_stocks': '500', 'total_market_cap_formatted': '$10T', 'price_vs_sma_pct': '10.00%'},
    {'id': '2', 'symbol': 'TSLA', 'industry': 'Automotive', 'market_cap': '800000000000', 'market_cap_formatted': '$800B', 'latest_volume': '50000000', 'mrs_current': '1.1', 'weekly_growth': '+3.2%', 'total_stocks': '500', 'total_market_cap_formatted': '$10T', 'price_vs_sma_pct': '12.00%'},
    {'id': '3', 'symbol': 'MSFT', 'industry': 'Technology', 'market_cap': '2300000000000', 'market_cap_formatted': '$2.3T', 'latest_volume': '75000000', 'mrs_current': '1.3', 'weekly_growth': '+1.8%', 'total_stocks': '500', 'total_market_cap_formatted': '$10T', 'price_vs_sma_pct': '9.00%'}
]

MOCK_SUBSCRIPTION_REQUESTS = [
    {
        'id': '1',
        'user_id': '3',
        'user_name': 'John Smith',
        'user_email': 'user1@example.com',
        'current_tier': 'medium',
        'requested_tier': 'pro',
        'created_at': '2024-03-15T10:00:00Z'
    }
]

@admin_bp.route('/admin/login')
def admin_login():
    """Admin login page"""
    return render_template('spa.html')

@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    """Admin dashboard page"""
    if not require_admin_session():
        return redirect('/admin/login')
    return render_template('spa.html')

@admin_bp.route('/admin/logout', methods=['GET', 'POST'])
def admin_logout():
    """Admin logout endpoint"""
    session.pop('mock_user_id', None)
    session.pop('mock_user_data', None)
    session.pop('is_admin', None)
    
    # Return JSON for AJAX requests, redirect for direct browser access
    if request.method == 'POST' or request.headers.get('Content-Type') == 'application/json':
        return jsonify({'message': 'Logged out successfully'})
    else:
        return redirect('/admin/login')


# API Endpoints

# In-memory mock screenings list
MOCK_SCREENINGS = [
    {
        'id': 1,
        'name': 'High Growth Stocks',
        'criteria': {
            'min_price': 10,
            'max_price': 1000,
            'min_volume': 100000,
            'min_market_cap': 1000000000,
            'pe_ratio_max': 50,
            'sectors': ['Technology', 'Healthcare']
        },
        'results_data': {'stocks': []},
        'created_at': '2024-03-15T10:00:00Z'
    }
]

@admin_bp.route('/admin/stock-screening/create', methods=['POST'])
def create_stock_screening():
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'success': False, 'error': 'Missing screening name'}), 400
    criteria = data.get('criteria', {})
    results = data.get('results_data', {'stocks': []})
    screening = StockScreening(
        name=data['name'],
        criteria=criteria,
        results=results,
        created_by='1'  # TODO: Use real admin id from session
    )
    screening.save()
    return jsonify({'success': True, 'screening': {
        'id': screening.id,
        'name': screening.name,
        'criteria': screening.criteria_data,
        'results_data': screening.results_data,
        'created_at': screening.created_at.isoformat() + 'Z'
    }})

# List all screenings (for admin dashboard)
@admin_bp.route('/admin/api/stock-screenings', methods=['GET'])
def list_stock_screenings():
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    screenings = StockScreening.get_all()
    return jsonify({'success': True, 'screenings': [
        {
            'id': s.id,
            'name': s.name,
            'criteria_data': s.criteria_data,
            'results_data': s.results_data,
            'created_at': s.created_at.isoformat() + 'Z'
        } for s in screenings
    ]})

# Get a single screening by id
@admin_bp.route('/admin/api/stock-screenings/<screening_id>', methods=['GET'])
def get_stock_screening(screening_id):
    if not require_admin_session():
        return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    screening = StockScreening.get(screening_id)
    if not screening:
        return jsonify({'success': False, 'error': 'Screening not found'}), 404
    return jsonify({'success': True, 'screening': {
        'id': screening.id,
        'name': screening.name,
        'criteria_data': screening.criteria_data,
        'results_data': screening.results_data,
        'created_at': screening.created_at.isoformat() + 'Z'
    }})

@admin_bp.route('/admin/api/dashboard-data')
def admin_dashboard_data():
    """Get admin dashboard statistics"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    screenings = StockScreening.query.order_by(StockScreening.created_at.desc()).all()
    return jsonify({
        'success': True,
        'data': {
            'stats': {
                'total_users': len(MOCK_USERS),
                'pro_users': len([u for u in MOCK_USERS if u['subscription_tier'] == 'pro']),
                'medium_users': len([u for u in MOCK_USERS if u['subscription_tier'] == 'medium']),
                'free_users': len([u for u in MOCK_USERS if u['subscription_tier'] == 'free']),
                'total_screenings': len(screenings)
            },
            'screenings': [
                {
                    'id': s.id,
                    'name': s.name,
                    'results_count': len(s.results_data.get('stocks', [])),
                    'created_at': s.created_at.isoformat() + 'Z'
                } for s in screenings
            ]
        }
    })

@admin_bp.route('/admin/api/users')
def get_all_users():
    """Get all users for admin management"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'users': MOCK_USERS
    })

@admin_bp.route('/admin/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update user information"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    
    # Find and update user in mock data
    for user in MOCK_USERS:
        if user['id'] == user_id:
            user.update({
                'email': data.get('email', user['email']),
                'full_name': data.get('full_name', user['full_name']),
                'subscription_tier': data.get('subscription_tier', user['subscription_tier']),
                'is_admin': data.get('is_admin', user['is_admin'])
            })
            return jsonify({'success': True, 'message': 'User updated successfully'})
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/admin/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global MOCK_USERS
    MOCK_USERS = [u for u in MOCK_USERS if u['id'] != user_id]
    
    return jsonify({'success': True, 'message': 'User deleted successfully'})

@admin_bp.route('/admin/api/users/<user_id>/subscription', methods=['PUT'])
def update_user_subscription(user_id):
    """Update user subscription tier"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_tier = data.get('subscription_tier')
    
    # Find and update user subscription
    for user in MOCK_USERS:
        if user['id'] == user_id:
            user['subscription_tier'] = new_tier
            return jsonify({'success': True, 'message': f'Subscription updated to {new_tier}'})
    
    return jsonify({'error': 'User not found'}), 404

@admin_bp.route('/admin/api/subscription-requests')
def get_subscription_requests():
    """Get all pending subscription requests"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    return jsonify({
        'success': True,
        'requests': MOCK_SUBSCRIPTION_REQUESTS
    })

@admin_bp.route('/admin/api/subscription-requests/<request_id>/<action>', methods=['POST'])
def handle_subscription_request(request_id, action):
    """Approve or reject subscription request"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global MOCK_SUBSCRIPTION_REQUESTS
    
    # Find the request
    request_obj = None
    for req in MOCK_SUBSCRIPTION_REQUESTS:
        if req['id'] == request_id:
            request_obj = req
            break
    
    if not request_obj:
        return jsonify({'error': 'Request not found'}), 404
    
    if action == 'approve':
        # Update user subscription
        for user in MOCK_USERS:
            if user['id'] == request_obj['user_id']:
                user['subscription_tier'] = request_obj['requested_tier']
                break
        
        # Remove request
        MOCK_SUBSCRIPTION_REQUESTS = [r for r in MOCK_SUBSCRIPTION_REQUESTS if r['id'] != request_id]
        
        return jsonify({
            'success': True, 
            'message': f"Subscription upgraded to {request_obj['requested_tier']}"
        })
    
    elif action == 'reject':
        # Remove request
        MOCK_SUBSCRIPTION_REQUESTS = [r for r in MOCK_SUBSCRIPTION_REQUESTS if r['id'] != request_id]
        
        return jsonify({
            'success': True,
            'message': 'Subscription request rejected'
        })
    
    return jsonify({'error': 'Invalid action'}), 400

@admin_bp.route('/admin/api/bulk-upgrade', methods=['POST'])
def bulk_upgrade_users():
    """Bulk upgrade users from one tier to another"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    from_tier = data.get('from_tier')
    to_tier = data.get('to_tier')
    
    updated_count = 0
    for user in MOCK_USERS:
        if user['subscription_tier'] == from_tier and not user.get('is_admin', False):
            user['subscription_tier'] = to_tier
            updated_count += 1
    
    return jsonify({
        'success': True,
        'message': f'Upgraded {updated_count} users from {from_tier} to {to_tier}',
        'updated_count': updated_count
    })


# Get all stocks or a single stock by symbol
@admin_bp.route('/admin/api/stocks', methods=['GET'])
def get_all_or_single_stock():
    """Get all stocks for management, or a single stock if symbol is provided"""
    symbol = request.args.get('symbol')
    if symbol:
        stock = next((s for s in MOCK_STOCKS if s['symbol'].upper() == symbol.upper()), None)
        if stock:
            # Add mock price history, bullish reasons, and screening info for demo
            stock = dict(stock)  # Copy to avoid mutating MOCK_STOCKS
            stock['priceHistory'] = stock.get('priceHistory', [170, 172, 175, 178, 180.5])
            stock['priceHistoryDates'] = stock.get('priceHistoryDates', [
                "2025-09-20", "2025-09-21", "2025-09-22", "2025-09-23", "2025-09-24"
            ])
            stock['bullishReasons'] = stock.get('bullishReasons', [
                {"reason": "Strong earnings report", "impact": "+5%"},
                {"reason": "Positive industry trend", "impact": "+3%"},
                {"reason": "Analyst upgrade", "impact": "+2%"}
            ])
            stock['screening'] = stock.get('screening', {
                "criteria": "High volume, tech sector",
                "result": "Meets all criteria"
            })
            return jsonify({'success': True, 'stock': stock})
        else:
            return jsonify({'success': False, 'error': 'Stock not found'}), 404
    return jsonify({
        'success': True,
        'stocks': MOCK_STOCKS
    })

@admin_bp.route('/admin/api/stocks/by-industry', methods=['GET'])
def get_stocks_by_industry():
    """Get stocks organized by industry"""
    industry_groups = {}
    
    for stock in MOCK_STOCKS:
        industry_type = stock.get('industry_type', 'Other')
        industry_code = stock.get('industry_code', 'N/A')
        sector = stock.get('sector', 'Other')
        
        # Group by sector first, then by industry type
        if sector not in industry_groups:
            industry_groups[sector] = {}
        
        if industry_type not in industry_groups[sector]:
            industry_groups[sector][industry_type] = {
                'industry_code': industry_code,
                'stocks': []
            }
        
        industry_groups[sector][industry_type]['stocks'].append(stock)
    
    return jsonify({
        'success': True,
        'industries': industry_groups,
        'total_stocks': len(MOCK_STOCKS)
    })


@admin_bp.route('/admin/api/stocks', methods=['POST'])
def add_stock():
    """Add a new stock to a watchlist (Entry Zone or Breakout)"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401

    data = request.get_json()
    symbol = data.get('symbol', '').upper()
    name = data.get('name', '')
    sector = data.get('sector', '')
    price = float(data.get('price', 0))
    change_percent = float(data.get('change_percent', 0))
    watchlist_type = data.get('watchlist_type', 'entry')  # 'entry' or 'breakout'

    # Find or create the admin's watchlist for the given type

    admin_user = User.query.filter_by(email='admin@tradinggrow.com').first()
    if not admin_user:
        # Create admin user if missing
        try:
            admin_user = User(email='admin@tradinggrow.com', full_name='Admin User', is_admin=True)
            db.session.add(admin_user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create admin user: {str(e)}'}), 500

    watchlist = Watchlist.query.filter_by(user_id=admin_user.id, watchlist_type=watchlist_type).first()
    if not watchlist:
        try:
            watchlist = Watchlist(name=f"Admin {watchlist_type.title()} Stocks", user_id=admin_user.id, watchlist_type=watchlist_type)
            db.session.add(watchlist)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': f'Failed to create watchlist: {str(e)}'}), 500

    # Add the stock to the watchlist
    stock_data = {
        'symbol': symbol,
        'name': name,
        'sector': sector,
        'price': price,
        'change_percent': change_percent
    }
    try:
        watchlist.add_stock(stock_data)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to add stock: {str(e)}'}), 500

    return jsonify({
        'success': True,
        'message': f'Stock added to {watchlist_type} watchlist',
        'stock': stock_data
    })

@admin_bp.route('/admin/api/stocks/<stock_id>', methods=['DELETE'])
def delete_stock(stock_id):
    """Delete a stock"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    global MOCK_STOCKS
    MOCK_STOCKS = [s for s in MOCK_STOCKS if s['id'] != stock_id]
    
    return jsonify({
        'success': True,
        'message': 'Stock removed successfully'
    })

@admin_bp.route('/admin/api/stocks/<stock_id>/price', methods=['PUT'])
def update_stock_price(stock_id):
    """Update stock price"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    new_price = float(data.get('price', 0))
    
    for stock in MOCK_STOCKS:
        if stock['id'] == stock_id:
            old_price = stock['price']
            stock['price'] = new_price
            # Calculate change percentage
            if old_price > 0:
                stock['change_percent'] = ((new_price - old_price) / old_price) * 100
            return jsonify({'success': True, 'message': 'Stock price updated'})
    
    return jsonify({'error': 'Stock not found'}), 404

@admin_bp.route('/admin/api/stocks/bulk-upload', methods=['POST'])
def bulk_upload_stocks():
    """Bulk upload stocks from CSV file"""
    if not require_admin_session():
        return jsonify({'error': 'Unauthorized'}), 401
    
    if 'csvFile' not in request.files:
        return jsonify({'error': 'No CSV file provided'}), 400
    
    file = request.files['csvFile']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename or not file.filename.endswith('.csv'):
        return jsonify({'error': 'File must be a CSV file'}), 400
    
    global MOCK_STOCKS, MOCK_SCREENINGS
    try:
        # Read CSV file content
        stream = io.StringIO(file.stream.read().decode("UTF8"), newline=None)
        csv_reader = csv.DictReader(stream)
        processed_count = 0
        error_count = 0
        errors = []
        # Clear all existing stocks before adding new ones from CSV
        MOCK_STOCKS.clear()
        new_stocks = []
        entry_stocks = []
        breakout_stocks = []
        for row_num, row in enumerate(csv_reader, start=2):  # Start from 2 to account for header
            try:
                # Validate required fields
                required_fields = ['symbol', 'industry', 'market_cap', 'market_cap_formatted', 'latest_volume', 'mrs_current', 'weekly_growth', 'total_stocks', 'total_market_cap_formatted', 'price_vs_sma_pct', 'watchlist_type']
                missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                if missing_fields:
                    error_count += 1
                    errors.append(f"Row {row_num}: Missing required fields: {', '.join(missing_fields)}")
                    continue
                # Process the stock data
                stock_data = {
                    'id': str(len(MOCK_STOCKS) + processed_count + 1),
                    'symbol': row['symbol'].strip().upper(),
                    'industry': row['industry'].strip(),
                    'market_cap': float(row['market_cap']),
                    'market_cap_formatted': row['market_cap_formatted'].strip(),
                    'latest_volume': int(row['latest_volume']),
                    'mrs_current': float(row['mrs_current']),
                    'weekly_growth': float(row['weekly_growth']),
                    'total_stocks': int(row['total_stocks']),
                    'total_market_cap_formatted': row['total_market_cap_formatted'].strip(),
                    'price_vs_sma_pct': float(row['price_vs_sma_pct']),
                    'watchlist_type': row['watchlist_type'].strip().lower()
                }
                # Check for duplicate symbols
                existing_stock = next((s for s in MOCK_STOCKS if s['symbol'] == stock_data['symbol']), None)
                if existing_stock:
                    existing_stock.update(stock_data)
                    existing_stock['id'] = existing_stock['id']
                else:
                    MOCK_STOCKS.append(stock_data)
                    new_stocks.append(stock_data)
                # Split by watchlist_type
                if stock_data['watchlist_type'] == 'entry':
                    entry_stocks.append(stock_data)
                elif stock_data['watchlist_type'] == 'breakout':
                    breakout_stocks.append(stock_data)
                processed_count += 1
            except ValueError as e:
                error_count += 1
                errors.append(f"Row {row_num}: Invalid data format - {str(e)}")
            except Exception as e:
                error_count += 1
                errors.append(f"Row {row_num}: Error processing row - {str(e)}")
        
        # Update admin's entry zone and breakout watchlists
        admin_user = User.query.filter_by(email='admin@tradinggrow.com').first()
        if admin_user:
            # Entry Zone
            entry_watchlist = Watchlist.query.filter_by(user_id=admin_user.id, watchlist_type='entry').first()
            if not entry_watchlist:
                entry_watchlist = Watchlist(name="Admin Entry Zone Stocks", user_id=admin_user.id, watchlist_type='entry')
                db.session.add(entry_watchlist)
            entry_watchlist.stocks = entry_stocks
            # Breakout
            breakout_watchlist = Watchlist.query.filter_by(user_id=admin_user.id, watchlist_type='breakout').first()
            if not breakout_watchlist:
                breakout_watchlist = Watchlist(name="Admin Breakout Stocks", user_id=admin_user.id, watchlist_type='breakout')
                db.session.add(breakout_watchlist)
            breakout_watchlist.stocks = breakout_stocks
            db.session.commit()
        # Update mock screening results (if any)
        for screening in MOCK_SCREENINGS:
            screening['results_data'] = {'entry': entry_stocks, 'breakout': breakout_stocks}
        # Update mock screening results (if any)
        for screening in MOCK_SCREENINGS:
            screening['results_data'] = {'stocks': new_stocks}
        # Prepare response
        response_data = {
            'success': True,
            'message': f'CSV processed successfully! {processed_count} stocks processed.',
            'processed': processed_count,
            'errors': error_count,
            'total_stocks': len(MOCK_STOCKS)
        }
        if errors:
            response_data['error_details'] = errors[:10]  # Limit to first 10 errors
        return jsonify(response_data)
        
    except Exception as e:
        return jsonify({
            'error': f'Failed to process CSV file: {str(e)}'
        }), 500