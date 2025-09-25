# Script to create sample Entry Zone and Breakout watchlists with stocks
from app import db
from models import Watchlist
from datetime import datetime

# Sample stocks
entry_zone_stocks = [
    {"symbol": "AAPL", "name": "Apple Inc.", "sector": "Technology", "price": 175.50},
    {"symbol": "TSLA", "name": "Tesla Inc.", "sector": "Consumer", "price": 245.80}
]
breakout_stocks = [
    {"symbol": "GOOGL", "name": "Alphabet Inc.", "sector": "Technology", "price": 2850.25},
    {"symbol": "JPM", "name": "JPMorgan Chase", "sector": "Financials", "price": 145.30}
]

# Create Entry Zone Watchlist
entry_watchlist = Watchlist(
    name="Entry Zone Example",
    user_id="1",  # Use a valid user_id from your DB
    watchlist_type="entry"
)
entry_watchlist.stocks = entry_zone_stocks
entry_watchlist.created_at = datetime.utcnow()
entry_watchlist.updated_at = datetime.utcnow()
entry_watchlist.save()

# Create Breakout Watchlist
breakout_watchlist = Watchlist(
    name="Breakout Example",
    user_id="1",  # Use a valid user_id from your DB
    watchlist_type="breakout"
)
breakout_watchlist.stocks = breakout_stocks
breakout_watchlist.created_at = datetime.utcnow()
breakout_watchlist.updated_at = datetime.utcnow()
breakout_watchlist.save()

print("Sample Entry Zone and Breakout watchlists created.")
