                  Customer
               PK customer_id
                     │
                     │
                     │
                     ▼
                 Orders
     PK order_id
     FK customer_id
     FK product_id
     FK store_id
             │
     ┌───────┴─────────┐
     ▼                 ▼
 Product            Store
PK product_id    PK store_id
     │
     ▼
 Payment
FK order_id