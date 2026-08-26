import pandas as pd
import numpy as np
from faker import Faker

fake = Faker(['en_GB', 'en_US'])
np.random.seed(42)

# 1. Generate Customers Data
customers = []
for i in range(1, 1001):
    customers.append({
        'customer_id': f"CUST_{i:05d}",
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'country': np.random.choice(['UK', 'US', 'DE'], p=[0.4, 0.4, 0.2]),
        'signup_date': fake.date_between(start_date='-2y', end_date='today').isoformat()
    })
df_customers = pd.DataFrame(customers)
df_customers.to_csv('raw_customers.csv', index=False)

# 2. Generate Products Data
products = [
    {'product_id': 'PRD_001', 'sku_name': 'Daily Hydrating Cleanser 200ml', 'category': 'Skin Health', 'unit_cost_gbp': 4.50, 'msrp_gbp': 14.99},
    {'product_id': 'PRD_002', 'sku_name': 'Rapid Pain Relief 500mg (32 ct)', 'category': 'Self Care', 'unit_cost_gbp': 1.20, 'msrp_gbp': 5.49},
    {'product_id': 'PRD_003', 'sku_name': 'Allergy 24hr Defense (30 ct)', 'category': 'Self Care', 'unit_cost_gbp': 2.80, 'msrp_gbp': 11.99},
    {'product_id': 'PRD_004', 'sku_name': 'Total Care Daily Mouthwash 500ml', 'category': 'Oral Care', 'unit_cost_gbp': 1.80, 'msrp_gbp': 6.25}
]
df_products = pd.DataFrame(products)
df_products.to_csv('raw_products.csv', index=False)

print("SUCCESS: raw_customers.csv and raw_products.csv have been created!")