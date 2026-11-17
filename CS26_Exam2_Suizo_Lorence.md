# KaPe Coffee Shop Management System
## CS 26 – Exam 2 Project Technical Documentation
 
**Document type:** Technical Documentation  
**Course coverage:** Weeks 4–5 Python concepts  
**Program type:** Console-based application
 
## 1. Program Overview
KaPe is a console application designed to help manage the daily operations of a coffee shop. It consists of three main subsystems: Ordering System, Management System, and Dashboard System.
 
The Ordering System allows customers to browse products, customize drinks, and place orders either in the shop (**In-Store**) or through the **online ordering channel** (**Online Pickup** or **Online Delivery**). The Management System allows the administrator to manage products, inventory, and incoming orders, including the status of online orders. The Dashboard System displays sales information and business performance, including sales per order type.
 
The program uses Python with a text-menu console interface and JSON files for storing data. The user types the number of a menu option to choose an action.
 
## 2. Problem Description
Managing a coffee shop manually can make it difficult to organize customer orders, monitor product availability, and track sales. Orders that come from online customers add more details to record, such as who the customer is, where to deliver, and whether payment has been received. Recording transactions and updating inventory manually may also lead to incorrect information.
 
**Input:** Customer orders and drink customizations, order type (in-store, online pickup, online delivery), customer details for online orders (name, contact number, delivery address), product information and prices, inventory quantities, payment method and transaction details.
 
**Processing:** Validate customer orders, selected customizations and online customer details; calculate order subtotals, delivery fees and totals; process and record transactions; update inventory after successful transactions and restore it when an order is cancelled; organize sales and order information for the dashboard.
 
**Output:** Order confirmation and receipt, updated product and inventory records, order status and transaction history, sales summaries (including sales by order type) and dashboard information.
 
## 3. Objectives
1. Allow customers to browse products, customize their orders, and order in-store or online.
2. Manage product information, inventory, and the progress of orders, including online orders.
3. Calculate order totals (including delivery fees) and record successful transactions.
4. Save and load product, order, and transaction records using JSON files.
5. Display sales information and handle invalid inputs and file errors.

## 4. Program Requirements and Features
 
### Ordering System
The ordering system allows customers to view available products and place orders.
 
Features include:
- Display available coffee shop products.
- Select products, quantities, drink size and temperature.
- Add products to the cart and remove items from the cart.
- Choose an order type: In-Store, Online Pickup, or Online Delivery.
- Enter customer details for online orders (name and contact number; delivery address for Online Delivery).
- Calculate the subtotal, delivery fee (PHP 50 for Online Delivery), and total amount.
- Select a payment method (Cash or GCash).
- Process customer transactions and show a receipt.
- Automatically update product stock after a successful transaction.
- Save completed orders and transaction records.

### Online Ordering Rules
| Order type | Customer details required | Delivery fee | Payment status when placed |
|---|---|---|---|
| In-Store | None | PHP 0 | Paid |
| Online Pickup | Name, contact number | PHP 0 | GCash: Paid; Cash: Pay on Pickup |
| Online Delivery | Name, contact number, address | PHP 50 | GCash: Paid; Cash: Pay on Delivery |
 
Cash on an online order is marked as paid when the administrator sets the order to Completed. The contact number must contain 10 to 12 digits (a leading `+`, spaces and dashes are allowed).
 
### Management System
The management system provides access to product and order management functions. A login system restricts access to these functions.
 
Features include:
- Management login.
- Add new products, edit product information, delete products, and update prices.
- Restock products and manage product availability.
- View customer orders with their order type, customer name, payment status and status.
- View the contact number and delivery address of an online order.
- Update order status. The available statuses depend on the order type:

| Order type | Statuses |
|---|---|
| In-Store | Pending, Preparing, Completed, Cancelled |
| Online Pickup | Pending, Preparing, Ready, Completed, Cancelled |
| Online Delivery | Pending, Preparing, Out for Delivery, Completed, Cancelled |
 
- Cancelling an order returns its items to stock. Completed or cancelled orders cannot be changed again.

### Dashboard
The dashboard provides a summary of the coffee shop's basic operations.
 
Features include:
- Display total sales (cancelled orders are excluded).
- Display the number of completed orders and the number of online orders.
- Display the total number of products.
- View recent transactions and best-selling products.
- Display low-stock products (5 or fewer in stock).
- Display the number of orders and sales for each order type.

### Limitations
The current prototype has the following limitations:
 
- The program runs in the console with text menus and has no graphical interface. This is intended for initial testing and demonstration and may be improved in the final version.
- Online orders are entered through the same console program (for example, by staff taking an order on behalf of a customer). The prototype does not include a website or mobile storefront for customers to order on their own.
- Cash and GCash are recorded as payment methods, but the system does not connect to an actual payment gateway, so a GCash payment is only recorded as paid.
- The delivery fee is a fixed amount, and there is no delivery tracking or rider assignment.
- The available customization choices are preset and cannot be configured through the management interface.

### Possible Future Improvements
- Add a graphical interface (for example, using Tkinter) and improve the overall user experience.
- Add a web or mobile storefront so customers can place online orders themselves, with real online payment integration.
- Calculate delivery fees by distance or area, and add rider assignment.
- Allow management users to configure product customizations.
- Provide more detailed sales reports.

## 5. Program Structure
 
```
KaPe_shop_system/
│
├── main.py
├── ordering.py
├── management.py
├── dashboard.py
├── storage.py
├── transactions.py
├── test_kape.py
│
├── products.json
├── orders.json
└── transactions.json
```
 
- `main.py` contains the console menus (Customer Ordering, Management and Dashboard), reads the user's input, and calls functions from the other modules.
- `ordering.py` contains cart functions, drink customization options, order types, delivery fee calculation, and customer detail validation.
- `management.py` contains product, inventory, and order management functions, including order status rules.
- `dashboard.py` contains sales summaries and business reports.
- `storage.py` contains JSON file reading and writing operations.
- `transactions.py` contains order validation and transaction processing.
- `test_kape.py` runs the automated test cases (T01-T18) against these functions, using a temporary data folder.
- `products.json` stores product information.
- `orders.json` stores customer order records, including order type, customer details and status.
- `transactions.json` stores completed transaction records.

**Example import:**
 
```python
from storage import load_data, save_data
from transactions import process_transaction
```
 
This separation keeps the program organized by responsibility. The main module can call functions from the other modules, while the storage module provides shared file operations.
 
## 6. Data Structures Used
 
### List
A list stores collections of products, cart items, and customer orders because multiple records may be added or removed.
 
```python
cart = []
```
 
### Dictionary
Each product is stored as a dictionary containing its information:
 
```python
product = {
    "code": "P001",
    "name": "Iced Coffee",
    "price": 100.0,
    "stock": 20,
    "available": True
}
```
 
Each order is also a dictionary. Online orders store the customer's details in a nested dictionary:
 
```python
order = {
    "order_id": "ORD-0003",
    "order_type": "Online Delivery",
    "customer": {"name": "Ben Lim", "contact": "+639171234567", "address": "12 Rizal St, Cebu"},
    "items": [...],
    "subtotal": 280.0,
    "delivery_fee": 50.0,
    "total": 330.0,
    "payment_method": "GCash",
    "payment_status": "Paid",
    "status": "Pending"
}
```
 
A dictionary makes it easier to access and update specific information using its keys.
 
### Tuple
A tuple stores fixed choices that should not change during normal program execution.
 
```python
DRINK_SIZES = ("Small", "Medium", "Large")
TEMPERATURES = ("Hot", "Iced")
PAYMENT_METHODS = ("Cash", "GCash")
ORDER_TYPES = ("In-Store", "Online Pickup", "Online Delivery")
```
 
A tuple is appropriate because these choices are fixed options that the program uses when validating customer selections.
 
## 7. Functions and Responsibilities
 
| Function | Parameters | Returns | Responsibility |
|---|---|---|---|
| `display_products` | `products` | `None` | Displays available products for customers |
| `add_to_cart` | `cart`, `product`, `customization`, `quantity` | `None` | Adds a customized product to the customer's cart |
| `calculate_total` | `cart` | `float` | Calculates the subtotal of all items in the cart |
| `calculate_delivery_fee` | `order_type` | `float` | Returns the delivery fee for the order type (PHP 50 for Online Delivery, otherwise 0) |
| `calculate_grand_total` | `cart`, `order_type` | `float` | Returns the subtotal plus the delivery fee |
| `validate_customer` | `order_type`, `customer` | `bool` | Checks the order type and the name, contact number and address required for online orders |
| `validate_order` | `order`, `products` | `bool` | Checks quantities, availability and stock for every item |
| `process_transaction` | `cart`, `payment_method`, `products`, `order_type`, `customer` | `bool` | Validates the order, records it, and updates stock |
| `save_transaction` | `transaction`, `filename` | `None` | Saves completed transaction details to a JSON file |
| `load_data` | `filename` | `list` | Loads records from a JSON file or returns an empty list if the file is missing |
| `update_stock` | `products`, `product_code`, `quantity` | `None` | Updates product stock after a successful transaction |
| `statuses_for_type` | `order_type` | `tuple` | Returns the order statuses that apply to an order type |
| `update_order_status` | `order_id`, `status` | `None` | Changes an order's status; cancelling restores stock and completing marks cash as paid |
 
### 7.1 Example: Subtotal Function
 
```python
def calculate_total(cart):
    """Total price of all items in the cart."""
    total = 0.0
    for item in cart:
        total += item["price"] * item["quantity"]
    return total
```
 
This function loops through the cart list and multiplies each item's price by its quantity, then returns the sum. `calculate_grand_total` adds the delivery fee to this value.
 
### 7.2 Example: Customer Validation Function
 
```python
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
```
 
In-store orders need no customer details, so the function returns right away. For online orders it raises a `ValueError` with a specific message if the name is missing, if the contact number (after removing spaces, dashes and a leading `+`) is not 10 to 12 digits, or if a delivery order has no address.
 
### 7.3 Example: Order Validation Function
 
```python
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
```

This function rejects an empty cart, checks every item, and then compares the total requested for each product with its stock. Adding up the quantities per product first means the same drink ordered with different sizes still cannot exceed the stock.
 
## 8. File Handling Procedures
The system uses JSON files to store product information, customer orders, and completed transactions. JSON is a text-based format that can represent Python dictionaries and lists. The `json` module converts the Python data when saving and reads it back when loading.
 
**Example:**
 
```python
class StorageError(Exception):
    """Raised when a data file is malformed or cannot be read/written."""
 
 
def save_data(filename, data):
    """Write data to a JSON file, creating or replacing it."""
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
    except OSError as error:
        raise StorageError(f"Could not write {os.path.basename(filename)}: {error}") from error
 
 
def load_data(filename):
    """Load records from a JSON file. A missing file returns an empty list.
    Malformed JSON is reported with a StorageError instead of being ignored."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError as error:
        raise StorageError(f"{os.path.basename(filename)} is malformed: {error}") from error
    except OSError as error:
        raise StorageError(f"Could not read {os.path.basename(filename)}: {error}") from error
```
 
### File Modes
 
- **Write mode (`w`)** – Creates the file or replaces its existing contents when saving records. Append mode (`a`) is not used: to add a record, `save_transaction` loads the list, appends the new record, and writes the whole list back.
- **Read mode (`r`)** – Opens the file to retrieve saved records.
- **UTF-8 encoding** – Provides consistent text encoding for names and addresses.
- **`with open(...)`** – Automatically closes the file after the operation is completed, including when an error occurs inside the block.

If a data file does not exist, `load_data` returns an empty list so the program can begin with no saved records. When the program starts, `initialize_files` creates any missing file (with sample products in `products.json`).
 
If a JSON file contains invalid or damaged data, `json.load()` raises a `json.JSONDecodeError`. `load_data` converts it to a `StorageError` with a readable message, so the program reports the problem instead of silently treating damaged data as valid records.
 
When an order is placed, the orders and transactions files are loaded before any stock is changed, so a damaged file stops the process before it makes any changes.
 
**Implementation status:** JSON storage is implemented. Records are saved in `products.json`, `orders.json` and `transactions.json` and persist between program runs.

## 9. Error Handling
 
Error handling is important in KaPe because incorrect quantities or customer details can produce wrong stock counts and unusable orders.
 
The program checks common input and data errors, including:
 
- Zero or negative quantities.
- Quantities that exceed the available stock, and unavailable products.
- Letters entered where a number is expected, such as in the quantity.
- An empty cart at checkout.
- Missing customer name, invalid contact number, or missing delivery address on online orders.
- Product codes and order IDs that do not exist.
- Status changes that do not apply to the order type, or changes to a completed or cancelled order.
- Missing or damaged data files.

**Example:**
 
```python
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
```
 
Every menu action runs inside this `try` block. The functions raise a `ValueError` (or a `StorageError` for file problems) with a specific message, and `run_menu` prints it as `Error: ...` and shows the menu again instead of ending the program.
 
Text typed by the user is converted at the point of input, so a conversion error can be reported clearly:
 
```python
try:
    quantity = int(ask("Quantity: "))
except ValueError:
    raise ValueError("Quantity must be a whole number") from None
```
 
**Input-validation errors and programming errors are handled differently.** Only `ValueError` and `StorageError` are caught, because they describe problems with the user's input or data files. Other exceptions, such as a `KeyError` or `TypeError` caused by a mistake in the code, are not caught, so they stop the program with a traceback instead of being hidden, and no bare `except:` is used. The one extra case is in `main`, where `EOFError` and `KeyboardInterrupt` (pressing Ctrl+C) end the program politely:
 
```python
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
```
 
## 10. Testing, Debugging, and Results
Testing is used to check whether the ordering, online ordering, management, transaction, and file handling operations produce the expected results. The cases cover normal cases (T01, T05, T06, T07), boundary cases (T16, T17, T18), and invalid-input or failure cases (the rest).
 
T01-T18 are automated in `test_kape.py`: running `python test_kape.py` runs them on a temporary copy of the data and prints each actual result. T19 and T20 are run through the console menus by typing the entries shown. The expected results below are the behavior the program is designed to show; the actual results are still pending.
 
### 10.1 Test Cases
 
| Test ID | Scenario | Input | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| T01 | Valid in-store order | P001, Large, Iced, quantity 2 | 1 line in cart; subtotal 240.0 | Pending actual test | Pending |
| T02 | Empty order | Checkout with no items | ValueError | Pending actual test | Pending |
| T03 | Zero quantity | Quantity = 0 | ValueError | Pending actual test | Pending |
| T04 | Insufficient stock (99 requested, 20 in stock) | Quantity 99 (stock 20) | ValueError | Pending actual test | Pending |
| T05 | Successful in-store transaction (Cash) | Cart of 2 Iced Coffee, Cash | Order and transaction saved; stock reduced to 18 | Pending actual test | Pending |
| T06 | Online Pickup order (Cash, name and contact given) | Caffe Latte × 1, Cash, name and contact | No delivery fee; total 140.0; Pay on Pickup; status Pending | Pending actual test | Pending |
| T07 | Online Delivery order (GCash, address given) | Cappuccino × 2, GCash, name, contact, address | Total 330.0 (280 + 50 fee); Paid | Pending actual test | Pending |
| T08 | Online order with no customer name | Online Pickup, name left empty | ValueError | Pending actual test | Pending |
| T09 | Invalid contact number (`abc`) | Contact number `abc` | ValueError | Pending actual test | Pending |
| T10 | Online Delivery with a blank address | Online Delivery, address `" "` | ValueError | Pending actual test | Pending |
| T11 | Cancel an online order (2 items) | Cancel ORD-0001, then try to set it to Pending | Stock restored (13 -> 15); a cancelled order cannot be changed again | Pending actual test | Pending |
| T12 | Status that does not apply (`Out for Delivery` on a pickup order) | Set a pickup order to `Out for Delivery` | ValueError | Pending actual test | Pending |
| T13 | Load a file that does not exist | A file path that does not exist | Empty list `[]` | Pending actual test | Pending |
| T14 | Load a file containing malformed JSON (`{bad`) | File containing `{bad` | StorageError | Pending actual test | Pending |
| T15 | Dashboard figures (1 in-store 240.0, 1 completed pickup 140.0, 1 cancelled delivery) | Three orders: in-store, completed pickup, cancelled delivery | Sales 380.0 (cancelled excluded); 1 completed; 1 online order | Pending actual test | Pending |
| T16 | Boundary: quantity equal to stock (20) and one above (21) | Quantity 20 and 21 for a product with stock 20 | 20 accepted; 21 rejected with ValueError; sold-out item leaves the menu | Pending actual test | Pending |
| T17 | Boundary: contact number length (valid range is 10 to 12 digits) | Contact numbers of 9, 10, 12 and 13 digits | 9 rejected; 10 accepted; 12 accepted; 13 rejected | Pending actual test | Pending |
| T18 | Boundary: low-stock limit (stock of 5 or less is listed) | Product stocks of 5 and 6 | P001 (stock 5) listed; P002 (stock 6) not listed | Pending actual test | Pending |
| T19 | Console walkthrough: customer ordering | Ran `main.py` with scripted keyboard input. In Customer Ordering: add Iced Coffee (Large, Iced) × 2; then quantity 0, quantity `abc`, quantity 99 for Caffe Latte, and product code `ZZZ`; checkout an Online Delivery order with a blank name, then valid details, paying with GCash; checkout again with an empty cart | First item added; each bad entry prints an error and returns to the menu; invalid customer details are asked for again; the receipt is shown; the empty checkout is rejected | Pending actual test | Pending |
| T20 | Console walkthrough: management and dashboard | Management login with a wrong password and then the correct one; view orders; cancel an Online Delivery order and try to change it again; set an Online Pickup order to Ready and then Completed; add, restock, toggle availability of, and delete a product; open the Dashboard | Login succeeds on the second attempt; the cancelled order cannot be changed again; the pickup order goes through its statuses; product changes are saved; the dashboard excludes the cancelled order | Pending actual test | Pending |
 
**Note:** The actual results are pending. After running the tests, replace each pending result with what is observed and update the status to Pass or Fail.
 
### 10.2 Debugging
During development, the program should be checked for problems involving product codes, stock calculations, and order processing.
 
One important calculation to verify is the Online Delivery total. The delivery fee must be added to the subtotal exactly once.
 
**Verification example:**
 
- Subtotal: 280.00 (2 items at PHP 140.00)
- Delivery fee: 50.00
- Expected total: 330.00

This example describes the expected calculation, not a confirmed debugging issue or test result.
 
For the final documentation, record an actual problem encountered during development, its cause, the correction made, and how the correction was tested. If no defect was found, explain what checks were performed to verify the program.

## 11. Conclusion
KaPe demonstrates how lists, dictionaries, tuples, functions, modules, file handling, and error handling work together in a small console application. It lets customers order in-store or online, lets the administrator manage products and order statuses, and summarizes sales on a dashboard, with its records saved in JSON files.
 
The program is a prototype with some limitations. It runs in the console, has no customer-facing storefront, and records payments without processing them through a real payment service.
 
Possible improvements include a web or mobile storefront with real online payment, and administrator-configurable drink options with more detailed sales reports.

## 12. References
- Python Software Foundation. *Python 3 Documentation*. https://docs.python.org/3/
- Python Software Foundation. *The Python Tutorial – Data Structures*. https://docs.python.org/3/tutorial/datastructures.html
- Python Software Foundation. *The Python Tutorial – Input and Output*. https://docs.python.org/3/tutorial/inputoutput.html
- Python Software Foundation. *The `json` module documentation*. https://docs.python.org/3/library/json.html

*References should be retained only if they were actually consulted while developing or documenting the project. Acknowledge any additional sources or assistance according to the course's academic-integrity requirements.*