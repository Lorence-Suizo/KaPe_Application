from datetime import datetime
 
from ordering import (PAYMENT_METHODS, calculate_delivery_fee, calculate_total,
                      describe_item, find_product, validate_customer)
from storage import (ORDERS_FILE, PRODUCTS_FILE, TRANSACTIONS_FILE,
                     load_data, next_id, save_data)
 
 
def validate_order(order, products):
    """Check quantities, availability and stock for every line.
    Raises ValueError if the order cannot proceed, otherwise returns True."""
    if not order:
        raise ValueError("Cart is empty")
 
    requested = {}
    for item in order:
        if item["quantity"] <= 0:
            raise ValueError("Invalid quantity")
        product = find_product(products, item["code"])
        if product is None:
            raise ValueError(f"Unknown product: {item['name']}")
        if not product["available"]:
            raise ValueError(f"{product['name']} is currently unavailable")
        requested[item["code"]] = requested.get(item["code"], 0) + item["quantity"]
 
    for code, quantity in requested.items():
        product = find_product(products, code)
        if quantity > product["stock"]:
            raise ValueError(f"Insufficient stock for {product['name']}")
 
    return True
 
 
def update_stock(products, product_code, quantity):
    """Reduce a product's stock after a successful transaction."""
    product = find_product(products, product_code)
    if product is None:
        raise ValueError(f"Unknown product code: {product_code}")
    if quantity > product["stock"]:
        raise ValueError(f"Insufficient stock for {product['name']}")
    product["stock"] -= quantity
 
 
def save_transaction(transaction, filename):
    """Append a completed transaction to a JSON file."""
    records = load_data(filename)
    records.append(transaction)
    save_data(filename, records)
 
 
def get_payment_status(order_type, payment_method):
    """GCash and in-store payments are recorded as paid. Cash on an online
    order is collected when the customer picks up or receives the order."""
    if order_type == "In-Store" or payment_method == "GCash":
        return "Paid"
    if order_type == "Online Pickup":
        return "Pay on Pickup"
    return "Pay on Delivery"
 
 
def process_transaction(cart, payment_method, products, order_type="In-Store", customer=None):
    """Validate the order, record it, and update stock.
    Returns True on success; raises ValueError if the order is invalid."""
    if payment_method not in PAYMENT_METHODS:
        raise ValueError("Select a valid payment method")
    validate_customer(order_type, customer)
    validate_order(cart, products)
 
    # Load everything first so a bad file stops the process before any change.
    orders = load_data(ORDERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)
 
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    order_id = next_id(orders, "order_id", "ORD")
    subtotal = calculate_total(cart)
    delivery_fee = calculate_delivery_fee(order_type)
    total = subtotal + delivery_fee
    items = [dict(item) for item in cart]
    payment_status = get_payment_status(order_type, payment_method)
 
    customer_info = {}
    if order_type != "In-Store":
        customer_info = {
            "name": customer["name"].strip(),
            "contact": customer["contact"].strip(),
            "address": (customer.get("address") or "").strip() if order_type == "Online Delivery" else "",
        }
 
    for item in cart:
        update_stock(products, item["code"], item["quantity"])
    save_data(PRODUCTS_FILE, products)
 
    orders.append({
        "order_id": order_id,
        "timestamp": timestamp,
        "order_type": order_type,
        "customer": customer_info,
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "payment_method": payment_method,
        "payment_status": payment_status,
        "status": "Pending",
    })
    save_data(ORDERS_FILE, orders)
 
    save_transaction({
        "transaction_id": next_id(transactions, "transaction_id", "TXN"),
        "order_id": order_id,
        "timestamp": timestamp,
        "order_type": order_type,
        "customer": customer_info,
        "items": items,
        "subtotal": subtotal,
        "delivery_fee": delivery_fee,
        "total": total,
        "payment_method": payment_method,
        "payment_status": payment_status,
    }, TRANSACTIONS_FILE)
    return True
 
 
def build_receipt(transaction):
    """Return a printable receipt for a transaction record."""
    lines = [
        "KaPe Coffee Shop",
        "-" * 36,
        f"Order:   {transaction['order_id']}",
        f"Date:    {transaction['timestamp']}",
        f"Type:    {transaction.get('order_type', 'In-Store')}",
    ]
    customer = transaction.get("customer") or {}
    if customer:
        lines.append(f"Name:    {customer['name']}")
        lines.append(f"Contact: {customer['contact']}")
        if customer.get("address"):
            lines.append(f"Address: {customer['address']}")
    lines.append(f"Payment: {transaction['payment_method']} ({transaction.get('payment_status', 'Paid')})")
    lines.append("-" * 36)
    for item in transaction["items"]:
        lines.append(f"{item['quantity']} x {item['name']} ({describe_item(item)})")
        lines.append(f"      @ {item['price']:.2f} = {item['price'] * item['quantity']:.2f}")
    lines.append("-" * 36)
    if transaction.get("delivery_fee"):
        lines.append(f"Subtotal:     PHP {transaction['subtotal']:.2f}")
        lines.append(f"Delivery fee: PHP {transaction['delivery_fee']:.2f}")
    lines += [f"TOTAL: PHP {transaction['total']:.2f}", "Thank you!"]
    return "\n".join(lines)