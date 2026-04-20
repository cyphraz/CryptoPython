from socket import *  # Importing the socket module for communication
import sqlite3
from database import initialise_database, get_connection

HOST = "127.0.0.1"  # Local address
PORT = 4000  # Port number
ADDRESS = (HOST, PORT)

class Server:
    def __init__(self):
        # Setting up the server socket to listen for client connections
        self.server_socket = socket(AF_INET, SOCK_STREAM)  # Initialize the socket
        self.server_socket.bind(ADDRESS)  # Binding to the specified address and port
        self.server_socket.listen(5)  # Listen for up to 5 connections
        print(f"Server started on {HOST}:{PORT}")  # Confirm server start

    def handle_client(self, client_socket, client_addr):
        # Handling client requests
        print(f"Handling client: {client_addr}")
        try:
            while True:
                # Receive the request data from the client
                received_data = client_socket.recv(1024).decode()
                if not received_data:
                    print(f"connection from {client_addr} disconnected")
                    break  # No data received means client disconnected
                server_response = self.process_request(received_data)
                client_socket.send(server_response.encode())  # Send response to client
        except Exception as error:
            print(f"Error handling client: {error}")
        finally:
            client_socket.close()  # Closing the client connection

    def create_server(self):
        # Server waiting for connections
        print("Server waiting for connections...")
        while True:
            client_socket, client_addr = self.server_socket.accept()  # Accept new connections
            print(f"Client connected: {client_addr}")
            self.handle_client(client_socket, client_addr)  # Handle the client connection directly

    def process_request(self, request):
        # Process the client request, splitting it into parts
        parts = request.split(";")
        action = parts[0]  # The action is the first part
        try:
            if action == "create_account":
                return User.create_account(parts[1], parts[2], float(parts[3]))  # Create account
            elif action == "login":
                return User.login(parts[1], parts[2])  # Handle login
            elif action == "view_assets":
                return Assets.view_assets()  # Show available assets
            elif action == "deposit" or action == "withdraw":
                return User.update_balance(parts[1], float(parts[2]))  # Update balance
            elif action == "view_portfolio":
                return Portfolio.view_portfolio(parts[1])  # View portfolio
            elif action == "view_balance":
                return User.view_balance(parts[1])  # View balance
            elif action == "buy_assets" or action == "sell_assets":
                return Portfolio.manage_assets(parts[1], parts[2], int(parts[3]), action)  # Manage assets
            else:
                return "Error: Unknown request."
        except (IndexError, ValueError) as error:
            return "Error: Malformed request."

class User:
    def create_account(username, password, balance):
        # Create a new account in the database
        with get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute("INSERT INTO accounts (username, password, balance) VALUES (?, ?, ?)", (username, password, balance))
                conn.commit()
                return "Account created successfully."
            except sqlite3.IntegrityError:
                return "Error: Username already exists."

    def login(username, password):
        # Check the credentials for login
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()
            return "Login successful." if result else "Error: Invalid username or password."

    def update_balance(username, amount):
        # Update balance when a user deposits or withdraws
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                new_balance = result[0] + amount
                if new_balance < 0:
                    return "Error: Insufficient funds."
                cursor.execute("UPDATE accounts SET balance = ? WHERE username = ?", (new_balance, username))
                conn.commit()
                return f"Balance updated: ${new_balance:.2f}"
            return "Error: Account not found."

    def view_balance(username):
        # Retrieve the balance of the user
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                return f"${result[0]:.2f}"
            return "Error: Account not found."

class Assets:
    def view_assets():
        # View available assets
        try:
            with get_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT asset_name, price FROM assets")
                assets = cursor.fetchall()
                if not assets:
                    return "No assets available."
                return "\n".join([f"{name}: ${price}" for name, price in assets])
        except Exception as error:
            return f"Error fetching assets: {error}"

class Portfolio:
    def view_portfolio(username):
        # View the user's portfolio (assets owned by user)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT asset_name, quantity FROM portfolio WHERE username = ?", (username,))
            assets = cursor.fetchall()
            if assets:
                return "\n".join([f"{name}: {quantity}" for name, quantity in assets])
            return "Portfolio is empty."

    def manage_assets(username, asset_name, quantity, action):
        # Buying or selling assets (deduct from balance and update portfolio)
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM assets WHERE asset_name = ?", (asset_name,))
            price = cursor.fetchone()
            if not price:
                return "Error: Asset not found."
            total_cost = price[0] * quantity
            cursor.execute("SELECT balance FROM accounts WHERE username = ?", (username,))
            account_balance = cursor.fetchone()
            if account_balance and account_balance[0] >= total_cost:
                new_balance = account_balance[0] - total_cost if action == "buy_assets" else account_balance[0] + total_cost
                cursor.execute("UPDATE accounts SET balance = ? WHERE username = ?", (new_balance, username))
                if action == "buy_assets":
                    cursor.execute("SELECT quantity FROM portfolio WHERE username = ? AND asset_name = ?", (username, asset_name))
                    portfolio = cursor.fetchone()
                    if portfolio:
                        cursor.execute("UPDATE portfolio SET quantity = quantity + ? WHERE username = ? AND asset_name = ?", (quantity, username, asset_name))
                    else:
                        cursor.execute("INSERT INTO portfolio (username, asset_name, quantity) VALUES (?, ?, ?)", (username, asset_name, quantity))
                else:
                    cursor.execute("SELECT quantity FROM portfolio WHERE username = ? AND asset_name = ?", (username, asset_name))
                    portfolio = cursor.fetchone()
                    if portfolio and portfolio[0] >= quantity:
                        new_quantity = portfolio[0] - quantity
                        if new_quantity == 0:
                            cursor.execute("DELETE FROM portfolio WHERE username = ? AND asset_name = ?", (username, asset_name))
                        else:
                            cursor.execute("UPDATE portfolio SET quantity = ? WHERE username = ? AND asset_name = ?", (new_quantity, username, asset_name))
                    else:
                        return "Error: Insufficient quantity."
                conn.commit()
                return f"{action.replace('_', ' ').title()} completed. New balance: ${new_balance:.2f}"
            return "Error: Insufficient funds."

# Initializing the database
initialise_database()  # Ensure database is set up

# Starting the server
if __name__ == "__main__":
    server = Server()
    server.create_server()  # Start the server
