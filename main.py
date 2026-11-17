
"""
KaPe Coffee Shop Management System (console version).
Management login:  admin / kape123
"""

import getpass

import dashboard
import management
from ordering import (DRINK_SIZES, ORDER_TYPES, PAYMENT_METHODS, SIZE_EXTRA, TEMPERATURES,
                      add_to_cart, calculate_delivery_fee, calculate_grand_total,
                      calculate_total, describe_item, display_products, find_product,
                      remove_from_cart, validate_customer)
from storage import (PRODUCTS_FILE, TRANSACTIONS_FILE, StorageError,
                     initialize_files, load_data)
from transactions import build_receipt, process_transaction

LINE = "=" * 60


# ---------------------------------------------------------------- input helpers
def ask(prompt):
    """Read one line of input without surrounding spaces."""
    return input(prompt).strip()


def ask_int(prompt, error="Enter a whole number."):
    """Keep asking until the user enters a whole number."""
    while True:
        try:
            return int(ask(prompt))
        except ValueError:
            print(f"Invalid entry: {error}")


def choose(title, options, labels=None):
    """Show a numbered list and return the option the user picks."""
    labels = labels or options
    print(title)
    for number, label in enumerate(labels, 1):
        print(f"  [{number}] {label}")
    while True:
        number = ask_int("Select: ")
        if 1 <= number <= len(options):
            return options[number - 1]
        print(f"Invalid entry: choose a number from 1 to {len(options)}.")


def confirm(prompt):
    return ask(f"{prompt} (y/n): ").lower() == "y"


def run_menu(title, actions, back_label="Back"):
    """Show a menu until the user picks 0. actions is a list of (label, function).
    Errors raised by an action are printed and the menu is shown again."""
    while True:
        print(f"\n{LINE}\n{title}\n{LINE}")
        for number, (label, _) in enumerate(actions, 1):
            print(f"[{number}] {label}")
        print(f"[0] {back_label}")
        choice = ask("Select: ")
        if choice == "0":
            return
        if choice.isdigit() and 1 <= int(choice) <= len(actions):
            try:
                actions[int(choice) - 1][1]()
            except (ValueError, StorageError) as error:
                print(f"\nError: {error}")
        else:
            print("Invalid choice. Pick a number from the menu.")


# ------------------------------------------------------------------- ordering
def prompt_customer(order_type):
    """Ask for customer details until they pass validation."""
    print("\nCustomer details")
    while True:
        customer = {
            "name": ask("  Name: "),
            "contact": ask("  Contact number: "),
            "address": ask("  Delivery address: ") if order_type == "Online Delivery" else "",
        }
        try:
            validate_customer(order_type, customer)
            return customer
        except ValueError as error:
            print(f"Invalid entry: {error}")


def ordering_menu():
    cart = []

    def view_menu():
        print()
        display_products(load_data(PRODUCTS_FILE))

    def view_cart():
        if not cart:
            print("\nYour cart is empty.")
            return
        print(f"\n{'#':<4}{'Item':<22}{'Options':<16}{'Qty':>4}{'Subtotal':>11}")
        for number, item in enumerate(cart, 1):
            print(f"{number:<4}{item['name']:<22}{describe_item(item):<16}{item['quantity']:>4}"
                  f"{item['price'] * item['quantity']:>11.2f}")
        print(f"{'Subtotal:':>47}{calculate_total(cart):>11.2f}")

    def add_item():
        products = load_data(PRODUCTS_FILE)
        view_menu()
        product = find_product(products, ask("\nProduct code: ").upper())
        if product is None:
            raise ValueError("Product code not found")
        size_labels = []
        for size in DRINK_SIZES:
            if SIZE_EXTRA[size]:
                size_labels.append(f"{size} (+{SIZE_EXTRA[size]:.0f})")
            else:
                size_labels.append(size)
        size = choose("Size:", DRINK_SIZES, size_labels)
        temperature = choose("Temperature:", TEMPERATURES)
        try:
            quantity = int(ask("Quantity: "))
        except ValueError:
            raise ValueError("Quantity must be a whole number") from None
        add_to_cart(cart, product, {"size": size, "temperature": temperature}, quantity)
        print(f"Added {quantity} x {product['name']} to the cart.")

    def remove_item():
        view_cart()
        if cart:
            number = ask_int("Item number to remove: ")
            remove_from_cart(cart, number - 1)
            print("Item removed.")

    def checkout():
        if not cart:
            raise ValueError("Cart is empty")
        products = load_data(PRODUCTS_FILE)
        view_cart()
        order_type = choose("\nOrder type:", ORDER_TYPES)
        customer = {}
        if order_type != "In-Store":
            customer = prompt_customer(order_type)
        payment = choose("\nPayment method:", PAYMENT_METHODS)

        print(f"\nSubtotal:     PHP {calculate_total(cart):.2f}")
        print(f"Delivery fee: PHP {calculate_delivery_fee(order_type):.2f}")
        print(f"TOTAL:        PHP {calculate_grand_total(cart, order_type):.2f}")
        if not confirm("Place this order?"):
            print("Order not placed. Your cart is kept.")
            return

        process_transaction(cart, payment, products, order_type, customer)
        cart.clear()
        print(f"\n{LINE}\n{build_receipt(load_data(TRANSACTIONS_FILE)[-1])}\n{LINE}")

    run_menu("Customer Ordering", [
        ("View menu", view_menu),
        ("Add item to cart", add_item),
        ("Remove item from cart", remove_item),
        ("View cart", view_cart),
        ("Checkout", checkout),
    ], back_label="Back to main menu")
    if cart:
        print("Your unfinished cart was cleared.")


# ----------------------------------------------------------------- management
def print_products(products):
    print(f"\n{'Code':<6}{'Name':<22}{'Price':>8}{'Stock':>7}  Available")
    for p in products:
        print(f"{p['code']:<6}{p['name']:<22}{p['price']:>8.2f}{p['stock']:>7}  "
              f"{'Yes' if p['available'] else 'No'}")


def print_orders(orders):
    if not orders:
        print("\nNo orders yet.")
        return
    print(f"\n{'Order':<10}{'Date':<20}{'Type':<17}{'Customer':<14}{'Total':>9}  {'Payment':<24}Status")
    for o in orders:
        customer = (o.get("customer") or {}).get("name", "-")
        payment = f"{o['payment_method']} ({o.get('payment_status', 'Paid')})"
        print(f"{o['order_id']:<10}{o['timestamp']:<20}{o.get('order_type', 'In-Store'):<17}"
              f"{customer[:13]:<14}{o['total']:>9.2f}  {payment:<24}{o['status']}")


def management_menu():
    def view_products():
        print_products(load_data(PRODUCTS_FILE))

    def pick_code(products):
        print_products(products)
        return ask("\nProduct code: ").upper()

    def add_product():
        products = load_data(PRODUCTS_FILE)
        name = ask("Product name: ")
        price = ask("Price: ")
        stock = ask("Initial stock: ")
        product = management.add_product(products, name, price, stock)
        print(f"Added {product['name']} with code {product['code']}.")

    def edit_product():
        products = load_data(PRODUCTS_FILE)
        code = pick_code(products)
        product = find_product(products, code)
        if product is None:
            raise ValueError("Select a product first")
        name = ask(f"New name [{product['name']}]: ") or product["name"]
        price = ask(f"New price [{product['price']:.2f}]: ") or product["price"]
        management.edit_product(products, code, name, price)
        print("Product updated.")

    def update_price():
        products = load_data(PRODUCTS_FILE)
        code = pick_code(products)
        management.update_price(products, code, ask("New price: "))
        print("Price updated.")

    def restock():
        products = load_data(PRODUCTS_FILE)
        code = pick_code(products)
        management.restock_product(products, code, ask("Quantity to add: "))
        print("Stock updated.")

    def toggle_availability():
        products = load_data(PRODUCTS_FILE)
        code = pick_code(products)
        product = find_product(products, code)
        if product is None:
            raise ValueError("Select a product first")
        management.set_availability(products, code, not product["available"])
        print(f"{product['name']} is now {'available' if product['available'] else 'unavailable'}.")

    def delete_product():
        products = load_data(PRODUCTS_FILE)
        code = pick_code(products)
        product = find_product(products, code)
        if product is None:
            raise ValueError("Select a product first")
        if confirm(f"Delete {product['name']}?"):
            management.delete_product(products, code)
            print("Product deleted.")

    def view_orders():
        print_orders(management.view_orders())

    def update_status():
        print_orders(management.view_orders())
        order = management.get_order(ask("\nOrder ID (e.g. ORD-0001): ").upper())
        if order is None:
            raise ValueError("Order not found")
        order_type = order.get("order_type", "In-Store")
        customer = order.get("customer") or {}
        print(f"\n{order['order_id']} - {order_type} - current status: {order['status']}")
        if customer:
            print(f"Customer: {customer['name']}, {customer['contact']}"
                  + (f", {customer['address']}" if customer.get("address") else ""))
        status = choose("New status:", management.statuses_for_type(order_type))
        management.update_order_status(order["order_id"], status)
        print(f"{order['order_id']} is now {status}.")

    run_menu("Management", [
        ("View products", view_products),
        ("Add product", add_product),
        ("Edit product", edit_product),
        ("Update price", update_price),
        ("Restock product", restock),
        ("Toggle availability", toggle_availability),
        ("Delete product", delete_product),
        ("View orders", view_orders),
        ("Update order status", update_status),
    ], back_label="Logout")


def management_login():
    for attempt in range(3):
        username = ask("Username: ")
        password = getpass.getpass("Password: ")
        if management.login(username, password):
            management_menu()
            return
        print(f"Incorrect username or password. ({2 - attempt} attempts left)")
    print("Too many failed attempts.")


# ------------------------------------------------------------------ dashboard
def show_dashboard():
    summary = dashboard.get_summary()
    print(f"\n{LINE}\nDashboard\n{LINE}")
    print(f"Total sales:      PHP {summary['total_sales']:.2f}")
    print(f"Completed orders: {summary['completed_orders']}")
    print(f"Online orders:    {summary['online_orders']}")
    print(f"Total products:   {summary['total_products']}")

    print("\nSales by order type")
    for name, count, total in summary["sales_by_channel"]:
        print(f"  {name:<17}{count:>4} order(s)   PHP {total:>9.2f}")

    print("\nRecent transactions")
    if not summary["recent_transactions"]:
        print("  None yet.")
    for t in summary["recent_transactions"]:
        print(f"  {t['order_id']}  {t['timestamp']}  {t.get('order_type', 'In-Store'):<16}"
              f"PHP {t['total']:>8.2f}  {t['payment_method']}")

    print("\nBest-selling products")
    if not summary["best_sellers"]:
        print("  None yet.")
    for name, sold in summary["best_sellers"]:
        print(f"  {name:<22}{sold} sold")

    print(f"\nLow-stock products (stock of {dashboard.LOW_STOCK_THRESHOLD} or less)")
    if not summary["low_stock"]:
        print("  None.")
    for p in summary["low_stock"]:
        print(f"  {p['name']:<22}{p['stock']} left")


# ----------------------------------------------------------------------- main
def main():
    try:
        initialize_files()
    except StorageError as error:
        print(f"Error: {error}")
        return
    try:
        run_menu("KaPe Coffee Shop", [
            ("Customer Ordering", ordering_menu),
            ("Management (login required)", management_login),
            ("Dashboard", show_dashboard),
        ], back_label="Exit")
    except (EOFError, KeyboardInterrupt):
        print()
    print("Thank you for using KaPe. Goodbye!")


if __name__ == "__main__":
    main()