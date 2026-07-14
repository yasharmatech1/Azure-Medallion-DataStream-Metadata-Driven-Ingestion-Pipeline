import csv
import random
import uuid
from datetime import datetime, timedelta

# Configuration
NUM_ROWS = 105000  # 1 Lakh+ rows
OUTPUT_FILE = "massive_sales_dataset.csv"

categories = {
    "Electronics": [("Apple iPhone 15", 999), ("Sony Headphones", 299), ("Dell XPS Laptop", 1200), ("Logitech Mouse", 99)],
    "Clothing": [("Nike Running Shoes", 120), ("Adidas Hoodie", 60), ("Levi's Jeans", 80), ("Puma T-Shirt", 30)],
    "Home Appliances": [("Samsung Microwave", 150), ("Dyson Vacuum", 499), ("Philips Air Fryer", 120), ("Keurig Coffee Maker", 90)],
    "Books": [("Atomic Habits", 15), ("Sapiens", 22), ("Thinking Fast and Slow", 18), ("Deep Work", 16)],
    "Beauty": [("L'Oreal Shampoo", 12), ("Mac Lipstick", 35), ("Clinique Moisturizer", 45), ("Nivea Body Wash", 8)]
}

payment_methods = ["Credit Card", "UPI", "Cash", "Net Banking", "Debit Card"]
locations = ["Delhi", "Mumbai", "Bangalore", "Hyderabad", "Pune", "Kolkata", "Chennai", "Ahmedabad"]

start_date = datetime(2026, 7, 11, 0, 0, 0)

print(f"Generating {NUM_ROWS} realistic rows... Please wait.")

with open(OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Writing Header
    writer.writerow([
        "transaction_id", "order_id", "customer_id", "product_category", 
        "product_name", "quantity", "unit_price", "total_price", 
        "payment_method", "store_location", "LastModifiedDate"
    ])
    
    for i in range(NUM_ROWS):
        # Generate Realistic Fields
        txn_id = f"TXN{1000000 + i}"
        order_id = f"ORD-{random.randint(500000, 999999)}"
        cust_id = f"CUST-{random.randint(10000, 99999)}"
        
        category = random.choice(list(categories.keys()))
        product, unit_price = random.choice(categories[category])
        
        # Introduce dirty data (1% chance of null order_id to test Databricks quality checks)
        if random.random() < 0.01:
            order_id = ""
            
        quantity = random.randint(1, 5)
        total_price = quantity * unit_price
        
        pay_method = random.choice(payment_methods)
        loc = random.choice(locations)
        
        # Spread timestamps realistically over 4 days
        seconds_to_add = random.randint(0, 345600)  # 4 days range
        txn_time = start_date + timedelta(seconds=seconds_to_add)
        
        writer.writerow([
            txn_id, order_id, cust_id, category, product, 
            quantity, unit_price, total_price, pay_method, 
            loc, txn_time.strftime('%Y-%m-%d %H:%M:%S')
        ])

print(f"Success! '{OUTPUT_FILE}' has been generated. Ready for big data ingestion.")