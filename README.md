# Shopify API to CSV

Generate a CSV with all Shopify products using the Shopify API

## Introduction

Shopify has an annoying trait where the product IDs are not unique, which makes syncing data from Shopify to anywhere else challenging. 

The UID you need to use, which is hidden by Shopify, is the variant_id

## How to Use

The python scrpt takes the Shopify url and the access token (Google "Shopify, how to create an access token" if you are unsure how to do this. It basically an API credential)

It then loops through these variant_ids and generates a CSV in the same folder the script was executed which include the variant_id, price and stock quantity.The means you get a unie identifier for each product, and the necessary data points

The sciprt can be built out to include more data points yourself, or get in touch with me if you need more. 

## Technical Bit

Shopify rate limits API requests, I have set the max number of queries to 250 per request. This has been tested on 4 different stores with no issues. It is fast, a 20,000 product store takes about 60 seconds to generate





