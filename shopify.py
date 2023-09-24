import requests
import csv
from time import sleep

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
        
        if last_variant_id:
            params["since_id"] = last_variant_id

        print(f"Fetching variants after variant ID: {last_variant_id}...")
        response = requests.get(variants_url, headers=headers, params=params)

        if response.status_code == 200:
            variants = response.json().get("variants", [])

            if not variants:
                print("No more variants found.")
                logging.info("No more variants found.")
                break
            
            print(f"Fetched {len(variants)} variants.")
            
            for variant in variants:
                hook_variant_id = 'KEEN' + str(variant['id'])
                writer.writerow({
                    'Variant ID': hook_variant_id,
                    'Inventory Quantity': variant['inventory_quantity'],
                    'Price': variant['price']
                })

                last_variant_id = variant["id"]

            # Fixed sleep of 5 seconds
            sleep(5)

            # Dynamic sleep based on rate limit headers
            used_calls, total_calls = map(int, response.headers.get("X-Shopify-Shop-Api-Call-Limit", "0/1").split('/'))
            if used_calls >= total_calls - 1:  # If we are close to the rate limit
                reset_time = int(response.headers.get("X-Shopify-Shop-Api-Call-Reset", "10"))
                sleep(reset_time + 1)  # Sleep for the reset time plus a safety margin

        else:
            error_message = f"Failed to fetch variants after variant ID {last_variant_id}. Status code: {response.status_code}, Response: {response.text}"
            print(error_message)
            logging.error(error_message)
            break

print("Data written to direct_variants.csv")
