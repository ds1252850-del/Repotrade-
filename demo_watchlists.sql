-- SQL to create and populate the watchlists table with entry and breakout stocks for demo
DROP TABLE IF EXISTS watchlists;
CREATE TABLE watchlists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    user_id TEXT NOT NULL,
    watchlist_type TEXT DEFAULT 'normal',
    stocks_json TEXT DEFAULT '[]',
    created_at TEXT,
    updated_at TEXT
);

-- Insert demo entry zone watchlist
INSERT INTO watchlists (id, name, user_id, watchlist_type, stocks_json, created_at, updated_at) VALUES (
    '1', 'Admin Entry Zone Stocks', 'admin', 'entry',
    '[{"symbol": "AAPL", "industry": "Technology", "latest_volume": 100000000, "total_market_cap_formatted": "$2.5T"}, {"symbol": "TSLA", "industry": "Automotive", "latest_volume": 50000000, "total_market_cap_formatted": "$800B"}]',
    '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z'
);

-- Insert demo breakout watchlist
INSERT INTO watchlists (id, name, user_id, watchlist_type, stocks_json, created_at, updated_at) VALUES (
    '2', 'Admin Breakout Stocks', 'admin', 'breakout',
    '[{"symbol": "MSFT", "industry": "Technology", "latest_volume": 75000000, "total_market_cap_formatted": "$2.3T"}, {"symbol": "GOOGL", "industry": "Technology", "latest_volume": 30000000, "total_market_cap_formatted": "$1.8T"}]',
    '2024-01-01T00:00:00Z', '2024-01-01T00:00:00Z'
);
