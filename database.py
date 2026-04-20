import sqlite3

def setup_db():
    try:
        conn = sqlite3.connect('crypto_investment.db')
        cursor = conn.cursor()
        
        # Accounts Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (username TEXT PRIMARY KEY, password TEXT, balance REAL)''')
        
        # Transactions Table
        cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, asset_name TEXT,
            type TEXT, quantity REAL, amount REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY(username) REFERENCES accounts(username))''')
        
        # Portfolio Table with unique constraint
        cursor.execute('''CREATE TABLE IF NOT EXISTS portfolio (
            username TEXT,
            asset_name TEXT,
            quantity INTEGER,
            PRIMARY KEY(username, asset_name),
            FOREIGN KEY(username) REFERENCES accounts(username))''')

        # Assets Table
        cursor.execute("CREATE TABLE IF NOT EXISTS assets (asset_name TEXT PRIMARY KEY, price REAL NOT NULL)")
        cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Bitcoin", 100475))
        cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Ethereum", 3785))
        cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Tether", 1))
        cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Solana", 229))
        cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Binance Coin", 695))
        cursor.execute("INSERT OR REPLACE INTO assets (asset_name, price) VALUES (?, ?)", ("Litecoin", 115))

        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        conn.rollback()
    except Exception as e:
        print(f"Unexpected error: {e}")
        conn.rollback()

def initialise_database():
    setup_db()

def get_connection():
    return sqlite3.connect('crypto_investment.db')
