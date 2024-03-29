import json
import os


def load_warehouse():
    if not os.path.exists("warehouse.json"):
        return {}
    with open("warehouse.json") as f:
        warehouse = json.load(f)
    return warehouse


def save_warehouse(warehouse):
    with open("warehouse.json", "w") as f:
        json.dump(warehouse, f)


def load_history():
    if not os.path.exists("history.json"):
        return []
    with open("history.json") as f:
        history = json.load(f)
    return history


def save_history(history):
    with open("history.json", "w") as f:
        json.dump(history, f)


def load_balance():
    if not os.path.exists("balance.json"):
        return 0
    with open("balance.json") as f:
        balance = json.load(f)
    return balance


def save_balance(balance):
    with open("balance.json", "w") as f:
        json.dump(balance, f)
