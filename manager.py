class Manager:
    def __init__(self):
        self.actions = {}

    def assign(self, name):
        def wrapper(func):
            self.actions[name] = func

        return wrapper

    def execute(self, name, inventory, balance, history, **kwargs):
        if name not in self.actions:
            print(f"Error: {name} not in actions")
            return inventory, balance, history
        else:
            return self.actions[name](balance, inventory, history, **kwargs)


manager = Manager()


@manager.assign("balance")
def perform_balance(balance, history, warehouse, value, actions):
    if actions == "add":
        balance += value
    elif actions == "subtract":
        if balance - value < 0:
            print("No money can be subtracted")
            return balance, history, warehouse
        balance -= value
    history.append(f"action: balance, cmd: {actions}, {value}")
    return balance, history, warehouse


@manager.assign("sale")
def perform_history(balance, history, warehouse, product_name, quantity):
    if product_name in warehouse:
        if quantity <= warehouse[product_name]:
            total_price = balance * quantity
            balance += total_price
            warehouse[product_name] -= quantity
            print(f"Products sold:{product_name},Quantity:{quantity}")
            history.append(product_name)
    else:
        print("Product not found in the warehouse or the quantity is not enough")
    return balance, history, warehouse


@manager.assign("purchase")
def perform_purchase(balance, history, warehouse, product_name, quantity, total_price):
    if total_price > balance:
        print("You have to low balance in your account")
        balance -= total_price
        print(f"You purchase {product_name}{quantity} items for {total_price}")
        if product_name not in warehouse:
            warehouse[product_name] = 0
            warehouse[product_name] += quantity
            history.append(product_name)

            return balance, history, warehouse


@manager.assign("sale")
def perform_sale(balance, history, warehouse):
    product_name = input("Enter the products name: ")
    price = int(input("Enter the price: "))
    quantity = int(input("Enter the quantity sold: "))
    if product_name in warehouse:
        if quantity <= warehouse[product_name]:
            total_price = price * quantity
            balance += total_price
            warehouse[product_name] -= quantity
            print(f"Products sold:{product_name},Quantity:{quantity}")
            history.append(product_name)
    else:
        print("Product not found in the warehouse or the quantity is not enough")

        return balance, history, warehouse


@manager.assign("account")
def perform_account(balance, history, warehouse):
    print(f"Current account balance is: {balance} ")

    return balance, history, warehouse


@manager.assign("account")
def perform_warehouse_list(balance, history, warehouse):
    for product_name, quantity in warehouse.items():
        print(f"{product_name}: {quantity}")

    return balance, history, warehouse


@manager.assign("warehouse")
def perform_warehouse(balance, history, warehouse):
    product_name = input("Enter the products name: ")
    if product_name in warehouse:
        print(f"{product_name} is available at the warehouse: {warehouse[product_name]}")
    else:
        print(f"The product name you are looking for are not in the warehouse")

        return balance, history, warehouse


@manager.assign("review")
def perform_review(balance, history, warehouse):
    first_index = int(input("Enter the first index: "))
    second_index = int(input("Enter the second index: "))
    for entry in history[first_index:second_index]:
        print(entry)
    else:
        print(f"The command are not supported review. Please select another command.")

        return balance, history, warehouse
