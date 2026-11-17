from ordering import ORDER_TYPES
from storage import ORDERS_FILE, PRODUCTS_FILE, TRANSACTIONS_FILE, load_data
 
LOW_STOCK_THRESHOLD = 5
 
 
def get_summary():
    """Return a dictionary of dashboard figures.
    Cancelled orders are excluded from sales figures."""
    products = load_data(PRODUCTS_FILE)
    orders = load_data(ORDERS_FILE)
    transactions = load_data(TRANSACTIONS_FILE)
 
    cancelled = {o["order_id"] for o in orders if o.get("status") == "Cancelled"}
    valid = [t for t in transactions if t["order_id"] not in cancelled]
 
    sold = {}
    channels = {order_type: [0, 0.0] for order_type in ORDER_TYPES}
    for transaction in valid:
        for item in transaction["items"]:
            sold[item["name"]] = sold.get(item["name"], 0) + item["quantity"]
        order_type = transaction.get("order_type", "In-Store")
        if order_type in channels:
            channels[order_type][0] += 1
            channels[order_type][1] += transaction["total"]
 
    return {
        "total_sales": sum(t["total"] for t in valid),
        "completed_orders": sum(1 for o in orders if o.get("status") == "Completed"),
        "online_orders": sum(1 for o in orders
                             if o.get("order_type", "In-Store") != "In-Store"
                             and o.get("status") != "Cancelled"),
        "total_products": len(products),
        "recent_transactions": list(reversed(transactions))[:10],
        "best_sellers": sorted(sold.items(), key=lambda pair: pair[1], reverse=True)[:5],
        "low_stock": [p for p in products if p["stock"] <= LOW_STOCK_THRESHOLD],
        "sales_by_channel": [(name, count, total) for name, (count, total) in channels.items()],
    }