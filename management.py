from ordering import find_product
from storage import ORDERS_FILE, PRODUCTS_FILE, load_data, next_id, save_data
 
# Prototype credentials (see limitations in the documentation).
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "kape123"
 
ORDER_STATUSES = ("Pending", "Preparing", "Ready", "Out for Delivery", "Completed", "Cancelled")
 
 
def statuses_for_type(order_type):
    """Statuses that make sense for an order type: 'Ready' is for pickup orders
    and 'Out for Delivery' is only for delivery orders."""
    skipped = {"In-Store": ("Ready", "Out for Delivery"),
               "Online Pickup": ("Out for Delivery",),
               "Online Delivery": ("Ready",)}.get(order_type, ())
    return tuple(s for s in ORDER_STATUSES if s not in skipped)
 
 
def login(username, password):
    """Return True if the credentials match the administrator account."""
    return username == ADMIN_USERNAME and password == ADMIN_PASSWORD
 
 
def _parse_price(value):
    try:
        price = float(value)
    except (TypeError, ValueError):
        raise ValueError("Price must be a number") from None
    if price <= 0:
        raise ValueError("Price must be greater than zero")
    return price
 
 
def _parse_stock(value):
    try:
        stock = int(value)
    except (TypeError, ValueError):
        raise ValueError("Stock must be a whole number") from None
    if stock < 0:
        raise ValueError("Stock cannot be negative")
    return stock
 
 
def _require_product(products, code):
    product = find_product(products, code)
    if product is None:
        raise ValueError("Select a product first")
    return product
 
 
def _next_product_code(products):
    """Return the next code in the P001 style."""
    highest = 0
    for product in products:
        try:
            highest = max(highest, int(product["code"][1:]))
        except (KeyError, ValueError):
            continue
    return f"P{highest + 1:03d}"
 
 
def add_product(products, name, price, stock):
    """Add a new product and save."""
    name = name.strip()
    if not name:
        raise ValueError("Product name is required")
    if any(p["name"].lower() == name.lower() for p in products):
        raise ValueError("A product with that name already exists")
    product = {
        "code": _next_product_code(products),
        "name": name,
        "price": _parse_price(price),
        "stock": _parse_stock(stock),
        "available": True,
    }
    products.append(product)
    save_data(PRODUCTS_FILE, products)
    return product
 
 
def edit_product(products, code, name, price):
    """Edit a product's name and price and save."""
    product = _require_product(products, code)
    name = name.strip()
    if not name:
        raise ValueError("Product name is required")
    if any(p["code"] != code and p["name"].lower() == name.lower() for p in products):
        raise ValueError("A product with that name already exists")
    product["name"] = name
    product["price"] = _parse_price(price)
    save_data(PRODUCTS_FILE, products)
 
 
def update_price(products, code, price):
    """Update only a product's price and save."""
    product = _require_product(products, code)
    product["price"] = _parse_price(price)
    save_data(PRODUCTS_FILE, products)
 
 
def delete_product(products, code):
    """Delete a product and save."""
    product = _require_product(products, code)
    products.remove(product)
    save_data(PRODUCTS_FILE, products)
 
 
def restock_product(products, code, quantity):
    """Add stock to a product and save."""
    product = _require_product(products, code)
    amount = _parse_stock(quantity)
    if amount == 0:
        raise ValueError("Restock quantity must be greater than zero")
    product["stock"] += amount
    save_data(PRODUCTS_FILE, products)
 
 
def set_availability(products, code, available):
    """Mark a product available or unavailable and save."""
    product = _require_product(products, code)
    product["available"] = bool(available)
    save_data(PRODUCTS_FILE, products)
 
 
def view_orders():
    """Return all customer orders, newest first."""
    return list(reversed(load_data(ORDERS_FILE)))
 
 
def get_order(order_id):
    """Return the order with the given ID, or None."""
    for order in load_data(ORDERS_FILE):
        if order["order_id"] == order_id:
            return order
    return None
 
 
def update_order_status(order_id, status):
    """Change an order's status and save.
    Cancelling an order returns its items to stock. Completing an order
    marks any cash payment as received."""
    orders = load_data(ORDERS_FILE)
    order = next((o for o in orders if o["order_id"] == order_id), None)
    if order is None:
        raise ValueError("Order not found")
 
    order_type = order.get("order_type", "In-Store")
    if status not in statuses_for_type(order_type):
        raise ValueError(f"'{status}' is not a valid status for {order_type} orders")
    if order["status"] in ("Completed", "Cancelled"):
        raise ValueError(f"Order is already {order['status'].lower()}")
 
    if status == "Cancelled":
        products = load_data(PRODUCTS_FILE)
        for item in order["items"]:
            product = find_product(products, item["code"])
            if product is not None:
                product["stock"] += item["quantity"]
        save_data(PRODUCTS_FILE, products)
    elif status == "Completed":
        order["payment_status"] = "Paid"
 
    order["status"] = status
    save_data(ORDERS_FILE, orders)