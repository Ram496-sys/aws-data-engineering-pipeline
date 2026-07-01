from faker import Faker
import pandas as pd
import random
from pathlib import Path

# ---------------------------------
# Faker Configuration
# ---------------------------------

fake = Faker("en_IN")

# ---------------------------------
# Project Configuration
# ---------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

OUTPUT_PATH = PROJECT_ROOT / "data" / "raw" / "customers.csv"

# Change these when testing incremental loads
START_CUSTOMER_ID = 200001
TOTAL_CUSTOMERS = 100000

# Used for generating duplicate emails
generated_emails = []


def generate_customer(customer_id):

    first_name = fake.first_name()
    last_name = fake.last_name()

    email = fake.email()

    # 2% NULL First Name
    if random.random() < 0.02:
        first_name = None

    # 2% NULL Email
    if random.random() < 0.02:
        email = None

    # 1% Duplicate Email
    elif generated_emails and random.random() < 0.01:
        email = random.choice(generated_emails)

    generated_emails.append(email)

    return {
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": fake.msisdn()[:10],
        "city": fake.city(),
        "state": fake.state(),
        "created_at": fake.date_time_this_year(),
    }


def main():

    customers = []

    for customer_id in range(
        START_CUSTOMER_ID,
        START_CUSTOMER_ID + TOTAL_CUSTOMERS,
    ):
        customers.append(generate_customer(customer_id))

    df = pd.DataFrame(customers)

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(OUTPUT_PATH, index=False)

    print("=" * 60)
    print("Customer Data Generated Successfully")
    print("=" * 60)
    print(f"Records Generated : {len(df)}")
    print(f"Customer ID Start : {START_CUSTOMER_ID}")
    print(f"Customer ID End   : {START_CUSTOMER_ID + TOTAL_CUSTOMERS - 1}")
    print(f"Output File       : {OUTPUT_PATH}")
    print("=" * 60)


if __name__ == "__main__":
    main()