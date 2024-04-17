from decimal import Decimal, InvalidOperation

from django.core.management.base import BaseCommand
import pandas as pd
from django.utils.dateparse import parse_date
from asset.models import Asset

class Command(BaseCommand):
    help = 'Imports data from an Excel file into the Asset model'

    def handle(self, *args, **options):
        df = pd.read_excel('Asset_Management_system.xlsx', engine='openpyxl')

        # Assuming df is your DataFrame after loading the Excel file
        df['PurchaseDate'] = pd.to_datetime(df['PurchaseDate'], errors='coerce')
        df['WarrantyExpirationDate'] = pd.to_datetime(df['WarrantyExpirationDate'], errors='coerce')
        df['LastMaintenanceDate'] = pd.to_datetime(df['LastMaintenanceDate'], errors='coerce')
        df['NextMaintenanceDate'] = pd.to_datetime(df['NextMaintenanceDate'], errors='coerce')

        # Ensure no essential columns are dropped
        if 'Category' in df:
            # Proceed with processing
            for index, row in df.iterrows():
                print(row['Category'])  # Example usage
        else:
            print("Column 'Category' does not exist.")
        # Iterate over the rows of the DataFrame
        for index, row in df.iterrows():
            purchase_price = convert_to_decimal(row['PurchasePrice'])
            Depreciation = convert_to_decimal(row['Depreciation'])
            asset = Asset(
                AssetName=row['AssetName'],
                Category=row['Category'],
                Department=row['Department'],
                Office=row['Office'],
                Location=row['Location'],
                Status=row['Status'],
                PurchaseDate= None,
                PurchasePrice=0,
                Depreciation=0,
                WarrantyExpirationDate= None,
                AssignedTo=row['AssignedTo'],
                LastMaintenanceDate=None,
                NextMaintenanceDate=None,
                Supplier_id=None,
                SerialNumber=row['SerialNumber'],
                Model=row['Model']
            )
            asset.save()
        self.stdout.write(self.style.SUCCESS('Successfully imported data.'))


def convert_to_decimal(value):
    try:
        # Convert the value to a string, trim whitespace, and replace any commas
        value = str(value).strip().replace(',', '')
        # Return a Decimal made from the value, or 0 if the value is empty
        return Decimal(value) if value else Decimal('0')
    except (InvalidOperation, TypeError, ValueError):
        # Return 0 if there's any error in conversion
        return Decimal('0')