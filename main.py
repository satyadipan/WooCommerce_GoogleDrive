from woocommerce import API
import csv
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# WooCommerce API setup
wcapi = API(
    url="http://example.com",  # Replace with your store URL
    consumer_key="your_consumer_key",  # Replace with your consumer key
    consumer_secret="your_consumer_secret",  # Replace with your consumer secret
    version="wc/v3"
)

# Google Drive Authentication
gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

# Fetch products from WooCommerce
products = wcapi.get("products").json()

# Process products and write to CSV
with open('products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["ID", "Title", "Description", "External Link", "Image Link", "Availability", "Price", "MPN", "Condition"])
    
    for product in products:
        writer.writerow([
            product.get("id"),
            product.get("name"),
            product.get("description"),
            product.get("permalink"),
            product.get("images")[0]["src"] if product.get("images") else None,
            product.get("stock_status"),
            product.get("price"),
            product.get("sku"),  
            "new"  # Assuming condition is new
        ])

# Upload file to Google Drive
file_drive = drive.CreateFile({'title': 'products.csv'})
file_drive.SetContentFile('products.csv')
file_drive.Upload()
print('File uploaded to Google Drive')
