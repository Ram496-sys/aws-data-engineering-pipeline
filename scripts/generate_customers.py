from faker import Faker
import pandas as pd
import random
from pathlib import Path

# Faker object for Indian data
fake = Faker("en_IN")

# Configuration
TOTAL_CUSTOMERS = 100_000
PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "customers.csv"


def generate_customer(customer_id):

    first_name = fake.first_name()
    email = fake.email()
    duplicate_emails = []

    if random.random() < 0.02:
        first_name = None

    if random.random() < 0.02:
        email = None

    # 1% duplicate emails
    elif duplicate_emails and random.random() < 0.01:
        email = random.choice(duplicate_emails)
    else:
        duplicate_emails.append(email)

    return {
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": fake.last_name(),
        "email": email,
        "phone": fake.msisdn()[:10],
        "city": fake.city(),
        "state": fake.state(),
        "created_at": fake.date_time_this_year()
    }


if __name__ == "__main__":

    TOTAL_CUSTOMERS = 10

    customers = []

    START_CUSTOMER_ID = 200001

    for customer_id in range(
        START_CUSTOMER_ID,
        START_CUSTOMER_ID + TOTAL_CUSTOMERS
    ):
        customers.append(generate_customer(customer_id))

    df = pd.DataFrame(customers)

    # Create folder if it doesn't exist
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save CSV
    df.to_csv(OUTPUT_PATH, index=False)

    print(f"Generated {len(df)} customers")
    print(f"File saved to: {OUTPUT_PATH}")