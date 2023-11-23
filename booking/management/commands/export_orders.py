from django.core.management.base import BaseCommand
from booking.models import Order
import pandas as pd


class Command(BaseCommand):
    help = 'Fetches all orders and saves them to an Excel file'

    def add_arguments(self, parser):
        parser.add_argument('file_name', type=str,
                            help='The name of the output Excel file')

    def handle(self, *args, **options):
        file_name = options['file_name']
        orders = Order.objects.all().values()
        df = pd.DataFrame.from_records(orders)

        # Convert timezone-aware datetimes to naive datetimes
        for col in df.columns:
            if df[col].dtype == 'datetime64[ns, UTC]':
                df[col] = df[col].dt.tz_convert(None)

        df.to_excel(file_name, index=False)
        self.stdout.write(self.style.SUCCESS(
            f'Successfully saved orders to {file_name}'))
