

DRINK_SIZES = ("Small", "Medium", "Large")
TEMPERATURES = ("Hot", "Iced")
PAYMENT_METHODS = ("Cash", "GCash")
ORDER_TYPES = ("In-Store", "Online Pickup", "Online Delivery")
 
# Flat fee added to Online Delivery orders.
DELIVERY_FEE = 50.0
 
# Extra charge added to the base price for each size.
SIZE_EXTRA = {"Small": 0.0, "Medium": 10.0, "Large": 20.0}
 
 
def find_product(products, code):
    """Return the product dictionary with the given code, or None."""
    for product in products:
        if product["code"] == code:
            return product
    return None
 
 
def get_available_products(products):
    """Return only products that are available and in stock."""
    return [p for p in products if p["available"] and p["stock"] > 0]
 
 
def display_products(products):
    """Print the available products (console view of the menu)."""
    print(f"{'Code':<6}{'Name':<22}{'Price':>8}{'Stock':>7}")
    for product in get_available_products(products):
        print(f"{product['code']:<6}{product['name']:<22}{product['price']:>8.2f}{product['stock']:>7}")
 
 
def quantity_in_cart(cart, code):
    """Total quantity of a product already in the cart (across customizations)."""
    return sum(item["quantity"] for item in cart if item["code"] == code)
 
 
def add_to_cart(cart, product, customization, quantity):
    """Add a customized product to the cart.
    customization is a dict: {"size": ..., "temperature": ...}.
    Raises ValueError for invalid choices, quantities or stock."""
    if product is None:
        raise ValueError("No product selected")
    if not product["available"]:
        raise ValueError(f"{product['name']} is currently unavailable")
    if customization.get("size") not in DRINK_SIZES:
        raise ValueError("Invalid drink size")
    if customization.get("temperature") not in TEMPERATURES:
        raise ValueError("Invalid temperature")
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")
    if quantity_in_cart(cart, product["code"]) + quantity > product["stock"]:
        raise ValueError(f"Insufficient stock for {product['name']} (available: {product['stock']})")
 
    unit_price = product["price"] + SIZE_EXTRA[customization["size"]]
 
    # Merge with an identical line already in the cart.
    for item in cart:
        if item["code"] == product["code"] and item["customization"] == customization:
            item["quantity"] += quantity
            return
 
    cart.append({
        "code": product["code"],
        "name": product["name"],
        "price": unit_price,
        "quantity": quantity,
        "customization": dict(customization),
    })
 
 
def remove_from_cart(cart, index):
    """Remove the cart line at the given index."""
    if not 0 <= index < len(cart):
        raise ValueError("Select an item to remove")
    del cart[index]
 
 
def calculate_total(cart):
    """Total price of all items in the cart."""
    total = 0.0
    for item in cart:
        total += item["price"] * item["quantity"]
    return total
 
 
def calculate_delivery_fee(order_type):
    """Delivery fee for the order type (only Online Delivery is charged)."""
    return DELIVERY_FEE if order_type == "Online Delivery" else 0.0
 
 
def calculate_grand_total(cart, order_type="In-Store"):
    """Cart subtotal plus any delivery fee."""
    return calculate_total(cart) + calculate_delivery_fee(order_type)
 
 
def validate_customer(order_type, customer):
    """Check the order type and the customer details required for online orders.
    customer is a dict with "name", "contact" and "address". Returns True or raises ValueError."""
    if order_type not in ORDER_TYPES:
        raise ValueError("Invalid order type")
    if order_type == "In-Store":
        return True
 
    customer = customer or {}
    if not customer.get("name", "").strip():
        raise ValueError("Customer name is required for online orders")
 
    digits = customer.get("contact", "").replace(" ", "").replace("-", "").lstrip("+")
    if not digits.isdigit() or not 10 <= len(digits) <= 12:
        raise ValueError("Enter a valid contact number (10 to 12 digits)")
 
    if order_type == "Online Delivery" and not customer.get("address", "").strip():
        raise ValueError("Delivery address is required for Online Delivery")
    return True
 
 
def describe_item(item):
    """Short text such as 'Large / Iced' for a cart line."""
    custom = item["customization"]
    return f"{custom['size']} / {custom['temperature']}"
 