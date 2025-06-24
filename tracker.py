import json
import os

DATA_FILE = "data.json"

# Ensure data.json exists
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

def get_entries():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def add_entry(entry_type, category, amount):
    entry = {
        "type": entry_type,
        "category": category,
        "amount": amount
    }
    entries = get_entries()
    entries.append(entry)
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def calculate_summary():
    entries = get_entries()
    income = sum(float(e.get('amount', 0)) for e in entries if e.get('type') == 'Income')
    expense = sum(float(e.get('amount', 0)) for e in entries if e.get('type') == 'Expense')
    balance = income - expense
    return income, expense, balance
