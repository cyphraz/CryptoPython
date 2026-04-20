CryptoPy is a small client-server cryptocurrency investment simulator built with Python, Tkinter,
sockets, and SQLite. It lets a user create an account, log in, view available crypto assets,
deposit or withdraw funds, and buy or sell assets while tracking a cash balance and portfolio.

Features
--------
* Create a local account with an initial cash balance
* Log in and manage your portfolio
* View the current list of supported crypto assets
* Deposit and withdraw funds
* Buy and sell assets
* Store accounts, portfolio data, and transaction history in a local SQLite database

How It Works
------------
The application is split into three Python files:

* server.py   - starts the SQLite database and launches a socket server that handles all
                client requests (account creation, login, balance updates, asset trading)
* client.py   - provides the Tkinter desktop GUI; sends semicolon-delimited requests to
                the server and displays responses
* database.py - handles database initialisation and provides a shared connection helper

The database file is created automatically as crypto_investment.db in the project root.

Supported Assets
----------------
The following cryptocurrencies are available by default:

  Bitcoin        $100,475
  Ethereum       $3,785
  Tether         $1
  Solana         $229
  Binance Coin   $695
  Litecoin       $115

Requirements
------------
* Python 3.10 or newer

No third-party packages are required. The project uses only the Python standard library
(socket, sqlite3, tkinter).

Run the App
-----------
Start the server from the project root:

    python server.py

Then, in a separate terminal, launch the client:

    python client.py

The server must be running before the client is opened. The server listens on
127.0.0.1:4000 by default.

Project Structure
-----------------
  server.py    - socket server and request handlers (User, Assets, Portfolio classes)
  client.py    - Tkinter desktop client (Client and Menu classes)
  database.py  - SQLite setup and shared connection logic

Notes
-----
* Asset prices are fixed at startup from the values defined in database.py and are not
  fetched live from an external API.
* User passwords are stored in plain text in the local SQLite database. This project is
  intended as a local demo and learning tool, not a production trading platform.
* Only one client connection is handled at a time; the server does not use threading.
* Accounts, balances, and portfolio data persist across sessions in crypto_investment.db.
