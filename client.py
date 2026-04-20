from socket import *
from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox

HOST = "127.0.0.1"  # Server's local IP address
PORT = 4000          # Port number the server listens on
ADDRESS = (HOST, PORT)  # Combine host and port into a tuple

class Client:
    def __init__(self):
        """Initializes client and connects to server."""
        self.socket = None
        self.logged_in_username = None
        self.connect_to_server()

    def connect_to_server(self):
        """Connects to the server, handles connection errors."""
        try:
            self.socket = socket(AF_INET, SOCK_STREAM)
            self.socket.connect(ADDRESS)
        except:
            self.socket = None

    def send_request(self, request):
        """Sends a request to the server and handles errors."""
        print(f"Sending request: {request}")  # Debugging line
        if not self.socket:
            self.connect_to_server()
            if not self.socket:
                return "Connection error."
        try:
            self.socket.send(request.encode())
            return self.socket.recv(1024).decode()
        except:
            self.socket = None
            return "Server error."

    def close_connection(self):
        """Closes the socket connection."""
        if self.socket:
            self.socket.close()

class Menu:
    def __init__(self):
        """Initializes the main menu and connects to the server."""
        self.client = Client()
        if not self.client.socket:
            messagebox.showwarning("Server", "Can't connect.")
        
        # Set up main window properties
        self.root = Tk()
        self.root.geometry("1366x720+0+0")
        self.root.title("Crypto App")
        self.root.config(bg="#1e1e2e")  # Background color

        # Label to display responses
        self.response_label = Label(self.root, text="", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 16))
        self.response_label.pack()

        # Frame setup for different menu screens
        self.main_menu_frame = Frame(self.root, bg="#1e1e2e")
        self.create_account_frame = Frame(self.root, bg="#1e1e2e")
        self.login_frame = Frame(self.root, bg="#1e1e2e")
        self.logged_in_frame = Frame(self.root, bg="#1e1e2e")

        # Call the menu setup functions
        self.main_menu()
        self.create_account_menu()
        self.login_menu()
        self.logged_in_menu()

        # Show the main menu frame by default
        self.show_frame(self.main_menu_frame)
        self.root.mainloop()

    def main_menu(self):
        """Creates the main menu with options like 'Create Account', 'Login', and 'Exit'."""
        Button(self.main_menu_frame, text="Create Account", command=lambda: self.show_frame(self.create_account_frame), bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.main_menu_frame, text="Login", command=lambda: self.show_frame(self.login_frame), bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.main_menu_frame, text="Exit", command=self.exit_application, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)

    def create_account_menu(self):
        """Handles account creation input fields and buttons."""
        Label(self.create_account_frame, text="Username", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 14)).pack(pady=5)
        self.username_entry = Entry(self.create_account_frame, font=("Comic Sans MS", 14))
        self.username_entry.pack(pady=5)

        Label(self.create_account_frame, text="Password", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 14)).pack(pady=5)
        self.password_entry = Entry(self.create_account_frame, show="*", font=("Comic Sans MS", 14))
        self.password_entry.pack(pady=5)

        Label(self.create_account_frame, text="Initial Balance", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 14)).pack(pady=5)
        self.balance_entry = Entry(self.create_account_frame, font=("Comic Sans MS", 14))
        self.balance_entry.pack(pady=5)

        Button(self.create_account_frame, text="Create", command=self.create_account, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.create_account_frame, text="Back", command=lambda: self.show_frame(self.main_menu_frame), bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=5)

    def login_menu(self):
        """Handles login input fields and buttons."""
        Label(self.login_frame, text="Username", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 14)).pack(pady=5)
        self.login_username = Entry(self.login_frame, font=("Comic Sans MS", 14))
        self.login_username.pack(pady=5)

        Label(self.login_frame, text="Password", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 14)).pack(pady=5)
        self.login_password = Entry(self.login_frame, show="*", font=("Comic Sans MS", 14))
        self.login_password.pack(pady=5)

        Button(self.login_frame, text="Login", command=self.login, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.login_frame, text="Back", command=lambda: self.show_frame(self.main_menu_frame), bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=5)

    def logged_in_menu(self):
        """Displays options for logged-in users like 'View Portfolio', 'Deposit', etc."""
        self.balance_label = Label(self.logged_in_frame, text="", bg="#1e1e2e", fg="#ffffff", font=("Comic Sans MS", 16))
        self.balance_label.pack(pady=10)
        
        Button(self.logged_in_frame, text="View Assets", command=self.view_assets, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.logged_in_frame, text="View Portfolio", command=self.view_portfolio, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.logged_in_frame, text="Deposit", command=self.deposit, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.logged_in_frame, text="Withdraw", command=self.withdraw, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.logged_in_frame, text="Buy Assets", command=self.buy_assets, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.logged_in_frame, text="Sell Assets", command=self.sell_assets, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)
        Button(self.logged_in_frame, text="Logout", command=self.logout, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)

    def show_frame(self, frame):
        """Switches between different menu frames."""
        for f in [self.main_menu_frame, self.create_account_frame, self.login_frame, self.logged_in_frame]:
            f.pack_forget()
        frame.pack(fill="both", expand=True)

    def create_account(self):
        """Handles account creation logic."""
        username = self.username_entry.get()
        password = self.password_entry.get()
        balance = self.balance_entry.get()

        if not balance.isdigit():
            messagebox.showerror("Error", "Balance must be numeric.")
            return

        response = self.client.send_request(f"create_account;{username};{password};{balance}")
        messagebox.showinfo("Server", response)

    def login(self):
        """Handles user login logic."""
        username = self.login_username.get()
        password = self.login_password.get()
        response = self.client.send_request(f"login;{username};{password}")
        messagebox.showinfo("Server", response)

        if response == "Login successful.":
            self.client.logged_in_username = username
            self.update_balance()
            self.show_frame(self.logged_in_frame)

    def update_balance(self):
        """Updates balance display for logged-in user."""
        if not self.client.logged_in_username:
            messagebox.showerror("Error", "User not logged in.")
            return

        response = self.client.send_request(f"view_balance;{self.client.logged_in_username}")
        if response == "Server error.":
            messagebox.showerror("Error", "There was an issue fetching the balance. Please try again.")
        else:
            self.balance_label.config(text=f"Balance: {response}")

    def view_assets(self):
        """Displays assets."""
        response = self.client.send_request("view_assets")
        self.response_label.config(text=response)

    def view_portfolio(self):
        """Displays portfolio for logged-in user."""
        if not self.client.logged_in_username:
            messagebox.showerror("Error", "Please login first.")
            return
        response = self.client.send_request(f"view_portfolio;{self.client.logged_in_username}")
        self.response_label.config(text=response)

    def deposit(self):
        """Handles deposit logic with a window input."""
        if not self.client.logged_in_username:
            messagebox.showerror("Error", "Please login first.")
            return

        self.deposit_window = Toplevel(self.root)
        self.deposit_window.geometry("300x150")
        self.deposit_window.title("Deposit")

        Label(self.deposit_window, text="Enter amount to deposit:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.deposit_amount = Entry(self.deposit_window, font=("Comic Sans MS", 14))
        self.deposit_amount.pack(pady=10)

        Button(self.deposit_window, text="Submit", command=self.submit_deposit, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)

    def submit_deposit(self):
        """Handles deposit submission."""
        amount = self.deposit_amount.get()
        if amount.isdigit():
            response = self.client.send_request(f"deposit;{self.client.logged_in_username};{amount}")
            self.deposit_window.destroy()
            self.update_balance()
            messagebox.showinfo("Deposit", response)
        else:
            messagebox.showerror("Error", "Amount must be numeric.")

    def withdraw(self):
        """Handles withdraw logic with a window input."""
        if not self.client.logged_in_username:
            messagebox.showerror("Error", "Please login first.")
            return

        self.withdraw_window = Toplevel(self.root)
        self.withdraw_window.geometry("300x150")
        self.withdraw_window.title("Withdraw")

        Label(self.withdraw_window, text="Enter amount to withdraw:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.withdraw_amount = Entry(self.withdraw_window, font=("Comic Sans MS", 14))
        self.withdraw_amount.pack(pady=10)

        Button(self.withdraw_window, text="Submit", command=self.submit_withdraw, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)

    def submit_withdraw(self):
        """Handles withdrawal submission."""
        amount = self.withdraw_amount.get()
        if amount.isdigit():
            response = self.client.send_request(f"withdraw;{self.client.logged_in_username};{amount}")
            self.withdraw_window.destroy()
            self.update_balance()
            messagebox.showinfo("Withdraw", response)
        else:
            messagebox.showerror("Error", "Amount must be numeric.")

    def buy_assets(self):
        """Handles buying assets logic with window input."""
        if not self.client.logged_in_username:
            messagebox.showerror("Error", "Please login first.")
            return

        self.buy_window = Toplevel(self.root)
        self.buy_window.geometry("300x200")
        self.buy_window.title("Buy Assets")

        Label(self.buy_window, text="Enter asset name:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.asset_name_buy = Entry(self.buy_window, font=("Comic Sans MS", 14))
        self.asset_name_buy.pack(pady=10)

        Label(self.buy_window, text="Enter amount:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.amount_buy = Entry(self.buy_window, font=("Comic Sans MS", 14))
        self.amount_buy.pack(pady=10)

        Button(self.buy_window, text="Submit", command=self.submit_buy_assets, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)

    def submit_buy_assets(self):
        """Handles asset purchase."""
        asset_name = self.asset_name_buy.get()
        amount = self.amount_buy.get()
        if asset_name and amount.isdigit():
            response = self.client.send_request(f"buy_assets;{self.client.logged_in_username};{asset_name};{amount}")
            self.buy_window.destroy()
            messagebox.showinfo("Buy", response)
        else:
            messagebox.showerror("Error", "Invalid input.")

    def sell_assets(self):
        """Handles selling assets logic with window input."""
        if not self.client.logged_in_username:
            messagebox.showerror("Error", "Please login first.")
            return

        self.sell_window = Toplevel(self.root)
        self.sell_window.geometry("300x200")
        self.sell_window.title("Sell Assets")

        Label(self.sell_window, text="Enter asset name:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.asset_name_sell = Entry(self.sell_window, font=("Comic Sans MS", 14))
        self.asset_name_sell.pack(pady=10)

        Label(self.sell_window, text="Enter amount:", font=("Comic Sans MS", 14)).pack(pady=10)
        self.amount_sell = Entry(self.sell_window, font=("Comic Sans MS", 14))
        self.amount_sell.pack(pady=10)

        Button(self.sell_window, text="Submit", command=self.submit_sell_assets, bg="#6305dc", fg="#ffffff", relief="flat", font=("Comic Sans MS", 14)).pack(pady=10)

    def submit_sell_assets(self):
        """Handles asset sale."""
        asset_name = self.asset_name_sell.get()
        amount = self.amount_sell.get()
        if asset_name and amount.isdigit():
            response = self.client.send_request(f"sell_assets;{self.client.logged_in_username};{asset_name};{amount}")
            self.sell_window.destroy()
            messagebox.showinfo("Sell", response)
        else:
            messagebox.showerror("Error", "Invalid input.")

    def logout(self):
        """Handles user logout."""
        self.client.logged_in_username = None
        self.show_frame(self.main_menu_frame)

    def exit_application(self):
        """Closes the application."""
        if self.client.socket:
            self.client.socket.close()
        self.root.quit()

if __name__ == "__main__":
    Menu()
