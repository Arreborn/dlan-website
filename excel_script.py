from booking.models import Orders
import os
import pandas as pd
import django

# Set the DJANGO_SETTINGS_MODULE environment variable
os.environ['DJANGO_SETTINGS_MODULE'] = 'dlan.settings'
django.setup()

# Import your models here

# Fetch data from the Django database


def fetch_orders():
    orders = Orders.objects.all().values()
    return orders

# Save data to an Excel file


def save_to_excel(data, file_name):
    df = pd.DataFrame.from_records(data)
    df.to_excel(file_name, index=False)


if __name__ == "__main__":
    data = fetch_orders()
    save_to_excel(data, 'orders.xlsx')
