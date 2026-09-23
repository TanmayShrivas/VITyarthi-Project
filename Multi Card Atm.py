import os
import json
import random
from datetime import datetime
 
DATA_FILE = "atm_cards.json"
HISTORY_LIMIT = 5
 
 
class Card:
    """Represents a single ATM card/account."""
 
    def __init__(self, card_number, holder_name, pin, balance=0.0, transactions=None):
        self.card_number = card_number
        self.holder_name = holder_name
        self.pin = pin
        self.balance = balance
        self.transactions = transactions if transactions is not None else []
 
    # ---------- Operations ----------
 
    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return
        self.balance += amount
        self.log_transaction(f"Deposited ₹{amount:.2f}")
        print(f"₹{amount:.2f} deposited. New balance: ₹{self.balance:.2f}")
 
    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return
        if amount > self.balance:
            print("Insufficient funds. Withdrawal denied.")
            self.log_transaction(f"Failed withdrawal of ₹{amount:.2f} (insufficient funds)")
            return
        self.balance -= amount
        self.log_transaction(f"Withdrew ₹{amount:.2f}")
        print(f"₹{amount:.2f} withdrawn. New balance: ₹{self.balance:.2f}")
 
    def change_pin(self, old_pin, new_pin):
        if old_pin != self.pin:
            print("Incorrect current PIN. PIN not changed.")
            return
        if len(new_pin) != 4 or not new_pin.isdigit():
            print("New PIN must be exactly 4 digits.")
            return
        self.pin = new_pin
        self.log_transaction("PIN changed")
        print("PIN changed successfully.")
 
    def verify_pin(self, entered_pin):
        return entered_pin == self.pin
 
    def log_transaction(self, description):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.transactions.append(f"[{timestamp}] {description}")
 
    def show_mini_statement(self):
        print(f"\n--- Mini Statement for card ending {self.card_number[-4:]} "
              f"(last {HISTORY_LIMIT}) ---")
        if not self.transactions:
            print("No transactions yet.")
        else:
            for entry in reversed(self.transactions[-HISTORY_LIMIT:]):
                print(entry)
        print("---------------------------------------------------\n")
 
    def masked_number(self):
        return "**** **** **** " + self.card_number[-4:]
 
    # ---------- Serialization ----------
 
    def to_dict(self):
        return {
            "card_number": self.card_number,
            "holder_name": self.holder_name,
            "pin": self.pin,
            "balance": self.balance,
            "transactions": self.transactions,
        }
 
    @staticmethod
    def from_dict(data):
        return Card(
            data["card_number"],
            data["holder_name"],
            data["pin"],
            data.get("balance", 0.0),
            data.get("transactions", []),
        )
 
 
class ATMSystem:
    """Manages a collection of cards: adding, deleting, saving, loading."""
 
    def __init__(self):
        self.cards = {}   # card_number -> Card object
        self.active_card = None
        self.load_data()
 
    # ---------- Card management ----------
 
    def generate_card_number(self):
        """Generate a unique 16-digit card number as a string."""
        while True:
            number = "".join(str(random.randint(0, 9)) for _ in range(16))
            if number not in self.cards:
                return number
 
    def add_card(self, holder_name, pin, opening_balance):
        card_number = self.generate_card_number()
        card = Card(card_number, holder_name, pin, opening_balance)
        card.log_transaction(f"Card created with opening balance ₹{opening_balance:.2f}")
        self.cards[card_number] = card
        print(f"\nCard created successfully!")
        print(f"Card Number : {card_number}")
        print(f"Holder Name : {holder_name}")
        print(f"PIN         : {pin}  (keep this safe!)")
        print(f"Balance     : ₹{opening_balance:.2f}\n")
        return card
 
    def delete_card(self, card_number):
        if card_number in self.cards:
            removed = self.cards.pop(card_number)
            print(f"Card ending {removed.card_number[-4:]} ({removed.holder_name}) deleted.")
            if self.active_card and self.active_card.card_number == card_number:
                self.active_card = None
        else:
            print("Card not found.")
 
    def list_cards(self):
        if not self.cards:
            print("\nNo cards found. Add a new card first.\n")
            return
        print("\n================= ALL CARDS =================")
        print(f"{'Card Number':<20}{'Holder':<20}{'Balance':<12}")
        print("-" * 52)
        for card in self.cards.values():
            print(f"{card.masked_number():<20}{card.holder_name:<20}₹{card.balance:<11.2f}")
        print("===============================================\n")
 
    def find_card_by_last4(self, last4_or_full):
        """Allow selecting a card by full number or just the last 4 digits."""
        query = last4_or_full.strip()
        if query in self.cards:
            return self.cards[query]
        matches = [c for c in self.cards.values() if c.card_number.endswith(query)]
        if len(matches) == 1:
            return matches[0]
        elif len(matches) > 1:
            print("Multiple cards match those digits. Please enter the full card number.")
            return None
        return None
 
    # ---------- File handling ----------
 
    def save_data(self):
        data = {number: card.to_dict() for number, card in self.cards.items()}
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=2)
        print("All card data saved.")
 
    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return
        try:
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
            for number, card_data in data.items():
                self.cards[number] = Card.from_dict(card_data)
        except (json.JSONDecodeError, KeyError):
            print("Warning: saved card data was corrupted and could not be loaded.")
 
 
# ---------------- Menu-driven interface ----------------
 
def get_amount(prompt):
    try:
        return float(input(prompt))
    except ValueError:
        print("Invalid amount entered.")
        return None
 
 
def print_main_menu():
    print("\n============ MULTI-CARD ATM SIMULATOR ============")
    print("1. Add New Card")
    print("2. View All Cards")
    print("3. Select / Login to a Card")
    print("4. Delete a Card")
    print("5. Save & Exit")
    print("====================================================")
 
 
def print_card_menu(card):
    print(f"\n--- Logged in: {card.holder_name} ({card.masked_number()}) ---")
    print("1. Check Balance")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Mini Statement")
    print("5. Change PIN")
    print("6. Switch Card")
    print("7. Logout")
    print("-------------------------------------------------")
 
 
def card_session(atm, card):
    """Handle all operations while logged into a specific card."""
    atm.active_card = card
    while True:
        print_card_menu(card)
        choice = input("Enter your choice (1-7): ").strip()
 
        if choice == "1":
            print(f"\nBalance for {card.masked_number()}: ₹{card.balance:.2f}\n")
 
        elif choice == "2":
            amount = get_amount("Enter amount to deposit: ₹")
            if amount is not None:
                card.deposit(amount)
 
        elif choice == "3":
            amount = get_amount("Enter amount to withdraw: ₹")
            if amount is not None:
                card.withdraw(amount)
 
        elif choice == "4":
            card.show_mini_statement()
 
        elif choice == "5":
            old_pin = input("Enter current PIN: ").strip()
            new_pin = input("Enter new 4-digit PIN: ").strip()
            card.change_pin(old_pin, new_pin)
 
        elif choice == "6":
            print("Switching card...")
            atm.active_card = None
            return "switch"
 
        elif choice == "7":
            print("Logging out...")
            atm.active_card = None
            return "logout"
 
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
 
 
def select_and_login(atm):
    atm.list_cards()
    if not atm.cards:
        return
    query = input("Enter full card number or last 4 digits to select: ").strip()
    card = atm.find_card_by_last4(query)
    if not card:
        print("Card not found.")
        return
 
    for attempt in range(3):
        pin = input(f"Enter PIN for card ending {card.card_number[-4:]}: ").strip()
        if card.verify_pin(pin):
            return card_session(atm, card)
        print(f"Incorrect PIN. {2 - attempt} attempt(s) remaining.")
    print("Too many incorrect attempts. Returning to main menu.")
 
 
def main():
    atm = ATMSystem()
    print("Welcome to the Multi-Card ATM Simulator!")
 
    while True:
        print_main_menu()
        choice = input("Enter your choice (1-5): ").strip()
 
        if choice == "1":
            holder_name = input("Enter cardholder name: ").strip()
            while True:
                pin = input("Set a 4-digit PIN: ").strip()
                if len(pin) == 4 and pin.isdigit():
                    break
                print("PIN must be exactly 4 digits.")
            opening_balance = get_amount("Enter opening balance: ₹")
            if opening_balance is None or opening_balance < 0:
                print("Invalid opening balance. Card creation cancelled.")
                continue
            atm.add_card(holder_name, pin, opening_balance)
 
        elif choice == "2":
            atm.list_cards()
 
        elif choice == "3":
            result = select_and_login(atm)
            if result == "switch":
                continue   # loop back, user can select another card
 
        elif choice == "4":
            atm.list_cards()
            if atm.cards:
                query = input("Enter full card number or last 4 digits to delete: ").strip()
                card = atm.find_card_by_last4(query)
                if card:
                    confirm = input(f"Are you sure you want to delete card "
                                     f"{card.masked_number()}? (y/n): ").strip().lower()
                    if confirm == "y":
                        atm.delete_card(card.card_number)
                else:
                    print("Card not found.")
 
        elif choice == "5":
            atm.save_data()
            print("Thank you for using the Multi-Card ATM Simulator. Goodbye!")
            break
 
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")
 
 
if __name__ == "__main__":
    main()
 
