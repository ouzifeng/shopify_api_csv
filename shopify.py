import requests
import csv

# Define the parameters
shop_url = "enter your shopify url"
access_token = "enter access token"
limit = 250  # Maximize the number of variants per request

# Build the request URL for variants
variants_url = f"https://{shop_url}/admin/api/2022-01/variants.json"

# Set up the headers
headers = {
    "Content-Type": "application/json",
    "X-Shopify-Access-Token": access_token
}

last_variant_id = 0  # Initialize with 0 to start from the beginning

# Create CSV file and write headers
with open('direct_variants.csv', 'w', newline='') as csvfile:
    fieldnames = ['Variant ID', 'Inventory Quantity', 'Price']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()

    while True:
        params = {
            "limit": limit,
            "fields": "id,inventory_quantity,price"
        }
        
        # Use the last_variant_id for pagination if set
        if last_variant_id:
            params["since_id"] = last_variant_id

        print(f"Fetching variants after variant ID: {last_variant_id}...")
        response = requests.get(variants_url, headers=headers, params=params)

        if response.status_code == 200:
            variants = response.json().get("variants", [])

            # If no more variants are returned, break out of the loop
            if not variants:
                print("No more variants found.")
                break
            
            print(f"Fetched {len(variants)} variants.")
            
            for variant in variants:
                writer.writerow({
                    'Variant ID': variant['id'],
                    'Inventory Quantity': variant['inventory_quantity'],
                    'Price': variant['price']
                })
                # Update the last_variant_id to the ID of the current variant
                last_variant_id = variant["id"]

        else:
            print(f"Failed to fetch variants after variant ID {last_variant_id}. Status code: {response.status_code}, Response: {response.text}")
            break

print("Data written to direct_variants.csv")
