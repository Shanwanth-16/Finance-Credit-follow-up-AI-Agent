from faker import Faker
import pandas as pd
import random

fake = Faker()

data = []

for i in range(8):
    data.append({
        "client_name": fake.name(),
        "invoice_no": f"INV{i+1:03}",
        "amount": random.randint(10000, 200000),
        "due_date": fake.date_between(start_date='-40d', end_date='today'),
        "email": fake.email(),
        "follow_up_count": random.randint(0,4)
    })

df = pd.DataFrame(data)
df.to_csv("invoices.csv", index=False)